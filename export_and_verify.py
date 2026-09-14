# -*- coding: utf-8 -*-
import os, sys
import win32com.client
import fitz

gdrive_dir = r"G:\我的雲端硬碟\低年級寫作學習單"
student_docx = os.path.join(gdrive_dir, "看圖寫話學習單_學生版.docx")
student_pdf = os.path.join(gdrive_dir, "看圖寫話學習單_學生版.pdf")
teacher_docx = os.path.join(gdrive_dir, "看圖寫話學習單_教師版.docx")
teacher_pdf = os.path.join(gdrive_dir, "看圖寫話學習單_教師版.pdf")

preview_student_png = os.path.join(gdrive_dir, "學生版_預覽.png")
preview_teacher_png = os.path.join(gdrive_dir, "教師版_預覽.png")
local_student_png = r"c:\2026antigravity2\student_preview.png"
local_teacher_png = r"c:\2026antigravity2\teacher_preview.png"

word = win32com.client.Dispatch('Word.Application')
word.Visible = False

try:
    # 1. Export Student Version
    doc = word.Documents.Open(os.path.abspath(student_docx))
    doc.SaveAs2(os.path.abspath(student_pdf), 17) # 17 = wdFormatPDF
    doc.Close()
    print("Exported Student PDF")

    # 2. Export Teacher Version
    doc = word.Documents.Open(os.path.abspath(teacher_docx))
    doc.SaveAs2(os.path.abspath(teacher_pdf), 17)
    doc.Close()
    print("Exported Teacher PDF")
finally:
    word.Quit()

# 3. Check Page Count and Render PNGs
pdf_s = fitz.open(student_pdf)
print(f"Student PDF Page Count: {len(pdf_s)}")
page_s = pdf_s[0]
pix_s = page_s.get_pixmap(dpi=150)
pix_s.save(preview_student_png)
pix_s.save(local_student_png)
print("Rendered Student PNG preview")

pdf_t = fitz.open(teacher_pdf)
print(f"Teacher PDF Page Count: {len(pdf_t)}")
page_t = pdf_t[0]
pix_t = page_t.get_pixmap(dpi=150)
pix_t.save(preview_teacher_png)
pix_t.save(local_teacher_png)
print("Rendered Teacher PNG preview")
