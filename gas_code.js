// Google Apps Script Backend for Student Grade Registration System

function getOrCreateSpreadsheet() {
  var scriptProperties = PropertiesService.getScriptProperties();
  var spreadsheetId = scriptProperties.getProperty("SPREADSHEET_ID");
  var ss;

  if (spreadsheetId) {
    try {
      ss = SpreadsheetApp.openById(spreadsheetId);
    } catch (e) {
      // If the sheet was deleted or access lost, create a new one
      ss = null;
    }
  }

  if (!ss) {
    ss = SpreadsheetApp.create("學生成績登錄資料庫");
    var sheet = ss.getSheets()[0];
    sheet.setName("成績表");
    
    // Set headers
    var headers = ['學號', '姓名', '班級', '數學', '英文', '自然', '總分', '平均', '更新時間'];
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    
    // Format headers (bold, background color, center align)
    var headerRange = sheet.getRange("A1:I1");
    headerRange.setFontWeight("bold");
    headerRange.setBackground("#4f46e5"); // Indigo background
    headerRange.setFontColor("#ffffff");
    headerRange.setHorizontalAlignment("center");
    
    // Auto-fit columns
    sheet.autoResizeColumns(1, headers.length);
    
    scriptProperties.setProperty("SPREADSHEET_ID", ss.getId());
  }

  return ss;
}

function getSheet() {
  var ss = getOrCreateSpreadsheet();
  return ss.getSheetByName("成績表");
}

// Handle GET requests
function doGet(e) {
  try {
    var sheet = getSheet();
    var data = sheet.getDataRange().getValues();
    var headers = data[0];
    var rows = data.slice(1);
    
    var students = [];
    rows.forEach(function(row) {
      if (row[0] === "") return; // Skip empty rows
      var student = {};
      headers.forEach(function(header, index) {
        // Map headers to readable English keys for API
        var key = getApiKey(header);
        var val = row[index];
        if (val instanceof Date) {
          val = Utilities.formatDate(val, Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss");
        }
        student[key] = val;
      });
      students.push(student);
    });
    
    var ss = getOrCreateSpreadsheet();
    var spreadsheetUrl = ss.getUrl();

    var response = {
      success: true,
      spreadsheetUrl: spreadsheetUrl,
      students: students
    };
    
    return ContentService.createTextOutput(JSON.stringify(response))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// Map Chinese headers to JSON keys
function getApiKey(header) {
  switch (header) {
    case '學號': return 'id';
    case '姓名': return 'name';
    case '班級': return 'className';
    case '數學': return 'math';
    case '英文': return 'english';
    case '自然': return 'science';
    case '總分': return 'total';
    case '平均': return 'average';
    case '更新時間': return 'timestamp';
    default: return header;
  }
}

// Handle POST requests
function doPost(e) {
  try {
    var payload;
    if (e.postData && e.postData.contents) {
      payload = JSON.parse(e.postData.contents);
    } else {
      payload = e.parameter;
    }
    
    var id = payload.id;
    var name = payload.name;
    var className = payload.className;
    var math = parseFloat(payload.math) || 0;
    var english = parseFloat(payload.english) || 0;
    var science = parseFloat(payload.science) || 0;
    
    if (!id || !name || !className) {
      throw new Error("Missing required fields: id, name, className");
    }
    
    var total = math + english + science;
    var average = parseFloat((total / 3).toFixed(2));
    var timestamp = new Date();
    
    var sheet = getSheet();
    var data = sheet.getDataRange().getValues();
    var idColumnIndex = 0; // "學號" is column A
    
    var targetRowIndex = -1;
    for (var i = 1; i < data.length; i++) {
      if (data[i][idColumnIndex].toString() === id.toString()) {
        targetRowIndex = i + 1; // 1-based index
        break;
      }
    }
    
    var rowValues = [id, name, className, math, english, science, total, average, timestamp];
    
    if (targetRowIndex > -1) {
      // Update existing student
      sheet.getRange(targetRowIndex, 1, 1, rowValues.length).setValues([rowValues]);
    } else {
      // Append new student
      sheet.appendRow(rowValues);
    }
    
    // Force column resize and styling for new data
    sheet.autoResizeColumns(1, rowValues.length);
    
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      message: targetRowIndex > -1 ? "學生資料更新成功" : "學生資料新增成功",
      student: {
        id: id,
        name: name,
        className: className,
        math: math,
        english: english,
        science: science,
        total: total,
        average: average,
        timestamp: Utilities.formatDate(timestamp, Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss")
      }
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
