/**
 * PCS Vector — Google Apps Script webhook (reliable referral capture)
 *
 * SETUP (about 3 minutes):
 * 1. Open the Google Sheet linked to your Form
 *    (Form → Responses → Link to Sheets), OR create any Sheet
 * 2. Extensions → Apps Script
 * 3. Delete any placeholder code and paste THIS entire file
 * 4. Click Deploy → New deployment → Type: Web app
 *      - Execute as: Me
 *      - Who has access: Anyone
 * 5. Deploy → copy the Web app URL
 * 6. Paste into Streamlit secrets:
 *
 *    [google_form]
 *    apps_script_url = "https://script.google.com/macros/s/XXXX/exec"
 *
 * The script appends a row with these columns (creates header row if missing):
 *   Timestamp | Destination | First Name | Last Name | Rank | Rent/Buy/Not Sure | Dependents | Email address
 */

var SHEET_NAME = "PCS Vector Referrals"; // change if you want a different tab name

function doPost(e) {
  try {
    var data = {};
    if (e.postData && e.postData.type === "application/json") {
      data = JSON.parse(e.postData.contents || "{}");
    } else if (e.parameter) {
      data = e.parameter;
    }

    var ss = SpreadsheetApp.getActiveSpreadsheet();
    if (!ss) {
      // If run from a standalone script, open by ID instead:
      // ss = SpreadsheetApp.openById("YOUR_SHEET_ID");
      throw new Error("No active spreadsheet. Run this script from the Sheet (Extensions → Apps Script).");
    }

    var sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
    }

    var headers = [
      "Timestamp",
      "Destination",
      "First Name",
      "Last Name",
      "Rank",
      "Rent/Buy/Not Sure",
      "Dependents",
      "Email address",
    ];

    if (sheet.getLastRow() === 0) {
      sheet.appendRow(headers);
    }

    sheet.appendRow([
      new Date(),
      data["Destination"] || "",
      data["First Name"] || "",
      data["Last Name"] || "",
      data["Rank"] || "",
      data["Rent/Buy/Not Sure"] || "",
      data["Dependents"] || "",
      data["Email address"] || "",
    ]);

    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ ok: false, error: String(err) })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput(
    JSON.stringify({ ok: true, message: "PCS Vector referral webhook is live. Use POST." })
  ).setMimeType(ContentService.MimeType.JSON);
}
