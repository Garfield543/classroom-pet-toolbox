# -*- coding: utf-8 -*-
import os, sys
import docx
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import win32com.client
import fitz

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for border_name, border_val in borders.items():
        if border_val:
            val = border_val.get("val", "single")
            sz = border_val.get("sz", "4")
            color = border_val.get("color", "000000")
            b_xml = parse_xml(f'<w:{border_name} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>')
            tcBorders.append(b_xml)
        else:
            b_xml = parse_xml(f'<w:{border_name} {nsdecls("w")} w:val="none"/>')
            tcBorders.append(b_xml)
    tcPr.append(tcBorders)

def add_run_bpmf(paragraph, text, font_size=10.5, bold=False, color_rgb=(0,0,0)):
    font_name = "Bpmf Iansui Regular"
    r = paragraph.add_run(text)
    r.font.name = font_name
    r.font.size = Pt(font_size)
    r.font.bold = bold
    r.font.color.rgb = RGBColor(*color_rgb)
    if r._element.rPr is None:
        r._element.get_or_add_rPr()
    r._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    r._element.rPr.rFonts.set(qn('w:ascii'), font_name)
    r._element.rPr.rFonts.set(qn('w:hAnsi'), font_name)
    return r

def build_doodle_worksheet(output_docx):
    doc = docx.Document()
    
    # 1. Page Setup - A4 Portrait with compact margins
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(0.9)
    section.bottom_margin = Cm(0.7)
    section.left_margin = Cm(1.0)
    section.right_margin = Cm(1.0)
    
    doodle_dir = r"c:\2026antigravity2\doodles"
    pot_img = os.path.join(doodle_dir, "pot.png")
    polaroid_img = os.path.join(doodle_dir, "empty_polaroid.jpg")
    camera_img = os.path.join(doodle_dir, "camera.png")
    tools_img = os.path.join(doodle_dir, "kitchen_tools.png")
    
    # ==================== HEADER TABLE ====================
    hdr_table = doc.add_table(rows=1, cols=2)
    hdr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_table.autofit = False
    
    # Left Header: Text
    cell_hdr_l = hdr_table.cell(0, 0)
    cell_hdr_l.width = Cm(15.2)
    set_cell_borders(cell_hdr_l)
    set_cell_margins(cell_hdr_l, top=0, bottom=20, left=0, right=40)
    
    p_sub = cell_hdr_l.paragraphs[0]
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(1)
    add_run_bpmf(p_sub, "◎ 國語第二課延伸學習 ‧ 親子共學體驗", font_size=9, bold=False, color_rgb=(80,80,80))
    
    p_title = cell_hdr_l.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    add_run_bpmf(p_title, "《一\U000e01e2起做○○》美味料理塗鴉筆記學習單", font_size=15.5, bold=True, color_rgb=(10,10,10))
    
    p_info = cell_hdr_l.add_paragraph()
    p_info.paragraph_format.space_before = Pt(1)
    p_info.paragraph_format.space_after = Pt(0)
    add_run_bpmf(p_info, "二年____班   座號：____   姓名：____________   日期：____年____月____日", font_size=10, bold=True, color_rgb=(40,40,40))
    
    # Right Header: Pot doodle
    cell_hdr_r = hdr_table.cell(0, 1)
    cell_hdr_r.width = Cm(3.8)
    set_cell_borders(cell_hdr_r)
    set_cell_margins(cell_hdr_r, top=0, bottom=20, left=10, right=0)
    p_pot = cell_hdr_r.paragraphs[0]
    p_pot.paragraph_format.space_before = Pt(0)
    p_pot.paragraph_format.space_after = Pt(0)
    p_pot.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if os.path.exists(pot_img):
        p_pot.add_run().add_picture(pot_img, width=Cm(3.5))

    # Divider Sketch Line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(1)
    p_div.paragraph_format.space_after = Pt(3)
    p_div.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run_bpmf(p_div, "—"*52, font_size=8, bold=False, color_rgb=(120,120,120))

    # ==================== MAIN 2-COLUMN NOTEBOOK TABLE ====================
    main_table = doc.add_table(rows=1, cols=2)
    main_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    main_table.autofit = False
    
    # -------------------- LEFT COLUMN (9.3 cm) --------------------
    cell_left = main_table.cell(0, 0)
    cell_left.width = Cm(9.4)
    set_cell_margins(cell_left, top=30, bottom=30, left=40, right=60)
    set_cell_borders(cell_left, right={'val': 'dashed', 'sz': '6', 'color': '999999'}) # notebook spine/divider
    
    # [SECTION 1: 壹、烹飪基本資訊]
    p_s1 = cell_left.paragraphs[0]
    p_s1.paragraph_format.space_before = Pt(0)
    p_s1.paragraph_format.space_after = Pt(1)
    add_run_bpmf(p_s1, "✎ 壹、烹飪基本資訊（起：情境與命名）", font_size=11, bold=True, color_rgb=(0,0,0))
    
    s1_items = [
        "1. 時間與地點：我們在 ＿＿＿＿＿＿（時間），在 ＿＿＿＿＿＿（地點）一\U000e01e2起做\U000e01e1料理。",
        "2. 合作小夥伴：這次我是和\U000e01e1 ＿＿＿＿＿＿＿＿＿＿＿（家人）一\U000e01e2起合作。",
        "3. 料理大名：我們要做的料理是：【 ＿＿＿＿＿＿＿＿＿＿＿＿＿＿ 】。",
        "4. 創意美食名（想像力命名）：我幫它取名叫「 ＿＿＿＿＿＿＿＿＿＿ 」！"
    ]
    for it in s1_items:
        p = cell_left.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = Pt(13.5)
        add_run_bpmf(p, it, font_size=9, bold=False, color_rgb=(30,30,30))

    # [SECTION 2: 貳、事前食材準備]
    p_s2 = cell_left.add_paragraph()
    p_s2.paragraph_format.space_before = Pt(4)
    p_s2.paragraph_format.space_after = Pt(1)
    add_run_bpmf(p_s2, "📋 貳、事前食材準備（承：材料點點名）", font_size=11, bold=True, color_rgb=(0,0,0))
    
    s2_items = [
        "動手做\U000e01e1之前，我們準備了新鮮食材與實用工具：",
        "• 主要食材：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿",
        "• 調味料與工具：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿"
    ]
    for it in s2_items:
        p = cell_left.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = Pt(13.5)
        add_run_bpmf(p, it, font_size=9, bold=False, color_rgb=(30,30,30))

    # [SECTION 4: 肆、過程趣事紀錄]
    p_s4 = cell_left.add_paragraph()
    p_s4.paragraph_format.space_before = Pt(4)
    p_s4.paragraph_format.space_after = Pt(1)
    add_run_bpmf(p_s4, "📷 肆、過程趣事紀錄（轉：互動小插曲）", font_size=11, bold=True, color_rgb=(0,0,0))
    
    p_s4_q = cell_left.add_paragraph()
    p_s4_q.paragraph_format.space_before = Pt(0)
    p_s4_q.paragraph_format.space_after = Pt(1)
    p_s4_q.paragraph_format.line_spacing = Pt(13.5)
    add_run_bpmf(p_s4_q, "在和\U000e01e1家人一\U000e01e2起料理時，有發生什麼特別、手忙腳亂或好笑的事嗎？", font_size=9, bold=False, color_rgb=(30,30,30))
    
    for _ in range(2):
        p_line = cell_left.add_paragraph()
        p_line.paragraph_format.space_before = Pt(0)
        p_line.paragraph_format.space_after = Pt(1)
        p_line.paragraph_format.line_spacing = Pt(15)
        add_run_bpmf(p_line, "＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", font_size=9, bold=False, color_rgb=(60,60,60))

    # [SECTION 5: 伍、品嘗與心得感受]
    p_s5 = cell_left.add_paragraph()
    p_s5.paragraph_format.space_before = Pt(4)
    p_s5.paragraph_format.space_after = Pt(1)
    add_run_bpmf(p_s5, "😋 伍、品嘗與心得感受（合：色香味與心情）", font_size=11, bold=True, color_rgb=(0,0,0))
    
    s5_items = [
        "美味上桌囉！請寫下品嘗料理時的五官感受：",
        "1. 【色】看著外觀：這道菜看起來 ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿。",
        "2. 【香】聞著香氣：剛起鍋時聞起來 ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿。",
        "3. 【味】嘗嘗滋味：吃進嘴裡感覺 ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿。",
        "4. 【心】共享心情：能和\U000e01e1家人一\U000e01e2起動手做\U000e01e1料理，我覺得\U000e01e1 ＿＿＿＿＿＿＿＿，",
        "   因為 ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿。"
    ]
    for it in s5_items:
        p = cell_left.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = Pt(13.5)
        add_run_bpmf(p, it, font_size=9, bold=False, color_rgb=(30,30,30))

    # -------------------- RIGHT COLUMN (9.6 cm) --------------------
    cell_right = main_table.cell(0, 1)
    cell_right.width = Cm(9.6)
    set_cell_margins(cell_right, top=30, bottom=30, left=60, right=40)
    set_cell_borders(cell_right)

    # [SECTION 3: 參、步驟大公開]
    p_s3 = cell_right.paragraphs[0]
    p_s3.paragraph_format.space_before = Pt(0)
    p_s3.paragraph_format.space_after = Pt(1)
    add_run_bpmf(p_s3, "🍳 參、步驟大公開（承：烹飪過程與句型）", font_size=11, bold=True, color_rgb=(0,0,0))
    
    p_s3_sub = cell_right.add_paragraph()
    p_s3_sub.paragraph_format.space_before = Pt(0)
    p_s3_sub.paragraph_format.space_after = Pt(1)
    add_run_bpmf(p_s3_sub, "請用順序連接詞，寫下你們製作這道料理的詳細步驟：", font_size=9, bold=False, color_rgb=(50,50,50))
    
    steps = [
        "① 我先： ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿",
        "② 再： ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿",
        "③ 接著： ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿",
        "④ 然後： ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿",
        "⑤ 最後： ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿"
    ]
    for st in steps:
        p = cell_right.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = Pt(14)
        add_run_bpmf(p, st, font_size=9, bold=False, color_rgb=(30,30,30))

    # [句型小達人 加分區]
    p_tips = cell_right.add_paragraph()
    p_tips.paragraph_format.space_before = Pt(3)
    p_tips.paragraph_format.space_after = Pt(1)
    add_run_bpmf(p_tips, "💡 句型小達人（加分區：運用修辭造句）", font_size=10, bold=True, color_rgb=(0,0,0))
    
    patterns = [
        "★ 【看起來】：料理在製作過程中，＿＿＿＿＿＿＿＿＿＿＿＿，\n   看起來 ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿。",
        "★ 【就像】：完成後的樣貌，繽紛的色彩 就像 ＿＿＿＿＿＿＿＿＿＿\n   ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿。"
    ]
    for pt in patterns:
        p = cell_right.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = Pt(13)
        add_run_bpmf(p, pt, font_size=8.5, bold=False, color_rgb=(40,40,40))

    # [SECTION 6: 陸、美食小畫廊（成果展示）]
    p_s6 = cell_right.add_paragraph()
    p_s6.paragraph_format.space_before = Pt(4)
    p_s6.paragraph_format.space_after = Pt(1)
    add_run_bpmf(p_s6, "🎨 陸、美食小畫廊（定格美味 ‧ 成果展示）", font_size=11, bold=True, color_rgb=(0,0,0))
    
    # Polaroid Image
    p_polaroid = cell_right.add_paragraph()
    p_polaroid.paragraph_format.space_before = Pt(1)
    p_polaroid.paragraph_format.space_after = Pt(1)
    p_polaroid.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(polaroid_img):
        p_polaroid.add_run().add_picture(polaroid_img, width=Cm(6.8))

    p_pola_desc = cell_right.add_paragraph()
    p_pola_desc.paragraph_format.space_before = Pt(0)
    p_pola_desc.paragraph_format.space_after = Pt(0)
    p_pola_desc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run_bpmf(p_pola_desc, "請在拍立得相框中畫下美味料理，或貼上開心合照喔！", font_size=8.5, bold=False, color_rgb=(60,60,60))

    # Bottom Sketch Footer
    p_foot = doc.add_paragraph()
    p_foot.paragraph_format.space_before = Pt(2)
    p_foot.paragraph_format.space_after = Pt(0)
    p_foot.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run_bpmf(p_foot, "✎ 小小主廚隨筆：動手做\U000e01e1料理真有趣！記得寫完請大聲朗讀一遍自己的美食筆記喔！ ✨", font_size=8.5, bold=True, color_rgb=(50,50,50))

    doc.save(output_docx)
    print(f"Generated: {output_docx}")

if __name__ == '__main__':
    target_docx = r"D:\OneDrive\萍\115.二上\塗鴉簿\一起做OO\一起做OO_黑白塗鴉填空學習單.docx"
    build_doodle_worksheet(target_docx)
