import sys
from rembg import remove,new_session
from PIL import Image, ImageFilter, ImageEnhance, ImageChops
import numpy as np
S=new_session('isnet-general-use')
def cutout(path,crop=None,th=38):
    im=Image.open(path).convert("RGB")
    if crop: im=im.crop(crop)
    a=np.asarray(im).astype(int)
    m=np.asarray(remove(im,session=S,only_mask=True)).astype(int)
    # background colour = median of border pixels
    border=np.concatenate([a[:15].reshape(-1,3),a[-15:].reshape(-1,3),a[:,:15].reshape(-1,3),a[:,-15:].reshape(-1,3)])
    bg=np.median(border,axis=0)
    dist=np.sqrt(((a-bg)**2).sum(-1))
    colmask=np.clip((dist-th)*6,0,255)
    # restrict colour mask to the product region (dilated rembg mask)
    region=np.asarray(Image.fromarray((m>40).astype(np.uint8)*255).filter(ImageFilter.MaxFilter(41))).astype(int)>0
    mask=np.where(region,np.maximum(m,colmask),0).astype(np.uint8)
    mask=Image.fromarray(mask).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    c=im.convert('RGBA'); c.putalpha(mask); return c.crop(c.getbbox())
def place(scene,c,cx,y,W,warm=True,out='o.jpg',zoom=None):
    sc=Image.open(scene).convert('RGBA'); H=int(c.height*W/c.width); c=c.resize((W,H),Image.LANCZOS)
    rgb=c.convert('RGB')
    if warm:
        rgb=ImageEnhance.Brightness(rgb).enhance(0.94); r,g,b=rgb.split(); r=r.point(lambda v:min(255,int(v*1.03))); b=b.point(lambda v:int(v*0.95)); rgb=Image.merge('RGB',(r,g,b))
    c2=rgb.convert('RGBA'); c2.putalpha(c.split()[3])
    x=cx-W//2
    sh=Image.new('RGBA',c2.size,(35,22,10,0)); sh.putalpha(c2.split()[3].point(lambda v:int(v*0.4))); sh=sh.filter(ImageFilter.GaussianBlur(8))
    o=sc.copy(); o.alpha_composite(sh,(x+5,y+9)); o.alpha_composite(c2,(x,y)); o=o.convert('RGB'); o.save(out,quality=92)
    if zoom: o.crop(zoom).save('zoom.jpg')
if __name__=='__main__':
    src,scene,cx,y,W,out=sys.argv[1:7]
    c=cutout(src); place(scene,c,int(cx),int(y),int(W),out=out,zoom=(int(cx)-300,int(y)-60,int(cx)+300,int(y)+200))
