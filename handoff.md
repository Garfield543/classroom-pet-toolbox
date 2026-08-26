# 專案交接紀錄 (Handoff)

- **更新時間**：2026-08-27 00:05
- **專案名稱**：classroom-pet-toolbox

## ⏯️ 目前進度 / 上次做到哪
1. 完成跨 Agent（ChatGPT App / Codex、Claude Code、AntiGravity）的核心工作流技能升級與同步（`startup`、`shutdown`、`project-init`）。
2. 全面更新收工流程：自動在專案根目錄生成並維護 `handoff.md`，開工時支援讀取 `handoff.md` 或 Obsidian 筆記銜接進度。
3. 盤點並為 Claude Code 與 Codex 安裝補齊 11 項教學教材、文書文件與 PDF/OCR 技能工具（`lesson-planner`, `quiz-generator`, `knowledge-card-generator`, `html-slide-builder`, `document-formatter`, `calendar-csv-generator`, `read_microsoft_docs`, `PyMuPDF`, `pdf_extract_images`, `pdf_ocr`, `markitdown`）。

## ➡️ 下一步建議 (Next Steps)
1. 在 Claude Code 或 ChatGPT App 中測試執行各項新安裝的教學與文書技能（例如 `lesson-planner` 或 `quiz-generator`）。
2. 依專案需求接續課堂寵物工具箱或各項子模組開發。

## 📝 本次主要更動
- `~/.codex/skills/`：建立 14 項技能之 `SKILL.md` 與 `agents/openai.yaml`。
- `~/.claude/skills/` & `~/.claude-skills/`：安裝並同步 14 項技能。
- `~/.gemini/config/skills/`：更新 `startup`, `shutdown`, `project-init`, `05-workflow`。
- 專案根目錄：生成 `./handoff.md`。
- Obsidian Vault：建立/更新 `classroom-pet-toolbox/工作筆記.md`。

## 🕳️ 踩坑與注意事項
- 各 Agent 技能設定檔已完成 Windows cp950 / UTF-8 編碼相容處理，跨平台調用正常。
