# 專案交接紀錄 (Handoff)

- **更新時間**：2026-08-31 00:30
- **專案名稱**：classroom-pet-toolbox

## ⏯️ 目前進度 / 上次做到哪
1. 實現「同步與備份」功能一鍵大整合：重寫 `exportData()` 與 `importData()`，現在點擊主畫面最下方的「同步與備份」即可將「表現計分器、作業追蹤器、潔牙表、考試計時器與班級寵物」的所有資料（包含金鑰與音效設定）一鍵打包為單一備份檔案。
2. 保持向下相容：匯入舊版只包含「班級資料」的 JSON 時，自動進行相容解析，不影響或覆寫現有的寵物資料庫。
3. 全功能通過 Selenium 自動化整合測試（`test_backup_unification.py`），並已編譯、同步至 GitHub 與部署上線至 Netlify。

## ➡️ 下一步建議 (Next Steps)
1. 在表現計分器中，提供一鍵複製貼上整班名單（換行或逗號分隔）並自動解析座號姓名，減少手動一個個新增學生的繁雜手續。
2. 在 API 金鑰儲存時，可向 Gemini 進行一次輕量級測試請求以驗證該金鑰是否有效，避免使用者打錯金鑰而不知。

## 📝 本次主要更動
- `scratch/claude_main_script.js`：修改 `exportData` 和 `importData` 以讀寫和整合班級寵物 LocalStorage 屬性。
- `compile_complete_pet.py`：新增輸出 `index.html`（根目錄）輸出通道，便於 Pages 託管。
- `public/index.html`、`index.html`、`班級經營工具箱.html`：整合後重新編譯。

## 🕳️ 踩坑與注意事項
- **LocalStorage 異步清空與 auto-initialize**：執行 `localStorage.clear()` 重載後，APP 會自動套用並儲存預設班級狀態（`我的班級` 等），因此斷言時需檢查其是否為預設狀態而非 None。
