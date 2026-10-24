"""Build sales/catalogue/trade_prices_2026-10-22.csv from Sristi's 3 PDFs and 4 JotForms (22 Oct 2026).
Data transcribed from text extracted by PyMuPDF (PDF) and BeautifulSoup (JotForm HTML). Never guessed: unclear -> 'check'."""
import csv, json, sys

JF = 'https://www.jotform.com/uploads/amit2sap/form_files/'
IMG = {  # JotForm product image filenames
'WH001':'5b2256cb_ba45_48e8_9f7d_3aeca3f38961_407de3043fbdec50b257c61f96d9115d.png',
'WH002':'84696013_c6e7_4128_840e_631321cddb67_2_84cd96d4d954399afd33935f8fc2ab80.png',
'WH003':'db73dfdf_9313_48cf_a73b_da8ee48056e6_2_ceb774617fd0155605b3a1e2903dac2c.png',
'WH004':'ce1fe41c_f4ca_4005_b4b6_e9d99204e045_2_1_4cb6a66860ca7cad499496193978a42c.png',
'WH005':'e3cf99ab_2d29_4774_85d9_3c776d75ca50_2_1_13b5f86ccde0cf752534af70f6e512e0.png',
'WH006':'b9c11b57_d3fa_489c_a312_0a5918148904_2_201f4c862564c152ed7d1cf36e13931f.png',
'WH007':'5f0058c8_cd22_49b5_9830_61bf9cacf24a_2_464f35135505f7345069468cccec4bd5.png',
'WH008':'afaa3db4_d9c7_4d52_83e7_392fd50987fe_2_b3e0538cf8ede8de06cab7d75d30c35d.png',
'WH009':'7ab5a156_124a_4a87_bc10_41e629dbb1b7_e47262d4a6a7d0a280b62c04b04a336d.png',
'WH010':'29a08328_5d70_4419_ab89_59e230c7699e_2_71aba64bead52389c21ac52b789e16b2.png',
'WH011':'88a6989a_4aac_4775_aa8b_3b1339ef8a79_bce1bc0a535fd8135dea333c39c1b5f2.png',
'WH012':'644367dc_5ce9_4f4c_92c6_360ad8ed8821_2_eb846ffee3b3bf327b4b63eeeeabb389.png',
'WH013':'e3e09753_f59d_4612_abae_6b97ad1c155d_2_2_15f509e8e01716bf7df556d2d4c62088.png',
'WH014':'6120c706_f7a7_49a3_bb7f_cfb28929edc0_2_dfa0b54d808d2289649b0e156d4a6f38.png',
'WH015':'af5005e4_5d54_445b_897e_53dbd76adbfa_2_f5baf009b34c2abf92424862c0ee821d.png',
'WH016':'29160936_c167_4409_8718_e225cb0eb63e_2_d172c7151e391b95a28aa7c35c64d761.png',
'WH017':'44420886_99ab_43fe_be03_d21fd9e41816_2_d019444bf56bdddcdefdd04bc252e21a.png',
'WH018':'img_20251018_wa0008_2_791ae2bce7b890ab5eab15db7e457480.png',
'AS001':'143a91d6_1cfa_4492_82a6_e8b9bdb2d1ac_2_36c9c7df6f8510a52f20f515c35822c8.png',
'AS002':'196787b6_ada0_4604_a3ed_7a69c02f510d_371594e6d0cfe8f6fec51b8951bcaa42.png',
'AS003':'8918dec3_7c51_44dd_83e2_0f3da40dc8db_fede188c0540260cca5a383531e066ff.png',
'AS004':'688d95d7_f3d6_46ba_af66_95c72f271784_2_f2e49e937dfcdb1eb75023bd4aca9e76.png',
'AS005':'eco_friendly_gift_set_display_29c44e75a002c2c3d7b81ad91c64e616.png',
'AS006':'f854f207_4926_4c8b_83b1_4958b5bd73ce_5c50a1cc5bb0c7aaeaebaa4e577c7f7c.png',
'AS007':'oct_19_2025_12_36_07_pm_487f3e7d381773e5238f28947624fcdf.png',
'AS008':'0cf46b53_7a02_403f_82c1_06120618a1b5_2_fa2f135ef0ec812422efda694cc2c9b5.png',
'AS009':'fb27c453_3f30_480b_a193_08ba31ea2404_b19bc918559d139c7aa6a18845573a3c.png',
'AS010':'cc678ea2_ff75_457b_9f01_e8380c8d2dae_7fde4d1b44df2ec7d927a1b6715955db.png',
'AS011':'8a123120_5f4e_4553_b034_af74d33de89f_395189512d2495b6fcf72f0bd8a847aa.png',
'AS012':'e810676b_79a3_4954_ac5d_0535edeb839f_efbfe58f33fc862402ccaf263d2a15bc.png',
'AS013':'099a922b_2a94_4448_aa64_406435b41563_3_b45f872c361a5bcc9a98a7e8acbdd89b.png',
'AS014':'2cdcc6d6_e44a_466c_8668_ca6c088601a3_e0bcdc0f987556c836658149396bcc07.png',
'AS015':'50b399ae_8786_4300_a7a7_b2ea6d444d97_4512ca689a2c4a61ac1f11153f81e992.png',
'AS016':'23f21c3f_404f_49d4_9980_c6dbc4f74050_8c09e5a3fbd9774918391aa1c17a1f50.png',
'AS017':'0fc2a975_f31b_47b9_9741_7237d141487f_a5fd530ae80cfc0778a8febf0f59c4fa.png',
'AS018':'b9d1e99f_8589_41b7_847c_bd6c1a383fd4_8112fa692ffcea5d47c612d4e0b33c57.png',
'AS019':'9be5cfe2_66ca_44e3_8c1b_d6fc6ef068b5_9fdcd0124950ee826876ae7e2b3a90ee.png',
'AS020':'0123542b_e384_454b_9a63_0eb81cbf7b38_66d0c63f9e577d37c6985fd11af6bff3.png',
'AS021':'788ed64b_2f00_4ab8_ab46_7eb15db7ca40_ffadfd1abafd10f897f9f97bbb7d7ca0.png',
'AS022':'5567cb25_598d_4bf1_91b0_d48564e9a709_2af983803eba523e251df16efad9a86a.png',
'SM001':'d9695e8a_219f_4938_a47f_c6cf08e33c99_1_1_8823e9fd4d2390d09fb8a7b2265f0ae1.png',
'SM002':'50957714_33f7_465c_8eab_c9cc775c3054_1_93b64fd9e1e4d27394067d4c18b05649.png',
'SM003':'1088b9a5_7ca1_40fa_916e_61f8cf8a6630_2_1_acf926a2e3fd3a9d9c9e6dc4ac501c7f.png',
'SM004':'d41875fe_8fed_488f_a25f_801b293e5ac3_1_1_22e8066c1b41b8257fb29625e72a92b0.png',
'SM005':'whatsapp_image_2023_11_10_at_3_52_26_pm_82a547919e4828f48d4a7607351a75be.jpeg',
'SM006':'a60c49e3_01b9_4e0e_8b09_2c05bf9bbb93_7958dcae54d39095e3c21d97ed76ef80.png',
'SM007':'6cac6108_d40c_41f7_bd50_5d67ff6b0cf3_1_72d48844e92d9380d8911a0a289a5277.png',
'SM008':'e24a99d2_cf7c_49ee_b940_9d7c7e61ff57_1_8af06e516cd2bbd0b3d34dd6881186b9.png',
'SM009':'ff2541ae_c389_4b8c_85aa_14e59cced611_1_cdc031e2922472b061482034071a0ca1.png',
'SM010':'792352bd_20e1_4a5c_9482_e331e6c578fe_2_1_17bfacc9d749985d75c1b1b53b8d6a75.png',
'SM011':'7db77800_a41c_49f5_8294_9eaa98b09989_1_ea3d3be07d42611629b43326dc36fda1.png',
'SM012':'baab99d8_b44f_4c8b_ab51_4e8d02311b13_1_6bd5b38776a916de3cd55ca6a2efb5f6.png',
'SM013':'440d00e6_46e5_4202_bd1f_64ba69e677a1_1_258d8c65b76c75c7c3fe47c5577d6ab1.png',
'SM014':'chatgpt_image_may_30_2025_08_58_55_am_1_1c532ca0a2042d426bef12e8f935ddf7.png',
'SM015':'befa371b_b20b_4afc_90d0_368210c3e525_4_1_af40ff3b8aaee8ba5ad44ee76ca7a2d7.png',
'SM016':'2133927e_5e46_48a2_8c95_1780f904457d_86b255807595747fb63157be0e79bb8b.png',
'SM017':'41c5fcab_82e2_41e8_8c32_e19e3c67b916_2_aba7d055685e217ff647b7243a80857f.png',
'KU001':'0736edcb_002d_4837_bd86_626ab3962d86_29115cedbd435a43a22c8db7239b79be.png',
'KU002':'ee09a51f_1538_459b_971e_c2d5b7615238_1_e7c26219d884953572f1ebbda17f839d.png',
'KU003':'21249a93_6a21_4193_be79_3c707e1ceb02_40f74d5636d7095f298fc276341c167e.png',
'KU004':'c1f2443b_0086_4922_8591_4674702a0039_2_1_0edc74bed761a7976097ca500d70b054.png',
'KU005':'chatgpt_image_may_26_2025_12_36_21_pm_2_b6b77d3915ea687d23c49ad27d6ed5ff.png',
'KU006':'1bc8ef38_a802_4174_9506_7b42cbe3e16d_e3623028231e5ef0a272ef72abd561c7.png',
'KU007':'88a67135_665d_43fa_89f3_07c76c282180_1_79fc1f9d0b69b5cef79a9b006cf7dbaf.png',
'KU008':'53cbecac_e61d_46cc_a454_e329145f528e_1_ddc818bbeaebda631f0f83ca61fa2718.png',
'KU009':'87a7ca8d_2e60_4472_a559_cc002470eb41_1_69ddb745aae7625ccb139cd7fd3317a2.png',
'KU010':'e1199a5d_31b4_4f7a_8358_e8b1119f39cc_2_1_3c53a7e3c30689d4c2e0f3e175104775.png',
'KU011':'3175929a_e35c_4c8a_a0ff_985a36d5aa05_1_20b4bbbbac2c78e346344a2ed4a9f4db.png',
'KU012':'5087781d_54b9_4d31_b814_f8096bf5cb5c_1_c53cd57f4934c8826b4f4cf322a5d3bd.png',
'KU013':'0bd76447_0d3c_4898_9f2b_cc523564b4cd_1_bdc7daf6a5681f8230bdf7f53526babd.png',
'KU014':'857894a0_0633_4f74_a8cf_5f4105caba93_1_1_ea3caad8cadda573bfdb4d2ffb5bc255.png',
'KU015':'f447f774_e819_4676_a422_fff85a1e6fb3_2_b89305ec22f5131321d9d40ee51e2510.png',
'KU016':'00905f57_4d2a_4f37_9f22_cba512814d5e_3_1_ec8c9b2ca5fb1d601b93443bed763fe6.png',
'KU017':'e8b82861_d9ca_4888_85a0_bae1f9080531_2_1_00d1107f9b609c90846996dc6ebb9c3e.png',
'KU018':'4fad9f86_92d8_424c_876f_c9498e9c22c0_d4be04b0b5450f2c32f5efeadf729126.png',
'KU019':'ac57234e_323d_447d_b69e_215d0eec49b5_1_e586dca55701fc72648e276762379c74.png',
'KU020':'723dc536_ec7d_4ff3_8a8f_0dd2c33dd502_1_e3af616f06427706b87ded1cf2ba60d3.png',
'KU021':'66c3e3e3_5494_4317_b62b_f8a1dbcc2d29_2_22370cd199d2ed2a87abda0cdb6e32f7.png',
'KU022':'e531d233_1c8e_4745_954f_28ca32fc85c1_2_1_8ec6f94a3d988d7c294185fe10c24c9c.png',
'KU023':'b04d8abc_1791_4d07_ba1f_a41c97c65f9e_2_1_35977b148a0acdf092c118e08c108f5b.png',
'KU024':'2d34fb6d_9e9b_4446_b1f3_da261ffaee42_2_1_23acd88a7beffbb47cd4bca4667e838c.png',
'KU025':'file_0000000067186230bfea3f95926d6af0_afe87554383f465f374557e01c7b6952.png',
'KU026':'d336b1fb_6867_4f57_a351_b4b4f10950ec_2_1_3_0c9f1e63ebbe66bad76ad25a1f9539cd.png',
'KU027':'img_20250409_wa0243_37819b6e44af483a419ed6c9cbcf674d.jpg',
'KU028':'77837ead_2f89_4659_9421_4a91e8ee370d_59642cbdffc8282410e716686551bd39.png',
'KU029':'d3c2b2f8_df81_4faf_b1f8_cb012e2eb4e7_1_e44f6fc52d244182921e718323256227.png',
'KU030':'50fa6bf2_d8ca_485a_84bd_b310c3579d7b_a9f43c5dd47b0dfeb602983a2fb51c49.png',
}

PDF_SM = 'PDF Sabai_BulkMay25.pdf'
PDF_KU = 'PDF Kauna_BulkJune25 (1).pdf'
PDF_AS = 'PDF Sabai_BulkJune25.pdf'
F_WH = 'JotForm 252891622774466 (Water Hyacinth)'
F_AS = 'JotForm 252893366646471 (Sabai Grass-2)'
F_SM = 'JotForm 252869411925465 (Sabai Grass)'
F_KU = 'JotForm 252628825024053 (Kauna)'

# (source, code, product, type, material, dimensions, price, note)
R = []
def add(src, code, product, typ, mat, sizes, note=''):
    for dim, price in sizes:
        R.append(dict(source=src, style_no=code, product=product, type=typ, material=mat,
                      dimensions=dim, trade_price_inr=price, note=note))

# ---------------- PDF Sabai_BulkMay25 (SM) ----------------
S = 'Sabai grass'
add(PDF_SM,'SM001','Sabai mat','Mat',S,[('Dia 6 in',65),('Dia 8 in',95),('Dia 10 in',125),('Dia 12 in',155),('Dia 14 in',195)])
add(PDF_SM,'SM002','Sabai mesh bag','Bag',S,[('L 12 x H 9 x W 5 in',400),('L 13 x H 12 x W 5 in',500),('L 16 x H 10 x W 5 in',575),('L 18 x H 14 x W 4 in',620)])
add(PDF_SM,'SM003','Sabai mesh bag','Bag',S,[('L 12 x H 6 x W 4 in',350)])
add(PDF_SM,'SM004','Sabai mesh bag','Bag',S,[('L 10 x H 8 x W 4 in',350)])
add(PDF_SM,'SM005','Sabai jar','Jar / box',S,[('Dia 4 x H 4 in',190),('Dia 5 x H 5 in',220),('Dia 6 x H 6 in',250)])
add(PDF_SM,'SM006','Sabai boat basket without handle','Basket',S,[('L 10 x H 6 x W 3 in',220),('L 12 x H 6 x W 3 in',270),('L 14 x H 7 x W 3 in',300)])
add(PDF_SM,'SM006','Sabai boat basket with handle','Basket',S,[('L 10 x H 6 x W 3 in',240),('L 12 x H 6 x W 3 in',290),('L 14 x H 7 x W 3 in',320)])
add(PDF_SM,'SM007','Sabai oval basket','Basket',S,[('L 8 x H 6 x W 2.5 in',240),('L 10 x H 8 x W 3 in',290)])
add(PDF_SM,'SM008','Sabai roti basket with lid','Roti basket',S,[('Dia 7 x H 3 in',300),('Dia 8 x H 3 in',350),('Dia 9 x H 3 in',400),('Dia 10 x H 3 in',450)])
add(PDF_SM,'SM009','Sabai box with lid','Box',S,[('Dia 4 x H 3 in',170),('Dia 5 x H 4 in',200),('Dia 6 x H 5 in',230)])
add(PDF_SM,'SM010','Sabai mesh oval basket','Basket',S,[('L 8 x H 5 x W 3 in',400),('L 10 x H 6.5 x W 3.5 in',450),('L 12 x H 8 x W 4 in',500)])
add(PDF_SM,'SM011','Sabai rectangular basket','Basket',S,[('L 9 x H 5 x W 4 in',230),('L 12 x H 9 x W 4 in',300)])
add(PDF_SM,'SM012','Sabai iron frame basket, without lid','Basket','Sabai grass, iron frame',[('L 910 (sic) x H 6.5 x W 3.5 in',500),('L 12 x H 9.5 x W 4.5 in',600),('L 14 x H 12.5 x W 5.5 in',700)],'PDF prints first length as "910"; JotForm gives L 10 in')
add(PDF_SM,'SM012','Sabai iron frame basket, with lid','Basket','Sabai grass, iron frame',[('L 910 (sic) x H 6.5 x W 3.5 in',575),('L 12 x H 9.5 x W 4.5 in',675),('L 14 x H 12.5 x W 5.5 in',825)],'PDF prints first length as "910"; with-lid prices only in PDF')
add(PDF_SM,'SM013','Sabai iron frame floral basket','Basket','Sabai grass, iron frame',[('Dia 8 x H 2.5 in',550),('Dia 10 x H 3 in',650),('Dia 12 x H 3.5 in',750)],'Dia 8 in: PDF 550 vs JotForm 500')
add(PDF_SM,'SM014','Sabai iron frame hexa basket','Basket','Sabai grass, iron frame',[('Dia 8 x H 2.5 in',525),('Dia 10 x H 3 in',600),('Dia 12 x H 3.5 in',700)])
add(PDF_SM,'SM015','Sabai mesh laundry basket','Laundry basket',S,[('Dia 10 x H 14 in',560),('Dia 14 x H 20 in',820)])

# ---------------- PDF Kauna_BulkJune25 (KU) ----------------
K = 'Kauna grass'
add(PDF_KU,'KU001','Kauna moon shape bag, leather handle','Bag',K+', leather handle',[('Dia 8 x W 4 in',430),('Dia 12 x W 4 in',550)])
add(PDF_KU,'KU002','Kauna moon shape bag, hand embroidery, grass handle','Bag',K,[('Dia 8 x W 4 in',550)])
add(PDF_KU,'KU003','Kauna U-shape bag, round cane handle','Bag',K+', cane handle',[('9 in',280),('11 in',300),('13 in',400),('14 in',470),('15 in',500)])
add(PDF_KU,'KU004','Kauna U-shape bag, round cane handle, hand embroidered','Bag',K+', cane handle',[('9 in',430),('11 in',450),('13 in',550),('14 in',620),('15 in',650)])
add(PDF_KU,'KU005','Kauna bag, grass handle','Bag',K,[('L 9 x H 9 x W 5 in',310),('L 12 x H 12 x W 5 in',380)])
add(PDF_KU,'KU005','Kauna bag, leather handle','Bag',K+', leather handle',[('L 12 x H 12 x W 5 in',550)])
add(PDF_KU,'KU006','Kauna bag, grass handle, hand embroidered','Bag',K,[('L 9 x H 9 x W 5 in',470),('L 12 x H 12 x W 5 in',550)],'JotForm KU006 is leather handle + embroidered at 650/700')
add(PDF_KU,'KU007','Kauna moon clutch','Clutch',K,[('10 in',230),('12 in',250)])
add(PDF_KU,'KU008','Kauna moon clutch, hand embroidered','Clutch',K,[('10 in',330),('12 in',360)])
add(PDF_KU,'KU009','Kauna U bag, grass handle, mesh/net pattern','Bag',K,[('15 in',470)])
add(PDF_KU,'KU010','Kauna U-shape bag, square cane handle','Bag',K+', cane handle',[('13 in',430)])
add(PDF_KU,'KU011','Kauna U-shape bag, triangle cane handle','Bag',K+', cane handle',[('11 in',300)])
add(PDF_KU,'KU012','Kauna bag, square cane handle','Bag',K+', cane handle',[('L 13 x H 13 x W 4 in',450)])
add(PDF_KU,'KU013','Kauna tote bag, grass handle','Bag',K,[('L 17 x H 12 x W 6 in',380)])
add(PDF_KU,'KU014','Kauna round gift hamper basket, dense weave','Hamper basket',K,[('Dia 9 x H 4 in',200)])
add(PDF_KU,'KU015','Kauna round gift hamper basket, mesh/net weave, grass handle','Hamper basket',K,[('Dia 6 x H 4 in',140)])
add(PDF_KU,'KU016','Kauna square gift hamper basket, mesh/net, single grass handle','Hamper basket',K,[('L 7 x H 5 x W 7 in',150)])
add(PDF_KU,'KU017','Kauna square gift hamper basket, mesh/net, double grass handle','Hamper basket',K,[('L 7 x H 5 x W 7 in',150)])
add(PDF_KU,'KU018','Kauna rectangular gift hamper basket, dense weave, round cane handle','Hamper basket',K+', cane handle',[('L 8 x W 6 x H 4 in',230),('L 9 x W 7 x H 4 in',250),('L 10 x W 8 x H 4 in',280),('L 12 x W 9 x H 5 in',300),('L 14 x W 10 x H 5 in',340)])
add(PDF_KU,'KU019','Kauna rectangular gift hamper basket, dense weave','Hamper basket',K,[('L 10 x W 8 x H 5 in',230)])
add(PDF_KU,'KU020','Kauna rectangular gift hamper basket, dense weave, grass handle','Hamper basket',K,[('L 10 x W 8 x H 5 in',230)])
add(PDF_KU,'KU021','Kauna oval gift hamper basket, dense weave, grass handle','Hamper basket',K,[('L 10 x W 6 x H 6 in',230)])
add(PDF_KU,'KU022','Kauna round gift hamper basket with cover, dense weave','Box with lid',K,[('Dia 10 x H 5 in',390)])
add(PDF_KU,'KU023','Kauna square gift hamper basket with cover, dense weave','Box with lid',K,[('L 8 x W 8 x H 5 in',340)])
add(PDF_KU,'KU024','Kauna rectangular gift hamper basket with cover, dense weave','Box with lid',K,[('L 10 x W 8 x H 5 in',360)])
add(PDF_KU,'KU025','Kauna rectangular gift hamper basket with cover and handle, dense weave','Box with lid',K,[('L 10 x W 8 x H 5 in',390)])
add(PDF_KU,'KU026','Kauna planter, mesh/net pattern','Planter',K,[('Dia 5 x H 5 in',130),('Dia 6 x H 6 in',160),('Dia 8 x H 8 in',240),('Dia 10 x H 10 in',330),('Dia 12 x H 12 in',430),('Dia 14 x H 14 in',650),('Dia 16 x H 16 in',850)])
add(PDF_KU,'KU026 (dense; JotForm KU027)','Kauna planter, dense weave','Planter',K,[('Dia 5 x H 5 in',150),('Dia 6 x H 6 in',180),('Dia 8 x H 8 in',290),('Dia 10 x H 10 in',370),('Dia 12 x H 12 in',470),('Dia 14 x H 14 in',700),('Dia 16 x H 16 in',900)],'PDF reuses style no. KU026 for the dense planter')

# ---------------- PDF Sabai_BulkJune25 (AS, sabai and palm leaf) ----------------
P = 'Sabai grass and palm leaf'
add(PDF_AS,'AS001','Sabai and palm leaf basket','Basket',P,[('Dia 6 x H 5 in',325),('Dia 8 x H 6 in',410)],'JotForm AS001: 375 / 420')
add(PDF_AS,'AS002','Sabai and palm leaf basket','Basket',P,[('Dia 6 x H 5 in',325),('Dia 8 x H 6 in',410)],'JotForm AS002 is a box Dia 6 x H 6 in at 350')
add(PDF_AS,'AS003','Sabai and palm leaf container','Container with lid',P,[('Dia 7 x H 5.5 in',325)])
add(PDF_AS,'AS004','Sabai and palm leaf container','Container with lid',P,[('Dia 6 x H 5 in',300)])
add(PDF_AS,'AS005','Sabai and palm leaf container','Container with lid',P,[('Dia 5 x H 5 in',275)])
add(PDF_AS,'AS006','Sabai and palm leaf container','Container with lid',P,[('Dia 4 x H 5 in',150)])
add(PDF_AS,'AS007','Sabai and palm leaf box','Box',P,[('L 10 x H 8 x W 5 in',350)])
add(PDF_AS,'AS008','Sabai and palm leaf box','Box',P,[('L 6 x H 4 x W 3 in',180)])
add(PDF_AS,'AS009','Sabai and palm leaf box','Box',P,[('L 3 x H 3 x W 3 in',180),('L 4 x H 4 x W 4 in',195),('L 5 x H 5 x W 5 in',220)])
add(PDF_AS,'AS010','Sabai and palm leaf box','Box',P,[('L 3 x H 3 x W 3 in',180),('L 4 x H 4 x W 4 in',195),('L 5 x H 5 x W 5 in',220)],'3 in: PDF 180 vs JotForm 185')
add(PDF_AS,'AS011','Sabai and palm leaf container','Container with lid',P,[('Dia 4 x H 5 in',220)])
add(PDF_AS,'AS012','Sabai and palm leaf cube box','Box',P,[('L 4 x H 4 x W 4 in',200),('L 5 x H 5 x W 5 in',230)])
add(PDF_AS,'AS013','Sabai and palm leaf kalash box','Box with lid',P,[('Dia 8 x H 8 in',450),('Dia 10 x H 10 in',500)])
add(PDF_AS,'AS014','Sabai and palm leaf kalash box','Box with lid',P,[('Dia 8 x H 8 in',450),('Dia 10 x H 10 in',500)])
add(PDF_AS,'AS015','Sabai and palm leaf abstract planter','Planter',P,[('Dia 8 x H 8 in',550)])
add(PDF_AS,'AS016','Sabai and palm leaf tray','Tray',P,[('L 10 x H 7 x W 2 in',340)])
add(PDF_AS,'AS017','Sabai and palm leaf bear basket','Planter / basket',P,[('Dia 10 x H 8 in',700)])
add(PDF_AS,'AS018','Sabai and palm leaf square box','Box',P,[('L 8 x H 8 x W 4 in',540),('L 10 x H 10 x W 3 in',600)])
add(PDF_AS,'AS019','Sabai and palm leaf round box','Box with lid',P,[('Dia 8 x H 4 in',500),('Dia 10 x H 4 in',550)])
add(PDF_AS,'AS020','Sabai and palm leaf table mat / coaster','Table mat',P,[('Dia 8 in',260),('Dia 10 in',360),('Dia 12 in',460)],'JotForm lists these mats as AS021; JotForm AS020 is a thali')

# ---------------- JotForm Water Hyacinth (WH) ----------------
W = 'Water hyacinth'
add(F_WH,'WH001','Round basket with handles, net (jali) weave','Basket',W,[('Dia 7 x H 4.5 in',190)])
add(F_WH,'WH002','Round basket with handles, dense weave','Basket',W,[('Dia 7 x H 3 in',180),('Dia 8 x H 5 in',210)])
add(F_WH,'WH003','Rectangle basket with handles, dense weave','Basket',W,[('L 11 x W 8 x H 3 in',280),('L 13 x W 9 x H 4 in',300)])
add(F_WH,'WH004','Square basket with lid, dense weave','Box with lid',W,[('L 10 x W 9 x H 6.5 in',490),('L 12 x W 10 x H 12 in',600)])
add(F_WH,'WH005','Basket with net-weave lid, dense weave','Box with lid',W,[('L 14 x W 12 x H 6 in',800)])
add(F_WH,'WH006','Rectangular basket with lid','Box with lid',W,[('L 12 x W 5 x H 5 in',430)])
add(F_WH,'WH007','Square basket with detachable lid','Box with lid',W,[('L 7 x W 7 x H 4 in',220)])
add(F_WH,'WH008','Rectangular basket, grass handles both sides','Basket',W,[('L 10 x W 4 x H 3 in',170)])
add(F_WH,'WH009','U-shaped basket, cane handles both sides','Basket',W+', cane handles',[('L 9 x W 6 x H 4 in',270),('L 12.5 x W 9.5 x H 6 in',420),('L 14.5 x W 9 x H 7 in',450)])
add(F_WH,'WH010','Round basket, detachable net-weave lid','Box with lid',W,[('Dia 10 x H 3 in',270)])
add(F_WH,'WH011','Square basket, detachable net-weave lid','Box with lid',W,[('L 4 x W 4 x H 3.5 in',190)])
add(F_WH,'WH012','Rectangle basket with cut-out handles','Basket',W,[('L 8 x W 8 x H 3 in',200)])
add(F_WH,'WH013','Round table mat','Table mat',W,[('Dia 12 in',150)])
add(F_WH,'WH014','Round dish organiser, net sides','Organiser',W,[('Dia 10 x H 7 in',390)])
add(F_WH,'WH015','Rectangle table mat','Table mat',W,[('L 18 x W 12 in',130)])
add(F_WH,'WH016','Rectangular basket','Basket / organiser',W,[('L 12 x W 4 x H 4 in',330)])
add(F_WH,'WH017','Square cutlery organiser with compartments and loop','Organiser',W,[('L 8 x W 8 x H 4 in',380)])
add(F_WH,'WH018','Rectangular organiser with compartments, net-weave lid','Organiser with lid',W,[('L 9.5 x W 7.5 x H 8 in',470)])

# ---------------- JotForm Sabai Grass-2 (AS) ----------------
add(F_AS,'AS001','Sabai and palm leaf basket','Basket',P,[('Dia 6 x H 5 in',375),('Dia 8 x H 6 in',420)],'PDF AS001: 325 / 410')
add(F_AS,'AS002','Sabai and palm leaf box','Box',P,[('Dia 6 x H 6 in',350)],'PDF AS002 is a basket 325 / 410')
add(F_AS,'AS003','Round sabai and palm leaf container','Container with lid',P,[('Dia 7 x H 5.5 in',325)])
add(F_AS,'AS004','Round sabai and palm leaf container','Container with lid',P,[('Dia 6 x H 5 in',300)])
add(F_AS,'AS005','Round sabai and palm leaf container','Container with lid',P,[('Dia 5 x H 5 in',275)])
add(F_AS,'AS006','Round sabai and palm leaf container','Container with lid',P,[('Dia 4 x H 5 in',150)])
add(F_AS,'AS007','Oval container','Container',P,[('L 10 x W 5 x H 8 in',350)])
add(F_AS,'AS008','Oval container','Container',P,[('L 6 x W 3 x H 4 in',180)])
add(F_AS,'AS009','Round container','Container with lid',P,[('L 3 x W 3 x H 3 in',180),('L 4 x W 4 x H 4 in',195),('L 5 x W 5 x H 5 in',220)])
add(F_AS,'AS010','Round container','Container with lid',P,[('L 3 x W 3 x H 3 in',185),('L 4 x W 4 x H 4 in',195),('L 5 x W 5 x H 5 in',220)],'3 in: JotForm 185 vs PDF 180')
add(F_AS,'AS011','Round container','Container with lid',P,[('Dia 4 x H 5 in',220)])
add(F_AS,'AS012','Cube container','Box with lid',P,[('L 4 x W 4 x H 4 in',200),('L 5 x W 5 x H 5 in',230)])
add(F_AS,'AS013','Round (kalash) container','Box with lid',P,[('Dia 8 x H 8 in',450),('Dia 10 x H 10 in',500)])
add(F_AS,'AS014','Round (kalash) container','Box with lid',P,[('Dia 8 x H 8 in',450),('Dia 10 x H 10 in',500)])
add(F_AS,'AS015','Round planter','Planter',P,[('Dia 8 x H 8 in',550)])
add(F_AS,'AS016','Tray','Tray',P,[('L 10 x W 7 x H 2 in',340)])
add(F_AS,'AS017','Round planter (bear)','Planter',P,[('Dia 10 x H 8 in',700)])
add(F_AS,'AS018','Square container','Box',P,[('L 8 x H 8 x W 4 in',540),('L 10 x H 10 x W 3 in',600)])
add(F_AS,'AS019','Round container','Box with lid',P,[('Dia 8 x H 4 in',500),('Dia 10 x H 4 in',550)])
add(F_AS,'AS020','Round thali / tray (Karwa Chauth, Bhai Dooj, puja)','Thali / tray',P,[('Dia 10 x H 3 in',400)])
add(F_AS,'AS021','Round table mat','Table mat',P,[('Dia 8 in',260),('Dia 10 in',360),('Dia 12 in',460)])
add(F_AS,'AS022','Round wall plate','Wall plate',P,[('Dia 8 in',300),('Dia 10 in',350),('Dia 12 in',400),('Dia 14 in',450)])

# ---------------- JotForm Sabai Grass (SM) ----------------
add(F_SM,'SM001','Sabai mat','Mat',S,[('Dia 4 in, set of 6',200),('Dia 6 in',65),('Dia 8 in',95),('Dia 10 in',125),('Dia 12 in',155),('Dia 14 in',195)])
add(F_SM,'SM002','Sabai mesh bag, leather handle','Bag',S+', leather handle',[('L 12 x H 9 x W 5 in',400),('L 13 x H 12 x W 5 in',500),('L 16 x H 10 x W 5 in',575),('L 18 x H 14 x W 4 in',620)])
add(F_SM,'SM003','Sabai mesh bag, leather handle','Bag',S+', leather handle',[('L 12 x H 6 x W 4 in',350)])
add(F_SM,'SM004','Sabai mesh bag with jari threads, leather handle','Bag',S+', jari thread, leather handle',[('L 10 x H 8 x W 4 in',350)])
add(F_SM,'SM005','Sabai jar with lid','Jar with lid',S,[('Dia 4 x H 4 in',190),('Dia 5 x H 5 in',220),('Dia 6 x H 6 in',250)])
add(F_SM,'SM006','Sabai boat basket, wooden handle','Basket',S+', wooden handle',[('L 10 x H 6 x W 3 in',240),('L 12 x H 6 x W 3 in',290),('L 14 x H 7 x W 3 in',320)])
add(F_SM,'SM007','Sabai oval basket','Basket',S,[('L 8 x H 6 x W 2.5 in',240),('L 10 x H 8 x W 3 in',290)])
add(F_SM,'SM008','Sabai roti basket, wooden lid','Roti basket',S+', wooden lid',[('Dia 7 x H 3 in',300),('Dia 8 x H 3 in',350),('Dia 9 x H 3 in',400),('Dia 10 x H 3 in',450)])
add(F_SM,'SM009','Sabai box, grass lid','Box with lid',S,[('Dia 4 x H 3 in',170),('Dia 5 x H 4 in',200),('Dia 6 x H 5 in',230)])
add(F_SM,'SM010','Sabai mesh oval basket','Basket',S,[('L 8 x H 5 x W 3 in',400),('L 10 x H 6.5 x W 3.5 in',450),('L 12 x H 8 x W 4 in',500)])
add(F_SM,'SM011','Sabai rectangular basket, grass handle','Basket',S,[('L 9 x H 5 x W 4 in',230),('L 12 x H 9 x W 4 in',300)])
add(F_SM,'SM012','Sabai iron frame basket','Basket','Sabai grass, iron frame',[('L 10 x H 6.5 x W 3.5 in',500),('L 12 x H 9.5 x W 4.5 in',600),('L 14 x H 12.5 x W 5.5 in',700)])
add(F_SM,'SM013','Sabai iron frame floral basket','Basket','Sabai grass, iron frame',[('Dia 8 x H 2.5 in',500),('Dia 10 x H 3 in',650),('Dia 12 x H 3.5 in',750)],'Dia 8 in: JotForm 500 vs PDF 550')
add(F_SM,'SM014','Sabai iron frame hexa basket','Basket','Sabai grass, iron frame',[('Dia 8 x H 2.5 in',525),('Dia 10 x H 3 in',600),('Dia 12 x H 3.5 in',700)])
add(F_SM,'SM015','Sabai mesh laundry basket','Laundry basket',S,[('Dia 10 x H 14 in',560),('Dia 14 x H 20 in',820)])
add(F_SM,'SM016','Sabai boat basket','Basket',S,[('L 10 x H 6 x W 3 in',220),('L 12 x H 6 x W 3 in',270),('L 14 x H 7 x W 3 in',300)])
add(F_SM,'SM017','Sabai iron frame box','Box','Sabai grass, iron frame',[('L 12 x W 10 x H 5 in','check')],'JotForm shows price as "Free" - price not given')

# ---------------- JotForm Kauna (KU) ----------------
add(F_KU,'KU001','Kauna moon shape bag, leather handle','Bag',K+', leather handle',[('Dia 8 x W 4 in',430),('Dia 12 x W 4 in',550)])
add(F_KU,'KU002','Kauna moon shape bag, hand embroidery, grass handle','Bag',K,[('Dia 8 x W 4 in',550)])
add(F_KU,'KU003','Kauna U-shape bag, round cane handle','Bag',K+', cane handle',[('9 in',280),('11 in',300),('13 in',400),('14 in',470),('15 in',500)])
add(F_KU,'KU004','Kauna U-shape bag, round cane handle, hand embroidered','Bag',K+', cane handle',[('9 in',430),('11 in',450),('13 in',550),('14 in',620),('15 in',650)])
add(F_KU,'KU005','Kauna bag, leather handle','Bag',K+', leather handle',[('L 12 x H 12 x B 5 in',550)])
add(F_KU,'KU006','Kauna bag, leather handle, hand embroidered','Bag',K+', leather handle',[('L 9 x H 9 x W 5 in',650),('L 12 x H 12 x W 5 in',700)],'PDF KU006 is grass handle + embroidered at 470/550')
add(F_KU,'KU007','Kauna moon clutch','Clutch',K,[('10 in',230),('12 in',250)])
add(F_KU,'KU008','Kauna moon clutch, hand embroidered','Clutch',K,[('10 in',330),('12 in',360)])
add(F_KU,'KU009','Kauna U bag, grass handle, mesh/net pattern','Bag',K,[('15 in',470)])
add(F_KU,'KU010','Kauna U-shape bag, square cane handle','Bag',K+', cane handle',[('13 in',430)])
add(F_KU,'KU011','Kauna U-shape bag, triangle cane handle','Bag',K+', cane handle',[('11 in',300)])
add(F_KU,'KU012','Kauna bag, square cane handle','Bag',K+', cane handle',[('L 13 x H 13 x W 4 in',450)])
add(F_KU,'KU013','Kauna tote bag, grass handle','Bag',K,[('L 17 x H 12 x W 6 in',380)])
add(F_KU,'KU014','Kauna round gift hamper basket, dense weave','Hamper basket',K,[('Dia 9 x H 4 in',200)])
add(F_KU,'KU015','Kauna round gift hamper basket, mesh/net, grass handle','Hamper basket',K,[('Dia 6 x H 4 in',140)])
add(F_KU,'KU016','Kauna square gift hamper basket, mesh/net, single grass handle','Hamper basket',K,[('L 7 x H 5 x W 7 in',150)])
add(F_KU,'KU017','Kauna square gift hamper basket, mesh/net, double grass handle','Hamper basket',K,[('L 7 x H 5 x W 7 in',150)])
add(F_KU,'KU018','Kauna rectangular gift hamper basket, dense, round cane handle','Hamper basket',K+', cane handle',[('L 8 x W 6 x H 4 in',230),('L 9 x W 7 x H 4 in',250),('L 10 x W 8 x H 4 in',280),('L 12 x W 9 x H 5 in',300),('L 14 x W 10 x H 5 in',340)])
add(F_KU,'KU019','Kauna rectangular gift hamper basket, dense weave','Hamper basket',K,[('L 10 x W 8 x H 5 in',230)])
add(F_KU,'KU020','Kauna rectangular gift hamper basket, dense, grass handle','Hamper basket',K,[('L 10 x W 8 x H 5 in',230)])
add(F_KU,'KU021','Kauna oval gift hamper basket, dense, grass handle','Hamper basket',K,[('L 10 x W 6 x H 6 in',230)])
add(F_KU,'KU022','Kauna round gift hamper basket with cover','Box with lid',K,[('Dia 10 x H 5 in',390)])
add(F_KU,'KU023','Kauna square gift hamper basket with cover','Box with lid',K,[('L 8 x W 8 x H 5 in',340)])
add(F_KU,'KU024','Kauna square gift hamper basket with cover','Box with lid',K,[('L 10 x W 8 x H 5 in',360)])
add(F_KU,'KU025','Kauna rectangular gift hamper basket with cover and handle','Box with lid',K,[('L 10 x W 8 x H 5 in',390)])
add(F_KU,'KU026','Kauna planter, mesh/net pattern','Planter',K,[('Dia 5 x H 5 in',130),('Dia 6 x H 6 in',160),('Dia 8 x H 8 in',240),('Dia 10 x H 10 in',330),('Dia 12 x H 12 in',430),('Dia 14 x H 14 in',650),('Dia 16 x H 16 in',850)])
add(F_KU,'KU027','Kauna planter, dense weave','Planter',K,[('Dia 5 x H 5 in',150),('Dia 6 x H 6 in',180),('Dia 8 x H 8 in',290),('Dia 10 x H 10 in',370),('Dia 12 x H 12 in',470),('Dia 14 x H 14 in',700),('Dia 16 x H 16 in',900)])
add(F_KU,'KU028','Kauna rectangular gift hamper basket with handle, jali/net weave','Hamper basket',K,[('L 9 x W 6 x H 4 in',180)])
add(F_KU,'KU029','Kauna bag, grass handle','Bag',K,[('L 9 x H 7 x W 4 in',300),('L 12 x H 9 x W 5 in',350)])
add(F_KU,'KU030','Kauna oval gift hamper basket with cover and handle','Box with lid',K,[('L 10 x H 5 x W 6 in',330)])

def img_ref(row):
    if row['source'].startswith('PDF'):
        return 'photo next to ' + row['style_no'] + ' in ' + row['source'][4:]
    return JF + IMG[row['style_no']]

if __name__ == '__main__':
    out = sys.argv[1]
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['source','style_no','product','type','material','dimensions','trade_price_inr','moq','image_ref','note'])
        w.writeheader()
        for r in R:
            ref = img_ref(r)
            w.writerow({**r, 'moq': 25, 'image_ref': ref})
    print(len(R), 'rows')
