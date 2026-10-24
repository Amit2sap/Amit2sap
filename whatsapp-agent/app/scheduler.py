"""Background scheduler: an asyncio loop that runs due jobs from SQLite and the daily digest.

Jobs live in the ``jobs`` table, so they survive restarts. The loop wakes every
SCHEDULER_INTERVAL_SECONDS. Webhooks also trigger a run straight away for immediate messages.
"""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime
from typing import Any, Callable

from .automations import ShopifyAutomations
from .config import Settings
from .digest import IST, send_digest
from .store import Store

log = logging.getLogger(__name__)

MAX_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 300


class Scheduler:
    def __init__(
        self,
        settings: Settings,
        store: Store,
        automations: ShopifyAutomations,
        whatsapp: Any,
        email_sender: Callable[[str, str], None] | None = None,
    ):
        self.settings = settings
        self.store = store
        self.automations = automations
        self.whatsapp = whatsapp
        self.email_sender = email_sender
        self._lock = asyncio.Lock()
        self._task: asyncio.Task | None = None

    async def run_due(self, now: float | None = None) -> list[tuple[str, str]]:
        """Run every due job once. Returns [(job key, result)]."""
        async with self._lock:
            now = now or time.time()
            done: list[tuple[str, str]] = []
            for job in self.store.claim_due_jobs(now):
                try:
                    result = await self.automations.run_job(job["kind"], job["payload"], job["key"])
                    status = "sent" if result == "sent" else ("duplicate" if result == "duplicate" else "skipped")
                    self.store.finish_job(job["id"], status, result)
                except Exception as exc:
                    error = str(exc) or type(exc).__name__
                    if job["attempts"] + 1 >= MAX_ATTEMPTS:
                        self.store.finish_job(job["id"], "failed", error)
                        result = "failed"
                    else:
                        self.store.retry_job(job["id"], now + RETRY_DELAY_SECONDS * (job["attempts"] + 1), error)
                        result = "retry"
                    log.warning("job %s %s: %s", job["kind"], result, error)
                done.append((job["key"], result))
            return done

    async def maybe_send_digest(self, now: float | None = None) -> bool:
        """Send the owner digest once per IST day, at or after DIGEST_HOUR."""
        if not self.settings.digest_enabled:
            return False
        now = now or time.time()
        local = datetime.fromtimestamp(now, IST)
        if local.hour < self.settings.digest_hour:
            return False
        # Claimed in SQLite before sending, so a restart never sends the same day's digest twice.
        if not self.store.claim_meta("digest_last_date", local.strftime("%Y-%m-%d")):
            return False
        await send_digest(self.settings, self.store, self.whatsapp, self.email_sender, now)
        return True

    async def tick(self, now: float | None = None) -> None:
        try:
            await self.run_due(now)
        except Exception:
            log.exception("scheduler run failed")
        try:
            await self.maybe_send_digest(now)
        except Exception:
            log.exception("digest failed")

    async def _loop(self) -> None:
        while True:
            await self.tick()
            await asyncio.sleep(max(5, self.settings.scheduler_interval_seconds))

    def start(self) -> None:
        if self._task is None:
            self.store.reset_running_jobs()
            self._task = asyncio.create_task(self._loop())
            log.info("scheduler started (every %ss)", self.settings.scheduler_interval_seconds)

    async def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
