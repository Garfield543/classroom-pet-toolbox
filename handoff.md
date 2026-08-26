# 專案交接紀錄 (Handoff)

- **更新時間**：2026-08-26 23:59
- **專案名稱**：classroom-pet-toolbox / teacher-toolkit

## ⏯️ 目前進度 / 上次做到哪
- 完成 RDQ Method（需求探索四象限法）技能的安裝、機制解析與環境適配。
- 已將 RDQ 技能部署至 Claude Code（`~/.claude/skills/rdq`）與 Google AntiGravity（`~/.gemini/config/skills/rdq`）。

## ➡️ 下一步建議 (Next Steps)
1. 在未來的教學工具開發、教材編寫或大型任務時，輸入「`用 RDQ`」體驗需求訪談與一頁規格卡。
2. 依實際教學與開發需求，於 `~/.gemini/config/skills/rdq/references/question-bank.md` 自訂專屬踩雷題庫。

## 📝 本次主要更動
- `~/.claude/skills/rdq/`：Clone 原版 RDQ Method 技能。
- `~/.gemini/config/skills/rdq/`：複製並啟用 AntiGravity 專用 RDQ 技能。
- `G:\我的雲端硬碟\secondbrain\teacher-toolkit\工作筆記.md`：同步更新進度與工具清單。

## 🕳️ 踩坑與注意事項
- AntiGravity 原生支援 `SKILL.md` 規範與 `ask_question` 結構化互動，使用 Claude 版原汁原味的 RDQ 體驗最完整，不需使用純文字降級版。
