// Frontend Application Logic for Student Grade System

const GAS_API_URL = "https://script.google.com/macros/s/AKfycbzaHX4f1tMlKjr6e0_hSq1JJAk0lw2JhG69WtYcqn5IccA7bIjw7Tu26LkJidac_q9X/exec";

// Application State
let studentList = [];
let spreadsheetUrl = "";

// DOM Elements
const gradeForm = document.getElementById("grade-form");
const studentIdInput = document.getElementById("student-id");
const studentNameInput = document.getElementById("student-name");
const studentClassInput = document.getElementById("student-class");
const scoreMathInput = document.getElementById("score-math");
const scoreEnglishInput = document.getElementById("score-english");
const scoreScienceInput = document.getElementById("score-science");

const btnSubmit = document.getElementById("btn-submit");
const btnReset = document.getElementById("btn-reset");
const btnText = document.getElementById("btn-text");
const btnSpinner = document.getElementById("btn-spinner");
const btnViewSheet = document.getElementById("btn-view-sheet");

const valTotalStudents = document.getElementById("val-total-students");
const valMathAvg = document.getElementById("val-math-avg");
const valEnglishAvg = document.getElementById("val-english-avg");
const valScienceAvg = document.getElementById("val-science-avg");

const valMathStatus = document.getElementById("val-math-status");
const valEnglishStatus = document.getElementById("val-english-status");
const valScienceStatus = document.getElementById("val-science-status");

const topStudentName = document.getElementById("top-student-name");
const topStudentScore = document.getElementById("top-student-score");
const passRatePercent = document.getElementById("pass-rate-percent");
const passRateFill = document.getElementById("pass-rate-fill");

const barMath = document.getElementById("bar-math");
const barEnglish = document.getElementById("bar-english");
const barScience = document.getElementById("bar-science");
const lblMathAvg = document.getElementById("lbl-math-avg");
const lblEnglishAvg = document.getElementById("lbl-english-avg");
const lblScienceAvg = document.getElementById("lbl-science-avg");

const tableSearch = document.getElementById("table-search");
const tableBody = document.getElementById("table-body");
const toast = document.getElementById("toast");
const toastMessage = document.getElementById("toast-message");

// Initialize
window.addEventListener("DOMContentLoaded", () => {
  fetchStudents();
  setupEventListeners();
});

function setupEventListeners() {
  gradeForm.addEventListener("submit", handleFormSubmit);
  btnReset.addEventListener("click", resetForm);
  tableSearch.addEventListener("input", filterTable);
}

// Fetch all students from Google Sheets database
async function fetchStudents() {
  try {
    const response = await fetch(GAS_API_URL);
    if (!response.ok) throw new Error("網路連線錯誤，無法取得資料");
    
    const result = await response.json();
    if (result.success) {
      studentList = result.students || [];
      spreadsheetUrl = result.spreadsheetUrl || "";
      
      // Update link to Spreadsheet
      if (spreadsheetUrl) {
        btnViewSheet.href = spreadsheetUrl;
        btnViewSheet.classList.remove("disabled");
      }
      
      renderTable(studentList);
      updateAnalytics(studentList);
    } else {
      showToast(result.error || "讀取資料失敗", "error");
    }
  } catch (error) {
    console.error("Fetch Error:", error);
    showToast(error.message || "無法連線至 Google Sheets 資料庫", "error");
  }
}

// Handle Form Submission (Add / Update)
async function handleFormSubmit(e) {
  e.preventDefault();
  
  // Set UI Loading State
  btnSubmit.disabled = true;
  btnText.classList.add("hidden");
  btnSpinner.classList.remove("hidden");
  
  const payload = {
    id: studentIdInput.value.trim(),
    name: studentNameInput.value.trim(),
    className: studentClassInput.value.trim(),
    math: parseInt(scoreMathInput.value) || 0,
    english: parseInt(scoreEnglishInput.value) || 0,
    science: parseInt(scoreScienceInput.value) || 0
  };
  
  try {
    // Send data to GAS Web App using POST
    const response = await fetch(GAS_API_URL, {
      method: "POST",
      mode: "no-cors", // Use no-cors for GAS redirects
      headers: {
        "Content-Type": "text/plain"
      },
      body: JSON.stringify(payload)
    });
    
    // Since 'no-cors' mode returns opaque response, we wait and fetch the updated list
    showToast("資料已送出！正在更新同步...", "success");
    resetForm();
    
    // Delay slightly to give GAS time to commit write
    setTimeout(async () => {
      await fetchStudents();
      showToast("資料庫同步成功！", "success");
      
      // Re-enable UI
      btnSubmit.disabled = false;
      btnText.classList.remove("hidden");
      btnSpinner.classList.add("hidden");
    }, 1500);

  } catch (error) {
    console.error("Submit Error:", error);
    showToast("寫入資料庫失敗，請確認網路連線", "error");
    btnSubmit.disabled = false;
    btnText.classList.remove("hidden");
    btnSpinner.classList.add("hidden");
  }
}

// Render student ledger table
function renderTable(students) {
  if (students.length === 0) {
    tableBody.innerHTML = `
      <tr class="empty-state-row">
        <td colspan="10" class="text-center">
          <div class="empty-state">
            <i class="fa-solid fa-folder-open empty-icon"></i>
            <p>目前尚無學生成績資料，請由上方表單進行登錄。</p>
          </div>
        </td>
      </tr>
    `;
    return;
  }
  
  tableBody.innerHTML = "";
  students.forEach(student => {
    const tr = document.createElement("tr");
    tr.dataset.id = student.id;
    
    tr.innerHTML = `
      <td>${student.id}</td>
      <td><strong>${student.name}</strong></td>
      <td>${student.className}</td>
      <td><span class="score-badge ${student.math >= 60 ? 'score-pass' : 'score-fail'}">${student.math}</span></td>
      <td><span class="score-badge ${student.english >= 60 ? 'score-pass' : 'score-fail'}">${student.english}</span></td>
      <td><span class="score-badge ${student.science >= 60 ? 'score-pass' : 'score-fail'}">${student.science}</span></td>
      <td class="avg-cell">${student.total}</td>
      <td class="avg-cell" style="color: ${student.average >= 60 ? '#34d399' : '#f87171'}">${student.average}</td>
      <td class="time-cell">${student.timestamp || '-'}</td>
      <td class="text-center">
        <button class="action-btn btn-edit" title="編輯此學生" onclick="editStudent('${student.id}')">
          <i class="fa-solid fa-pen-to-square"></i>
        </button>
      </td>
    `;
    tableBody.appendChild(tr);
  });
}

// Edit handler (pre-populate form fields)
window.editStudent = function(id) {
  const student = studentList.find(s => s.id === id);
  if (!student) return;
  
  studentIdInput.value = student.id;
  // Disable id modifications when editing to prevent duplicate creation
  studentIdInput.readOnly = false; // keep it readable
  
  studentNameInput.value = student.name;
  studentClassInput.value = student.className;
  scoreMathInput.value = student.math;
  scoreEnglishInput.value = student.english;
  scoreScienceInput.value = student.science;
  
  studentNameInput.focus();
  showToast(`已載入學號 ${student.id} 的成績資料`, "success");
};

// Filter ledger table locally
function filterTable() {
  const query = tableSearch.value.trim().toLowerCase();
  const rows = tableBody.querySelectorAll("tr");
  
  if (rows.length === 0 || rows[0].classList.contains("empty-state-row")) return;
  
  rows.forEach(row => {
    const cells = Array.from(row.querySelectorAll("td")).slice(0, 3); // check id, name, class
    const match = cells.some(cell => cell.textContent.toLowerCase().includes(query));
    if (match) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
}

// Reset Form fields
function resetForm() {
  gradeForm.reset();
  studentIdInput.readOnly = false;
}

// Process data and update Dashboard stats/insights
function updateAnalytics(students) {
  const count = students.length;
  valTotalStudents.textContent = count;
  
  if (count === 0) {
    valMathAvg.textContent = "0.0";
    valEnglishAvg.textContent = "0.0";
    valScienceAvg.textContent = "0.0";
    lblMathAvg.textContent = "0分";
    lblEnglishAvg.textContent = "0分";
    lblScienceAvg.textContent = "0分";
    barMath.style.width = "0%";
    barEnglish.style.width = "0%";
    barScience.style.width = "0%";
    topStudentName.textContent = "無資料";
    topStudentScore.textContent = "平均: - 分";
    passRatePercent.textContent = "0%";
    passRateFill.style.width = "0%";
    return;
  }
  
  // Calculate average scores
  let sumMath = 0, sumEnglish = 0, sumScience = 0;
  let allPassCount = 0;
  let topStudent = null;
  
  students.forEach(student => {
    const math = parseFloat(student.math) || 0;
    const english = parseFloat(student.english) || 0;
    const science = parseFloat(student.science) || 0;
    const avg = parseFloat(student.average) || 0;
    
    sumMath += math;
    sumEnglish += english;
    sumScience += science;
    
    if (math >= 60 && english >= 60 && science >= 60) {
      allPassCount++;
    }
    
    if (!topStudent || avg > topStudent.average) {
      topStudent = student;
    }
  });
  
  const avgMath = (sumMath / count).toFixed(1);
  const avgEnglish = (sumEnglish / count).toFixed(1);
  const avgScience = (sumScience / count).toFixed(1);
  
  // Update Big Cards
  valMathAvg.textContent = avgMath;
  valEnglishAvg.textContent = avgEnglish;
  valScienceAvg.textContent = avgScience;
  
  valMathStatus.textContent = getGradeRemark(avgMath);
  valEnglishStatus.textContent = getGradeRemark(avgEnglish);
  valScienceStatus.textContent = getGradeRemark(avgScience);
  
  // Update subject health ranks
  lblMathAvg.textContent = `${avgMath}分`;
  lblEnglishAvg.textContent = `${avgEnglish}分`;
  lblScienceAvg.textContent = `${avgScience}分`;
  
  barMath.style.width = `${avgMath}%`;
  barEnglish.style.width = `${avgEnglish}%`;
  barScience.style.width = `${avgScience}%`;
  
  // Top Student
  if (topStudent) {
    topStudentName.textContent = `${topStudent.name} (${topStudent.className})`;
    topStudentScore.textContent = `平均: ${topStudent.average} 分 | 總分: ${topStudent.total} 分`;
  }
  
  // Pass Rate (three subjects >= 60)
  const passRate = ((allPassCount / count) * 100).toFixed(0);
  passRatePercent.textContent = `${passRate}%`;
  passRateFill.style.width = `${passRate}%`;
}

// Remark indicator
function getGradeRemark(avg) {
  if (avg >= 85) return "卓越 (Excellent)";
  if (avg >= 70) return "良好 (Good)";
  if (avg >= 60) return "及格 (Pass)";
  return "待加強 (Needs Work)";
}

// Show Toast Notification helper
function showToast(message, type = "success") {
  toastMessage.textContent = message;
  toast.className = `toast ${type}`;
  toast.classList.remove("hidden");
  
  // Clear any existing timeouts if possible
  if (window.toastTimeout) clearTimeout(window.toastTimeout);
  
  window.toastTimeout = setTimeout(() => {
    toast.classList.add("hidden");
  }, 4000);
}
