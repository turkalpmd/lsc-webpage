/**
 * PRISM-III / PRISM-IV → Google Sheets writer
 *
 * Bu dosya, Google Apps Script editörüne yapıştırılmak üzere tasarlanmıştır.
 * Kullanım:
 *   1. https://sheets.new ile yeni bir spreadsheet oluştur, sayfa adını "PRISM" yap.
 *   2. Spreadsheet URL'inden SHEET_ID'yi al (/d/{SHEET_ID}/edit) ve aşağıdaki sabite yapıştır.
 *   3. Extensions → Apps Script → bu dosyanın tümünü yapıştır → Save.
 *   4. Deploy → New deployment → Web app → Execute as: Me, Who has access: Anyone → Deploy.
 *   5. Çıkan URL'i prism.html içindeki WEB_APP_URL sabitine yapıştır.
 *   6. Değişiklik yaparsan: Deploy → Manage deployments → kalem → Version: New → Deploy (aynı URL kalır).
 *
 * Mevcut deployment URL (Apr 16, 2026):
 *   https://script.google.com/macros/s/AKfycbzLC2GlcOpsJydYPpbeNE1JBkzUKvcLce7Dpfx1sUQUNL5uFJwRC1kdEBrlW8wQM1G52A/exec
 *
 * Sağlık kontrolü: Yukarıdaki URL'i tarayıcıdan aç → "PRISM endpoint OK" yazmalı.
 */

const SHEET_ID   = 'BURAYA_SHEET_ID_YAPISTIR';   // <-- DEĞİŞTİR
const SHEET_NAME = 'PRISM';

const COLUMNS = [
  'server_timestamp', 'client_timestamp', 'dosyano', 'score_type',
  // PRISM-III inputs (21)
  'iii_age_category', 'iii_sbp_low', 'iii_hr_high', 'iii_temp_low', 'iii_temp_high',
  'iii_gcs', 'iii_pupils_fixed', 'iii_ph_low', 'iii_ph_high',
  'iii_tco2_low', 'iii_tco2_high', 'iii_pco2_high', 'iii_pao2_low',
  'iii_glucose_mgdl', 'iii_potassium_meql', 'iii_creatinine_mgdl', 'iii_bun_mgdl',
  'iii_wbc', 'iii_pt', 'iii_ptt', 'iii_platelets_category',
  // PRISM-III scores (3)
  'iii_score_total', 'iii_score_neuro', 'iii_score_nonNeuro',
  // PRISM-IV inputs (5)
  'iv_age_category', 'iv_admission_source', 'iv_cpr_24h', 'iv_cancer', 'iv_low_risk_dysfunction',
  // PRISM-IV output (1)
  'iv_mortality_pct'
];

function doPost(e) {
  try {
    const data = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const ss = SpreadsheetApp.openById(SHEET_ID);
    let sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) sheet = ss.insertSheet(SHEET_NAME);

    if (sheet.getLastRow() === 0) {
      sheet.appendRow(COLUMNS);
      sheet.getRange(1, 1, 1, COLUMNS.length).setFontWeight('bold');
      sheet.setFrozenRows(1);
    }

    const iii = data.inputs_iii || {};
    const iv  = data.inputs_iv  || {};
    const s3  = data.score_iii  || {};
    const s4  = data.score_iv   || {};

    const row = [
      new Date(),
      data.timestamp_client || '',
      data.dosyano || '',
      data.score_type || '',
      // PRISM-III inputs
      iii.age_category || '',
      numOrEmpty(iii.sbp_low),  numOrEmpty(iii.hr_high),
      numOrEmpty(iii.temp_low), numOrEmpty(iii.temp_high),
      numOrEmpty(iii.gcs),      numOrEmpty(iii.pupils_fixed),
      numOrEmpty(iii.ph_low),   numOrEmpty(iii.ph_high),
      numOrEmpty(iii.tco2_low), numOrEmpty(iii.tco2_high),
      numOrEmpty(iii.pco2_high), numOrEmpty(iii.pao2_low),
      numOrEmpty(iii.glucose_mgdl),    numOrEmpty(iii.potassium_meql),
      numOrEmpty(iii.creatinine_mgdl), numOrEmpty(iii.bun_mgdl),
      numOrEmpty(iii.wbc), numOrEmpty(iii.pt), numOrEmpty(iii.ptt),
      iii.platelets_category || '',
      // PRISM-III scores
      numOrEmpty(s3.total), numOrEmpty(s3.neuro), numOrEmpty(s3.nonNeuro),
      // PRISM-IV inputs
      iv.age_category     || '',
      iv.admission_source || '',
      yesNoOrEmpty(iv.cpr_24h),
      yesNoOrEmpty(iv.cancer),
      yesNoOrEmpty(iv.low_risk_dysfunction),
      // PRISM-IV mortality
      (s4.mortality_probability != null)
        ? Number((s4.mortality_probability * 100).toFixed(2))
        : ''
    ];

    sheet.appendRow(row);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok', row: sheet.getLastRow() }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService
    .createTextOutput('PRISM endpoint OK')
    .setMimeType(ContentService.MimeType.TEXT);
}

function numOrEmpty(v) {
  if (v === null || v === undefined || v === '') return '';
  const n = Number(v);
  return isNaN(n) ? '' : n;
}

function yesNoOrEmpty(v) {
  if (v === null || v === undefined || v === '') return '';
  return v ? 'Evet' : 'Hayır';
}
