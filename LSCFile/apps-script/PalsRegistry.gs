/**
 * PALS Kayıt Formu (palsregistery.html) → Google Sheets writer
 *
 * Bu dosya, Google Apps Script editörüne yapıştırılmak üzere tasarlanmıştır.
 *
 * Kurulum:
 *   1. Extensions → Apps Script → bu dosyanın tümünü yapıştır → Save.
 *   2. Deploy → Manage deployments → kalem → Version: New version → Deploy.
 *      (Kodu kaydetmek yetmez; /exec adresi her zaman YAYINLANMIŞ sürümü çalıştırır.
 *       "New deployment" yerine mevcut deployment'ı düzenlersen URL sabit kalır ve
 *       palsregistery.html'i yeniden yayınlamak gerekmez.)
 *   3. Web app ayarları: Execute as: Me, Who has access: Anyone.
 *
 * Bağlı kaynaklar (Aug 1, 2026):
 *   Sheet : https://docs.google.com/spreadsheets/d/1i29Xd9t4pIshT-sQyd7TQSeGB5piObtJ2NrV4strlN8/edit
 *   Deploy: AKfycbxgNwa-4s268vLTnt-A6dFPOwLWlCqDBPr9-YBKeKRGlwIM-wfwZ6gm9EjTW2YYDLKR
 *   URL   : https://script.google.com/macros/s/AKfycbxgNwa-4s268vLTnt-A6dFPOwLWlCqDBPr9-YBKeKRGlwIM-wfwZ6gm9EjTW2YYDLKR/exec
 *
 * Sağlık kontrolü: Yukarıdaki URL'i tarayıcıdan aç → "PALS registry endpoint OK" yazmalı.
 */

const SHEET_ID   = '1i29Xd9t4pIshT-sQyd7TQSeGB5piObtJ2NrV4strlN8';
const SHEET_NAME = 'Sheet1';

/** Sheet başlıkları — sıra, doPost'taki row dizisiyle birebir aynı olmalı. */
const COLUMNS = [
  'server_timestamp', 'client_timestamp',
  'TCKN', 'PasaportNo', 'Ad', 'Soyad', 'Gün', 'Ay', 'Yıl',
  'Adres', 'Email', 'Telefon', 'Kurumici',
  'TıpFakültesiÖğrencisi', 'PediatriAsistanı', 'Hemşire', 'Diğer',
  'KVKKOnay', 'KVKKOnayZamani'
];

/** Düz metin kalması gereken sütunlar (1 tabanlı): TCKN, PasaportNo, Telefon. */
const TEXT_COLUMNS = [3, 4, 12];

const NA = 'NA';

function doPost(e) {
  try {
    const data = JSON.parse((e && e.postData && e.postData.contents) || '{}');

    // TCKN veya PasaportNo — en az biri dolu olmalı.
    const tckn = txt(data.TCKN);
    const pass = txt(data.PasaportNo);
    if ((tckn === NA || tckn === '') && (pass === NA || pass === '')) {
      return json({ status: 'error', message: 'TCKN veya PasaportNo alanlarından biri zorunludur.' });
    }
    if (!txt(data.Ad) || !txt(data.Email)) {
      return json({ status: 'error', message: 'Ad ve Email alanları zorunludur.' });
    }
    if (data.KvkkOnay !== 'Evet') {
      return json({ status: 'error', message: 'KVKK onayı olmadan kayıt alınamaz.' });
    }

    const sheet = getSheet_();

    const row = [
      new Date(),
      txt(data.timestamp_client),
      naOr(tckn),
      naOr(pass),
      txt(data.Ad),
      txt(data.Soyad),
      numOrNa(data.Gun),
      numOrNa(data.Ay),
      numOrNa(data.Yil),
      txt(data.Adres),
      txt(data.Email),
      txt(data.Telefon),
      binary(data.Kurumici),
      naOr(txt(data.TipFakultesiOgrencisi)),
      naOr(txt(data.PediatriAsistani)),
      naOr(txt(data.Hemsire)),
      naOr(txt(data.Diger)),
      'Evet',
      txt(data.KvkkOnayZamani)
    ];

    sheet.appendRow(row);

    return json({ status: 'ok', row: sheet.getLastRow() });
  } catch (err) {
    return json({ status: 'error', message: String(err) });
  }
}

function doGet() {
  return ContentService
    .createTextOutput('PALS registry endpoint OK')
    .setMimeType(ContentService.MimeType.TEXT);
}

/* ------------------------------------------------------------------ */

/**
 * Hedef sayfayı döndürür ve başlık satırının COLUMNS ile hizalı olmasını garanti eder.
 *
 * Henüz veri satırı yokken başlık satırı COLUMNS ile birebir yeniden yazılır — sütun
 * sırası değiştiğinde Sheet'i elle düzeltmek gerekmez. Veri girdikten sonra başlığa
 * dokunulmaz, çünkü mevcut satırların hizası bozulurdu.
 */
function getSheet_() {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SHEET_NAME);

  if (sheet.getMaxColumns() < COLUMNS.length) {
    sheet.insertColumnsAfter(sheet.getMaxColumns(), COLUMNS.length - sheet.getMaxColumns());
  }

  if (sheet.getLastRow() <= 1) {
    sheet.getRange(1, 1, 1, COLUMNS.length).setValues([COLUMNS]).setFontWeight('bold');
    sheet.setFrozenRows(1);
    // TCKN bilimsel gösterime düşmesin, telefondaki baştaki 0 kaybolmasın.
    const rows = sheet.getMaxRows() - 1;
    if (rows > 0) {
      TEXT_COLUMNS.forEach(function (c) {
        sheet.getRange(2, c, rows, 1).setNumberFormat('@');
      });
    }
  }
  return sheet;
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function txt(v) {
  return (v === null || v === undefined) ? '' : String(v).trim();
}

/** Boş gelen seçimler sheet'te NA olarak görünür. */
function naOr(v) {
  const s = txt(v);
  return s === '' ? NA : s;
}

function numOrNa(v) {
  if (v === null || v === undefined || v === '') return NA;
  const n = Number(v);
  return isNaN(n) ? NA : n;
}

/** Kurumici her zaman 0 veya 1 olarak yazılır. */
function binary(v) {
  const s = txt(v);
  if (s === '1' || s === 'true' || s === 'Evet') return 1;
  if (s === '0' || s === 'false' || s === 'Hayır') return 0;
  return NA;
}
