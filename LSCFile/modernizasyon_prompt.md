# LSC Sayfa Modernizasyon Rehberi (modernizasyon_prompt.md)

Bu doküman, Hacettepe Life Support Center (LSC) sitesindeki eski şablon sayfaları modern,
tutarlı bir görünüme taşırken izlenen kuralları tanımlar. Yeni bir sayfayı modernize ederken
bu rehberi referans al.

> Amaç: Tüm sayfalarda **aynı tema, aynı bileşenler, aynı davranış**. İçeriği koru, kabuğu yenile.

---

## 0. Altın Kurallar

1. **İçeriği bozma.** Metin, liste, tablo, form ve özellikle interaktif JS araçlarının
   (hesaplayıcılar) mantığı korunur; sadece görsel kabuk modernize edilir.
2. **Paylaşılan navbar (`.ust`) aynen kalır.** Sitenin geri kalanıyla birebir aynı üst menü.
3. **UTF-8.** Dosya `<meta charset="utf-8">` ile yazılır; Türkçe karakterler düzeltilir
   (eski `iso-8859-9` bozulmaları giderilir).
4. **Düzenlemeden önce yedek al.** Orijinali `Backup/<dosya>.<timestamp>.bak` olarak kopyala.
5. **Deploy:** `cd FTPServer && python upload_all_from_lscfile.py --only-changed`
6. **Doğrula:** Deploy sonrası `curl`/snapshot ile sayfanın 200 döndüğünü ve yeni işaretleri
   (hero, grid vb.) içerdiğini kontrol et.

---

## 1. Head: Ortak Varlıklar

Her sayfanın `<head>` bloğunda şunlar bulunur:

```html
<meta charset="utf-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SAYFA ADI &middot; Life Support Center</title>

<!-- favicon + manifest (mevcut bloğu koru) -->

<link href="fontawesome/css/all.min.css" rel="stylesheet">
<script src="fontawesome/js/all.min.js"></script>

<!-- paylaşılan tema + navbar varlıkları -->
<link href="/sablon2021/css/bootstrap.min.css" rel="stylesheet" />
<link href="/sablon2021/css/style.css" rel="stylesheet" />
<link href="/sablon2021/css/all.min.css" rel="stylesheet" />
<script src="/sablon2021/js/jquery.min.js"></script>
<script src="/sablon2021/js/bootstrap.min.js"></script>
<script src="/sablon2021/js/main.js"></script>

<link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,700;0,800;1,300;1,400;1,700;1,800&display=swap" rel="stylesheet">
```

Sayfaya özel ağır/eski vendor scriptleri (jQueryAssets, resumes/portfolyo vendor, recaptcha vb.)
gerekmiyorsa kaldırılır.

---

## 2. Tema Token'ları (CSS değişkenleri)

Her sayfanın `<style>` bloğu bu değişkenlerle başlar:

```css
:root{
  --ink:#1f3551; --ink-soft:#3f4a5a; --muted:#7c8898;
  --red:#ec1b23; --red-deep:#c41019; --link:#0b6bd3;
  --bg:#ffffff; --soft:#f5f6f9; --card:#ffffff; --line:#e4e7ec;
  --shadow:0 1px 2px rgba(31,53,81,.05),0 14px 34px -20px rgba(31,53,81,.35);
  --shadow-hover:0 12px 28px -8px rgba(31,53,81,.45);
  --maxw:1120px;
}
```

- Yazı tipi: `"Open Sans", system-ui, Segoe UI, Roboto, sans-serif`
- Renk paleti: lacivert (`--ink`) + kırmızı vurgu (`--red`), beyaz/soft zemin.
- Stil sınıflarını bir kök kapsayıcıya ata (ör. `.page`, `.ppl`, `.inv`) ki paylaşılan
  navbar (`.ust`) etkilenmesin.

---

## 3. Animasyonlar

Hafif, "hero tarzı" giriş ve hover animasyonları:

```css
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
```

- Hero ve grid bölümleri yüklenince `fadeUp` ile belirir.
- Kartlar hover'da hafifçe yükselir: `transform:translateY(-5px/-6px)` + `--shadow-hover`.
- Görseller hover'da çok hafif zoom (`scale(1.05)`) — **kare/öncül logolar kırpılmamalı**
  (bkz. Görsel Kuralları).

---

## 4. Bileşenler

### 4.1 Hero (açık, kompakt)

Koyu/ağır kahraman değil; **açık zeminli, kısa** bir başlık bandı.

```css
.page .hero{background:linear-gradient(180deg,#ffffff 0%,var(--soft) 100%);
  border-bottom:1px solid var(--line);padding:30px 16px 22px;text-align:center}
.page .hero .eyebrow{font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:var(--red)}
.page .hero h1{margin:6px 0 0;font-weight:800;color:var(--ink);font-size:clamp(24px,3.4vw,34px)}
.page .hero p.lead{max-width:660px;margin:10px auto 0;color:var(--ink-soft);font-size:15px;line-height:1.55}
```

Not: Ana sayfada (index) ayrı bir hero metni yerine `images/banner.png` kullanılır; gereksiz
büyük/ağır başlık tekrarından kaçınılır.

### 4.2 Alt-navigasyon (subnav pills) — bölümlü alanlar için

Bir bölümün (ör. PICU: Administration/Fellows/Thesis/SMR/Album; PALS: ... ) sayfaları
arasında geçiş için hero altında pill butonlar; aktif sayfa kırmızı dolu.

```css
.page .subnav{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:18px}
.page .subnav a{padding:8px 16px;border-radius:999px;background:#fff;border:1px solid var(--line);
  font-weight:700;font-size:13.5px;color:var(--ink-soft);transition:all .18s ease}
.page .subnav a:hover{border-color:var(--red);color:var(--red);transform:translateY(-1px)}
.page .subnav a.active{background:var(--red);border-color:var(--red);color:#fff}
```

### 4.3 Kart Grid (görsel/section kutucukları)

```css
.page .grid{display:grid;gap:22px;grid-template-columns:repeat(3,1fr)}
@media(max-width:760px){.page .grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:480px){.page .grid{grid-template-columns:1fr}}
.page .card{border-radius:16px;overflow:hidden;background:#fff;box-shadow:var(--shadow);
  border-top:3px solid var(--red);transition:transform .2s ease,box-shadow .2s ease;
  animation:fadeUp .6s ease both}
.page .card:hover{transform:translateY(-6px);box-shadow:var(--shadow-hover)}
```

İsteğe bağlı zenginleştirmeler: sıra numarası rozeti (`.idx`), kategori ikonlu etiket (`.tag`).

### 4.4 Kişi Grid (yönetim / fellow / kurul listeleri)

```css
.ppl .grid{display:grid;gap:20px;grid-template-columns:repeat(auto-fill,minmax(190px,1fr))}
.ppl .pcard .photo{aspect-ratio:1/1;overflow:hidden;background:var(--soft)}
.ppl .pcard .photo img{width:100%;height:100%;object-fit:cover;object-position:center top}
.ppl .pcard h3{font-size:15px;font-weight:700;color:var(--ink)}
.ppl .pcard .role{color:var(--red);background:#fde7e8;padding:5px 12px;border-radius:999px;
  font-size:11.5px;font-weight:700;text-transform:uppercase}   /* görev rozeti */
.ppl .pcard .years{color:var(--red);font-weight:700;font-size:13px}  /* yıl bilgisi */
```

Yüz kırpılmasın diye `object-position:center top`.

### 4.5 Makale / Detay sayfası (yöntem/protokol)

Açık hero (amblem görsel + tag + başlık + alt başlık), ardından `.article` prose:

```css
.pg .article{max-width:880px;margin:0 auto;padding:30px 18px}
.pg .article p{color:var(--ink-soft);line-height:1.72;text-align:justify}
.pg .highlights li{background:var(--soft);border-left:3px solid var(--red);border-radius:10px;padding:12px 14px}
.pg .backbtn{border:1px solid var(--line);border-radius:999px;padding:10px 18px;font-weight:700}
```

Detay sayfasında "Back to ..." butonu ile ilgili liste sayfasına dönüş.

### 4.6 Footer (temalı)

```css
.page .site-footer{background:linear-gradient(135deg,#1f3551,#142a44);color:#fff}
.page .site-footer .inner{max-width:var(--maxw);margin:0 auto;padding:32px 18px;text-align:center}
.page .site-footer .social{display:flex;gap:16px;justify-content:center;font-size:20px}
.page .site-footer .copy{border-top:1px solid rgba(255,255,255,.14);padding:14px;
  font-size:13px;color:rgba(255,255,255,.7)}
```

Sosyal linkler: Instagram / Twitter(X) / LinkedIn. Telif: `© 2015–2026 Life Support Center`.

---

## 5. Görsel Kuralları

- **Amblem/logo görseller** (daire içi simgeler): soft radyal zemin üzerinde **kırpmadan**
  göster (`object-fit:contain`, hafif padding). Kare zaten kare; zoom ile bozma.
  ```css
  .thumb.logo{background:radial-gradient(circle at 50% 36%,#fff 0%,#eef2f8 70%,#e3e9f2 100%)}
  .thumb.logo img{object-fit:contain;padding:14px}
  ```
- **Fotoğraflar** (kişiler): `object-fit:cover` + `object-position:center top`.
- **WebP'ye sıkıştır.** Büyük PNG/JPEG'ler web dostu hale getirilir:
  - En uzun kenar ~800px'e indir, kalite 84–88, `method=6`.
  - Amblem/illustrasyon PNG'lerde gerekiyorsa 256 renk paleti (FASTOCTREE) ile ek küçültme.
  - Orijinali `Backup/`'a `.orig` ile sakla.
  - Hedef boyut: amblemler ~15–40KB, portreler ~30–60KB.
- `alt` metni her görselde anlamlı doldurulur.

---

## 6. Sayfa Tipleri ve Yaklaşım

| Tip | Örnek sayfalar | Düzen |
|-----|----------------|-------|
| Bölüm açılış (görsel ızgara) | PALS, pay_school, paylasim, h_bps, h_ecmo, labs, archive, awards, about_us | Hero + kart grid (görseller) |
| Kişi/kurul listeleri | advisory_board, steering_committee, picu_leaders, picu_adminstration, picu_fellows | Hero + subnav (varsa) + kişi grid |
| Yenilik/yöntem detayları | zipper, pisa, selba, colchicine, stemcell, dialooxygenator, hybrid_membrane, hfnc, oxopreserve, xeno_transplantation | Açık hero (amblem) + makale + geri butonu |
| Doküman/duyuru listeleri | activity_reports, legislation_textus, resolutions..., pals_documents, pals_handouts, pals_announcement, pay_school_archives | Hero + liste/indirme kartları |
| Galeri | lsc_gallery, paylasim_album, picu_album | Hero + responsive görsel grid (lightbox korunur) |
| İnteraktif araç/hesaplayıcı | dilutionfactor, lab_correction, padqi, ecca, pals_certification | **JS mantığını koru**, sadece kabuk/kart/form stilini modernize et |
| İletişim | contacts | Hero + iletişim kartı + form (form action korunur) |

---

## 7. Erişilebilirlik & Responsive

- Tek breakpoint mantığı: desktop 3–auto kolon, tablet 2, mobil 1–2.
- Kontrast: lacivert metin, kırmızı vurgu; küçük gri metin `--muted` ile.
- Tıklanabilir alanlar yeterli padding; pill/buton min 40px dokunma hedefi.

---

## 8. İş Akışı (her sayfa için checklist)

- [ ] Orijinali oku, içerik/işlev envanteri çıkar (form/JS/tablo var mı?).
- [ ] `Backup/`'a yedekle.
- [ ] UTF-8 + ortak head + tema token'ları.
- [ ] `.ust` navbar'ı koru.
- [ ] Uygun düzeni uygula (yukarıdaki tipe göre).
- [ ] Görselleri WebP'ye sıkıştır, `alt` ekle, kırpma kurallarına uy.
- [ ] İnteraktif mantığı test et (bozulmadı mı?).
- [ ] Lint temiz.
- [ ] Deploy (`--only-changed`) + canlı doğrulama.

---

## 9. Şu ana kadar modernize edilenler (referans)

- `index.html` (banner + kayan mottolar + section grid, swaplar)
- `innovations.html` (8 amblem kart, numara rozeti, kategori ikonları)
- `bbenan.html` (CV)
- `oxopreserve.html`, `co-apnea-test.html` (yöntem detay)
- `picu_adminstration.html`, `picu_fellows.html` (kişi grid + PICU subnav)

Bunlar örnek/şablon olarak kullanılabilir.
