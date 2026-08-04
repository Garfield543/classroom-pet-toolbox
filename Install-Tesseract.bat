@echo off
chcp 65001 >nul
echo ===================================================
echo   正在安裝 Tesseract-OCR (Antigravity 技能依賴)
echo ===================================================
echo.
echo 正在透過 winget 啟動 Tesseract-OCR 安裝...
echo (可能會出現 Windows 使用者帳戶控制 UAC 提示，請按「是」授權)
echo.
winget install UB-Mannheim.TesseractOCR --accept-package-agreements --accept-source-agreements
echo.
echo ---------------------------------------------------
echo 安裝程序已完成！
echo 請按任意鍵關閉此視窗...
pause >nul
