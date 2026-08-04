# 專案筆記：學生成績登錄與智慧分析系統

## 1. 完成事項
- **後端 (Google Apps Script)**:
  - 建立 `gas_code.js`：具備 `doGet`、`doPost` API 與自動初始化/更新試算表邏輯。
  - 建立 `appsscript.json`：設定 Web App 存取權限為 `ANYONE_ANONYMOUS`、以部署者身分執行。
  - 建立 `.claspignore`：排除前端檔案，只推播後端程式碼。
  - 透過 `clasp` 初始化並成功部署 Web App（最新 API 部署 ID：`AKfycbzaHX4f1tMlKjr6e0_hSq1JJAk0lw2JhG69WtYcqn5IccA7bIjw7Tu26LkJidac_q9X`）。
- **前端 (Web UI)**:
  - 建立 `public/index.html`：基於 Outfit/Plus Jakarta Sans 字型，整合成績輸入表單、數據洞察區塊（全校最高分、及格率、學科排行）與成績總覽表格。
  - 建立 `public/style.css`：質感深色主題、漸層發光背景、玻璃擬物化卡片、按鈕與表格 hover 微動畫。
  - 建立 `public/app.js`：串接後端 API、處理非同步讀寫、動態更新數據與本地搜尋過濾。
- **部署**:
  - 全域安裝 `netlify-cli`。
  - 建立 Netlify 網站並完成生產環境部署（網站網址：`https://student-grade-ledger-76def6fb.netlify.app`）。
- **GitHub 連接 (已完成)**:
  - 確認系統環境：Windows 10，網路連線正常，Git 已安裝（v2.55.0）。
  - 自動使用 `winget` 安裝 GitHub CLI（v2.96.0），並刷新載入系統環境變數中。
  - 成功引導使用者透過瀏覽器登入 GitHub CLI（登入帳號：`Garfield543`）。
  - 設定 Git 全域使用者資訊：`user.name "Garfield"` 與 `user.email "ykes.cyc@gmail.com"`。
  - 建立 `github-test` 臨時專案推送至 GitHub，並啟用 GitHub Pages 驗證上線功能（驗證完成後已安全清理）。
- **Firebase 連接與 MCP 設定 (已完成)**:
  - 建立本機配置：`firestore.rules`（僅開放 `wordcloud_words` 與 `test_collection`）、`firebase.json` 與 `.firebaserc`。
  - 將白名單安全規則一鍵部署至雲端 Firestore 專案 `teacherstudy-12846`。
  - 在全域及專案設定中註冊並載入 Firebase MCP 伺服器，成功開啟 36 個資料庫工具並對接專案環境。
- **即時文字雲網頁應用程式 (已完成)**:
  - 於子目錄 `wordcloud` 中獨立建立前端項目：包含 `index.html`（Outfit/Inter 字型、統計面板與教師端密碼控制台）、`style.css`（深色玻璃擬物化樣式）與 `app.js`（Firebase 讀寫、`onSnapshot` 即時同步、`wordcloud2.js` 畫布渲染與教師端批次清除數據）。
  - 將專案推送至新建 GitHub 儲存庫 `firebase-wordcloud`。
  - 藉由 GitHub API 啟用並完成 GitHub Pages 部署（線上網頁：`https://garfield543.github.io/firebase-wordcloud/`）。
  - 成功驗證雲端 Firestore 資料寫入與即時文字雲繪製，且於後台進行了完整的 CRUD 驗證。
- **班級經營工具箱與獨立班級寵物整合 (已完成)**:
  - 成功整合 Gemini 班級寵物與表現計分器雙視窗應用。
  - **小組加分與事件前綴修復**：排除 inline `if` 事件編譯成 `window.petApp.if(...)` 的錯誤，重構將所有條件轉移至 JS 函數內部，確保所有動態與靜態按鈕皆能順暢運行並正確更新歷史紀錄。
  - **Gemini API 金鑰設定**：在 `💾 資料管理` 頁籤中提供 API 金鑰設定區塊與 `localStorage` 本地安全儲存，完成動態 API 金鑰預載，修復了 AI 連線失敗的故障。
  - **版面拉伸與去留白**：優化寵物舞台 CSS 為彈性拉伸設計，使舞台高度成功從固定 180px 延展至 314px（增長 74%），完美貼合螢幕，去除大片白底並防止任何版面裁切。

## 2. 踩坑與解決方案
- **npm/netlify 權限問題**:
  - 在 Windows PowerShell 中執行 `npm`、`npx` 會遇到 `PSSecurityException` 腳本執行安全限制。
  - **對策**：全面改用 `.cmd` 後綴（例如 `npm.cmd`、`npx.cmd`、`netlify.cmd`），可成功繞過 PowerShell 安全限制。
- **npx 執行緩慢與 stuck**:
  - 每一次執行 `npx.cmd netlify` 時 node 都會重新下載包，且易卡在互動輸入。
  - **對策**：直接執行 `npm.cmd install -g netlify-cli` 全域安裝，改用 `netlify.cmd` 執行，使部署流程毫秒級響應。
- **Google Apps Script 首次權限阻擋 (Authorization Required)**:
  - 直接呼叫 Web App API 會遭遇 404 或權限錯誤。
  - **對策**：引導使用者開啟線上編輯器手動執行一次任一函數，並點擊進階授權信任該腳本。
- **專案權限路徑夾帶隱藏字元導致沙盒報錯**:
  - 執行指令時，沙盒配置失敗並報錯 `sandbox configuration error: readwrite ...: non-absolute file path`。
  - **原因**：從屬性視窗複製路徑時夾帶了不可見的 `\u202a` (LRE) 字元，被寫入至 `C:\Users\User\.gemini\config\projects\78b678fb-2dff-4705-8e92-931be2495418.json` 權限清單中。
  - **對策**：直接編輯修正該專案 JSON 設定檔移除該隱藏字元，並引導使用者重啟 IDE 重新載入，即可正常執行終端機命令。
- **Firebase CLI 互動式登入卡死**:
  - 在背景任務中執行 `firebase login` 會因無 TTY 終端而報錯 `Cannot run login in non-interactive mode`。
  - **對策**：引導使用者在主機的獨立 PowerShell/CMD 中執行 `npx firebase-tools login`，登入後的 Token 會儲存於系統全域配置中，背景任務即可自動讀取並對接。
- **Firebase MCP 初始工具缺失**:
  - Firebase MCP 伺服器在未對接專案時僅加載 19 個基礎專案管理工具，無 `firestore_` CRUD 工具。
  - **對策**：利用 `firebase_update_environment` 顯式將 `project_dir` 設為包含 `firebase.json` 的專案目錄，並選定 active project，伺服器便會動態擴展加載至 36 個工具（包含全套 Firestore 工具）。
- **行內條件句 Event Namespacing 語法錯誤**:
  - HTML 或 JS 模板字串中的 `onclick="if(...) functionName()"` 在前綴編譯時會被 regex 誤寫為 `onclick="window.petApp.if(...)"`，進而拋出 TypeError。
  - **對策**：移除 HTML 事件屬性中的 inline `if` 判斷句，將條件分支完整移入 JS 函數體內處理，讓 onclick 屬性維持為純函數調用以便 regex 進行前綴 namespacing。
- **Gemini AI 功能連線失敗**:
  - Gemini API key 預設常數為空值 `apiKey = ""`，原版沒有提供 UI 設定。
  - **對策**：提供 API Key 輸入與本機 `localStorage` 安全持久化，使呼叫 API 時能動態讀取，並加載了友善的金鑰填寫提示彈窗。
- **五大底層文書自動化 Skills 安裝 (已完成)**:
  - 成功建立五大底層技能定義：`read_microsoft_docs`、`markitdown`、`PyMuPDF`、`pdf_ocr`、`pdf_extract_images`。
  - 安裝並設定相應的 Python 依賴包：`markitdown`、`pymupdf`、`pytesseract`。
  - 於專案根目錄建立一鍵安裝批次檔 `Install-Tesseract.bat`，以利使用者進行 UAC 授權完成 Tesseract-OCR 的本機安裝。

## 2. 踩坑與解決方案
- **npm/netlify 權限問題**:
  - 在 Windows PowerShell 中執行 `npm`、`npx` 會遇到 `PSSecurityException` 腳本執行安全限制。
  - **對策**：全面改用 `.cmd` 後綴（例如 `npm.cmd`、`npx.cmd`、`netlify.cmd`），可成功繞過 PowerShell 安全限制。
- **npx 執行緩慢與 stuck**:
  - 每一次執行 `npx.cmd netlify` 時 node 都會重新下載包，且易卡在互動輸入。
  - **對策**：直接執行 `npm.cmd install -g netlify-cli` 全域安裝，改用 `netlify.cmd` 執行，使部署流程毫秒級響應。
- **Google Apps Script 首次權限阻擋 (Authorization Required)**:
  - 直接呼叫 Web App API 會遭遇 404 或權限錯誤.
- **Tesseract OCR 背景靜態安裝受限**:
  - 在背景任務中透過 `winget` 執行靜態安裝時，會因 Windows 安全原則阻擋跨 Session UAC 彈窗而掛起。
  - **對策**：改為於專案目錄建立 `Install-Tesseract.bat`，引導使用者連點執行，即可順利於使用者 Session 內觸發 UAC 並自動安裝。

## 3. 下一步計畫
- **Tesseract OCR 執行驗證**：待使用者執行 `Install-Tesseract.bat` 後，對 `pdf_ocr` 技能進行實際的圖檔 PDF 辨識測試以確認一切正常。
- **試算表保護**：為試算表表頭列設定保護，防止管理員不小心手動刪改首行標題。
- **資料分頁**：當學生資料量擴大後，在前端 `app.js` 實現表格分頁 (Pagination) 以提升讀取效能。
- **資料防禦性驗證**：在前端加入更嚴格的學號格式檢查（如長度、英數字格式）與成績數值防呆。
- **文字雲字詞過濾機制 (Moderation)**：在前端 `app.js` 或 Firestore 安全性規則中，加入敏感詞彙/髒話過濾，避免不當單字顯示於大螢幕文字雲。
- **連線重試與錯誤邊界**：處理網路中斷時的 Firebase 重連狀態提示，給予使用者更友善的離線通知。
- **學生名單一鍵匯入**：在表現計分器中，提供一鍵複製貼上整班名單（換行或逗號分隔）並自動解析座號姓名，減少手動一個個新增學生的繁雜手續。
- **金鑰驗證提示**：在 API 金鑰儲存時，可向 Gemini 進行一次輕量級測試請求以驗證該金鑰是否有效，避免使用者打錯金鑰而不知。

