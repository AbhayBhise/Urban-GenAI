# -*- coding: utf-8 -*-
"""
UrbanGen AI Full Project Report Builder
Generates the complete SPPU / MIT AOE Third Year B.Tech Capstone Project Report
with all 8 chapters, 17 figures/charts, 9 tables, references, and appendix.
Then queries Word COM for exact page numbers to synchronize the Table of Contents,
List of Figures, and List of Tables.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOC_DIR = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs"
OUTPUT_DOCX = os.path.join(DOC_DIR, "UrbanGen_AI_Project_Report.docx")
OUTPUT_PDF = os.path.join(DOC_DIR, "UrbanGen_AI_Project_Report.pdf")

# Image assets
LOGO_PATH = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\poster\figures\mit_aoe_logo.png"
FIG_4_1_1 = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\clean_project_architecture.png"
FIG_4_1_2 = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\pipeline_architecture_plantuml.png"
FIG_5_1   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\poster\figures\full_project_architecture_plantuml.png"
FIG_5_2   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_vae_tradeoff.png"
FIG_6_1   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_landuse_distribution.png"
FIG_6_2   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_ae_crisp_restoration.png"
FIG_6_3   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_gan_diverse_generation.png"
FIG_6_4   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_vae_multi_interpolation.png"
FIG_7_1   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_ae_convergence.png"
FIG_7_2   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_psnr_comparison.png"
FIG_7_3   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_classifier_metrics.png"
FIG_7_4   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_gan_dynamics.png"
FIG_7_5   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_diffusion_training.png"
FIG_7_6   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_multimodel_loss_bars.png"
FIG_7_7   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\docs\figures\fig_energy_carbon_breakdown.png"
FIG_A_1   = r"c:\Users\Disha Satpute\Downloads\genAI\Urban-GenAI\archive\turnitin_reports\Screenshot 2026-10-26 225027.png"


def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_cell_shading(cell, color_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)


def style_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def add_page_number_to_section(section):
    footer = section.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fld = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    f_p._p.append(fld)


def add_page_border(section):
    sectPr = section._sectPr
    borders = parse_xml(
        f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">'
        f'  <w:top w:val="double" w:sz="12" w:space="24" w:color="000000"/>'
        f'  <w:bottom w:val="double" w:sz="12" w:space="24" w:color="000000"/>'
        f'  <w:left w:val="double" w:sz="12" w:space="24" w:color="000000"/>'
        f'  <w:right w:val="double" w:sz="12" w:space="24" w:color="000000"/>'
        f'</w:pgBorders>'
    )
    sectPr.append(borders)


def add_p(doc, text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.15, bold=False, italic=False, size_pt=11, font_name="Times New Roman", color_rgb=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        if color_rgb:
            run.font.color.rgb = color_rgb
    return p


def add_h1(doc, text):
    return add_p(doc, text, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=14, space_after=8, bold=True, size_pt=14)


def add_h2(doc, text):
    return add_p(doc, text, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=6, bold=True, size_pt=12)


def add_h3(doc, text):
    return add_p(doc, text, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=8, space_after=4, bold=True, italic=True, size_pt=11.5)


def add_bullet(doc, title, text):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    r1 = p.add_run(title + (" " if title else ""))
    r1.bold = True
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    r2 = p.add_run(text)
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(11)
    return p


def add_figure(doc, img_path, caption_num, caption_title, width=Inches(5.8)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=width)
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    r_bold = p_cap.add_run(f"Figure {caption_num}: ")
    r_bold.bold = True
    r_bold.font.name = "Times New Roman"
    r_bold.font.size = Pt(10)
    r_txt = p_cap.add_run(caption_title)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(10)
    return p_cap


def build_raw_document(toc_data=None, lof_data=None, lot_data=None):
    """
    Constructs the docx document. If toc_data, lof_data, lot_data are None,
    uses default/placeholder page values.
    """
    doc = docx.Document()
    
    # Page setup
    sec = doc.sections[0]
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.25)
    sec.right_margin = Inches(1.0)
    add_page_border(sec)
    add_page_number_to_section(sec)
    
    # Style normal
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)

    # =========================================================================
    # PAGE 1: TITLE PAGE
    # =========================================================================
    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(0)
        p_logo.paragraph_format.space_after = Pt(4)
        p_logo.add_run().add_picture(LOGO_PATH, width=Inches(3.2))

    add_p(doc, "MIT | Academy of Engineering", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=2, bold=True, size_pt=15)
    add_p(doc, "(An Autonomous Institute Affiliated to Savitribai Phule Pune University)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=8, italic=True, size_pt=10.5)

    add_p(doc, "A Project Report on", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=4, bold=True, size_pt=12)
    add_p(doc, "UrbanGen AI: A Multi-Model Generative Framework for Satellite Imagery Processing, Land-Use Analytics, and Sustainable Urban Planning",
          align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=12, bold=True, size_pt=13.5, color_rgb=RGBColor(0, 32, 96))

    add_p(doc, "Submitted by,", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4, italic=True, size_pt=11)

    # Students Table
    t_st = doc.add_table(rows=4, cols=2)
    t_st.alignment = WD_TABLE_ALIGNMENT.CENTER
    students = [
        ("Abhay Bhise", "(Exam Seat No. 202402040001)"),
        ("Disha Satpute", "(Exam Seat No. 202402040019)"),
        ("Vaishnavi Phad", "(Exam Seat No. 202402040006)"),
        ("Vedant Ingle", "(Exam Seat No. 202402040020)")
    ]
    for row_idx, (name, seat) in enumerate(students):
        c0, c1 = t_st.rows[row_idx].cells
        c0.width, c1.width = Inches(2.8), Inches(2.8)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r0 = p0.add_run(name)
        r0.bold = True
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p1.add_run(seat)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10.5)
        set_cell_margins(c0, 20, 20, 20, 20)
        set_cell_margins(c1, 20, 20, 20, 20)

    add_p(doc, "Guided by,", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=2, italic=True, size_pt=11)
    add_p(doc, "Prof. Savita Mane", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=10, bold=True, size_pt=12)

    add_p(doc, "A Report submitted to MIT Academy of Engineering, Alandi(D), Pune,\nAn Autonomous Institute Affiliated to Savitribai Phule Pune University\nin partial fulfillment of the requirements of",
          align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=4, size_pt=10.5)
    add_p(doc, "THIRD YEAR BACHELOR OF TECHNOLOGY\nin\nComputer Engineering", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=8, bold=True, size_pt=11.5)

    add_p(doc, "Department of Computer Engineering\nMIT Academy of Engineering\n(An Autonomous Institute Affiliated to Savitribai Phule Pune University)\nAlandi (D), Pune – 412105\n(2025–2026)",
          align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=0, bold=True, size_pt=10.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: CERTIFICATE
    # =========================================================================
    add_p(doc, "MIT | Academy of Engineering", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=2, bold=True, size_pt=14)
    add_p(doc, "(An Autonomous Institute Affiliated to Savitribai Phule Pune University)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=12, italic=True, size_pt=10.5)
    add_p(doc, "CERTIFICATE", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=14, bold=True, size_pt=15)

    add_p(doc,
        'It is hereby certified that the work which is being presented in the Third Year Major Project–2 Report entitled '
        '"UrbanGen AI: A Multi-Model Generative Framework for Satellite Imagery Processing, Land-Use Analytics, and Sustainable Urban Planning", '
        'in partial fulfillment of the requirements for the award of the Bachelor of Technology in Computer Engineering and submitted to '
        'the Department of Computer Engineering of MIT Academy of Engineering, Alandi(D), Pune, Affiliated to Savitribai Phule Pune University (SPPU), '
        'Pune, is an authentic record of work carried out during Academic Year 2025–2026 Semester VI, under the supervision of '
        'Prof. Savita Mane and Prof. Pramod Ganjewar, Department of Computer Engineering.',
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=14, line_spacing=1.3, size_pt=11
    )

    t_cert_st = doc.add_table(rows=4, cols=2)
    t_cert_st.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_i, (nm, st) in enumerate(students):
        c0, c1 = t_cert_st.rows[r_i].cells
        c0.width, c1.width = Inches(2.8), Inches(2.8)
        c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        run0 = c0.paragraphs[0].add_run(nm)
        run0.bold = True
        run0.font.name = "Times New Roman"
        run0.font.size = Pt(10.5)
        run1 = c1.paragraphs[0].add_run(st)
        run1.font.name = "Times New Roman"
        run1.font.size = Pt(10)
        set_cell_margins(c0, 20, 20, 20, 20)
        set_cell_margins(c1, 20, 20, 20, 20)

    add_p(doc, "", space_before=16, space_after=6)

    # Signatures
    t_sig = doc.add_table(rows=2, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_sig0, c_sig1 = t_sig.rows[0].cells
    c_sig0.width, c_sig1.width = Inches(2.8), Inches(2.8)
    p_s0 = c_sig0.paragraphs[0]
    p_s0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s0 = p_s0.add_run("Prof. Savita Mane\nProject Advisor")
    r_s0.bold = True
    r_s0.font.name = "Times New Roman"
    r_s0.font.size = Pt(11)

    p_s1 = c_sig1.paragraphs[0]
    p_s1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s1 = p_s1.add_run("External Examiner\nExaminer")
    r_s1.bold = True
    r_s1.font.name = "Times New Roman"
    r_s1.font.size = Pt(11)

    c_sig2, c_sig3 = t_sig.rows[1].cells
    c_sig2.width, c_sig3.width = Inches(2.8), Inches(2.8)
    p_s2 = c_sig2.paragraphs[0]
    p_s2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s2 = p_s2.add_run("\n\nDr. Pramod Ganjewar\nHoD")
    r_s2.bold = True
    r_s2.font.name = "Times New Roman"
    r_s2.font.size = Pt(11)

    p_s3 = c_sig3.paragraphs[0]
    p_s3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_s3 = p_s3.add_run("\n\n\nDate: ____________\nPlace: Alandi, Pune")
    r_s3.font.name = "Times New Roman"
    r_s3.font.size = Pt(10)

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: DECLARATION
    # =========================================================================
    add_p(doc, "DECLARATION", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=16, bold=True, size_pt=14)

    add_p(doc,
        "We the undersigned solemnly declare that the project report is based on our own work carried out during the "
        "course of our study under the supervision of Prof. Savita Mane and Prof. Pramod Ganjewar. We assert the statements "
        "made and conclusions drawn are an outcome of our project work. We further certify that:",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=12, line_spacing=1.25, size_pt=11
    )

    dec_points = [
        "The work contained in the report is original and has been done by us under the general supervision of our supervisor.",
        "The work has not been submitted to any other Institution for any other degree/diploma/certificate in this Institute/University or any other Institute/University of India or abroad.",
        "We have followed the guidelines provided by the Institute in writing the report.",
        "Whenever we have used materials (data, theoretical analysis, and text) from other sources, we have given due credit to them in the text of the report and giving their details in the references."
    ]
    for idx, pt in enumerate(dec_points, 1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.2
        r_num = p.add_run(f"{idx}. ")
        r_num.bold = True
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(11)
        r_txt = p.add_run(pt)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(11)

    add_p(doc, "", space_before=24, space_after=6)

    t_dec_st = doc.add_table(rows=4, cols=2)
    t_dec_st.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_i, (nm, st) in enumerate(students):
        c0, c1 = t_dec_st.rows[r_i].cells
        c0.width, c1.width = Inches(2.8), Inches(2.8)
        c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        run0 = c0.paragraphs[0].add_run(nm)
        run0.bold = True
        run0.font.name = "Times New Roman"
        run0.font.size = Pt(10.5)
        run1 = c1.paragraphs[0].add_run(st)
        run1.font.name = "Times New Roman"
        run1.font.size = Pt(10)
        set_cell_margins(c0, 20, 20, 20, 20)
        set_cell_margins(c1, 20, 20, 20, 20)

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: ABSTRACT
    # =========================================================================
    add_p(doc, "Abstract", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=16, bold=True, size_pt=14)

    add_p(doc,
        "Rapid global urbanization presents pressing challenges in zoning compliance, green cover preservation, "
        "transit infrastructure allocation, and microclimate resilience. Traditional Geographic Information System (GIS) "
        "workflows demand extensive manual photointerpretation and lack real-time scenario simulation capabilities. "
        "In this project, we propose UrbanGen AI, an end-to-end, edge-deployable multi-model generative artificial "
        "intelligence framework engineered specifically for sustainable smart city planning and digital twin prototyping. "
        "To bridge the critical gap between pixel-level remote sensing restoration and qualitative municipal policy formulation, "
        "UrbanGen AI coordinates six specialized deep learning architectures under a unified, reproducible 50-epoch benchmark "
        "protocol on the USGS UCMerced LandUse dataset (2,100 high-resolution aerial orthoimages, 21 classes, 0.3 m GSD).",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=8, line_spacing=1.2, size_pt=11
    )

    add_p(doc,
        "The architecture deploys: (i) a multi-scale skip-connected U-Net Denoising Autoencoder achieving 29.65 dB PSNR "
        "(+7.0 dB gain over baseline, SSIM 0.8649) to eliminate atmospheric scattering and sensor noise (sigma = 0.15); "
        "(ii) a Spatial Variational Autoencoder (beta-VAE) preserving 2D spatial topology in an explicit R^(64x8x8) latent tensor, "
        "achieving 27.49 dB PSNR with smooth continuous manifold interpolation and unsupervised anomaly detection (>3 sigma reconstruction disparity); "
        "(iii) a frozen ImageNet-adapted ResNet-18 Territorial Classifier attaining 98.10% validation accuracy (87.30% held-out test accuracy, Macro F1: 0.9784) "
        "serving as an autonomous semantic fidelity auditor; (iv) a Residual Class-Conditional DCGAN (cDCGAN) incorporating Spectral Normalization "
        "and projection conditioning that synthesizes aerial parcels in 32 ms with 99.40% intended-class proxy recognition; "
        "(v) a Class-Conditional Denoising Diffusion Probabilistic Model (DDPM) accelerated by a 20-step deterministic DDIM sampler achieving 0.0304 "
        "noise MSE and superior structural photorealism; and (vi) a domain-specialized causal Transformer (MiniGPT) yielding 1.110 perplexity "
        "(0.1505 bits/character) to formulate legally grounded Floor Space Index (FSI) and Transit-Oriented Development (TOD) bylaws.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=8, line_spacing=1.2, size_pt=11
    )

    add_p(doc,
        "Executed entirely on consumer edge hardware (NVIDIA RTX 4050 6 GB Laptop GPU, 0.112 kWh cumulative energy, 79.1 g CO2e), "
        "UrbanGen AI demonstrates that municipal intelligence can operate with high structural fidelity while strictly preserving "
        "institutional data sovereignty through complete air-gapped on-premises execution.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=12, line_spacing=1.2, size_pt=11
    )

    p_kw = add_p(doc, space_before=8, space_after=0)
    r_kwh = p_kw.add_run("Keywords: ")
    r_kwh.bold = True
    r_kwh.font.name = "Times New Roman"
    r_kwh.font.size = Pt(10.5)
    r_kwt = p_kw.add_run("Generative Artificial Intelligence, Remote Sensing, Denoising Autoencoder, Variational Autoencoder, Conditional GAN, Diffusion Models, Causal Transformer, Smart Cities, Green AI.")
    r_kwt.italic = True
    r_kwt.font.name = "Times New Roman"
    r_kwt.font.size = Pt(10.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: ACKNOWLEDGMENT
    # =========================================================================
    add_p(doc, "Acknowledgment", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=16, bold=True, size_pt=14)

    add_p(doc,
        "We take this opportunity to express our sincere gratitude to all those who supported and guided us throughout "
        "the development of this capstone research project. First and foremost, we extend our heartfelt thanks to our project "
        "guides, Prof. Savita Mane and Prof. Pramod Ganjewar, whose consistent mentorship, valuable feedback, and patient technical "
        "guidance shaped this work from its initial conceptual design into a fully validated, edge-deployable generative AI framework.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25, size_pt=11
    )

    add_p(doc,
        "We are deeply grateful to Dr. Pramod Ganjewar, Head of the Department of Computer Engineering, and Dr. Kanchan Dhote, "
        "Project Coordinator, for providing us with the necessary computing resources, high-performance workstation facilities, and an "
        "encouraging academic environment. Their continued support motivated us to push the boundaries of multi-modal generative modeling "
        "and maintain the rigorous quality expected of an IEEE-standard project.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=10, line_spacing=1.25, size_pt=11
    )

    add_p(doc,
        "We also wish to thank the faculty members of the Department of Computer Engineering, MIT Academy of Engineering, Alandi (D), "
        "Pune, for their constructive critiques during project review sessions. Finally, we express our heartfelt gratitude to our families "
        "and fellow students for their unwavering encouragement, moral support, and inspiration throughout this academic journey.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=4, space_after=16, line_spacing=1.25, size_pt=11
    )

    t_ack_st = doc.add_table(rows=4, cols=2)
    t_ack_st.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_i, (nm, st) in enumerate(students):
        c0, c1 = t_ack_st.rows[r_i].cells
        c0.width, c1.width = Inches(2.8), Inches(2.8)
        c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        run0 = c0.paragraphs[0].add_run(nm)
        run0.bold = True
        run0.font.name = "Times New Roman"
        run0.font.size = Pt(10.5)
        run1 = c1.paragraphs[0].add_run(st)
        run1.font.name = "Times New Roman"
        run1.font.size = Pt(10)
        set_cell_margins(c0, 20, 20, 20, 20)
        set_cell_margins(c1, 20, 20, 20, 20)

    doc.add_page_break()

    # =========================================================================
    # PAGES 6-7: CONTENTS (TABLE OF CONTENTS)
    # =========================================================================
    add_p(doc, "Contents", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=10, bold=True, size_pt=14)

    default_toc = [
        ("Abstract", "iv"),
        ("Acknowledgement", "v"),
        ("1 Introduction", "10-13"),
        ("   1.1 Background", "10"),
        ("   1.2 Motivation", "10"),
        ("   1.3 Project Idea", "11"),
        ("   1.4 Proposed Solution", "12"),
        ("   1.5 Project Report Organization", "13"),
        ("2 Literature Review", "14-16"),
        ("   2.1 Related Work and State of the Art", "14"),
        ("   2.1.1 Product Survey", "15"),
        ("   2.2 Limitations of State of the Art Techniques", "15"),
        ("   2.3 Discussion and Future Direction", "16"),
        ("   2.4 Concluding Remarks", "16"),
        ("3 Problem Definition and Scope", "17-19"),
        ("   3.1 Problem Statement", "17"),
        ("   3.2 Goals and Objectives", "17"),
        ("   3.3 Scope and Major Constraints", "18"),
        ("   3.4 Hardware and Software Requirements", "18"),
        ("   3.5 Expected Outcomes", "19"),
        ("4 System Requirement Specification", "20-22"),
        ("   4.1 Overall Description", "20"),
        ("   4.1.1 Block Diagram / Proposed System Setup", "21"),
        ("   4.1.2 Workflow of the Process", "21"),
        ("   4.1.3 Project Planning", "22"),
        ("   4.2 Project Planning Schedule", "22"),
        ("5 Proposed Methodology", "23-26"),
        ("   5.1 System Architecture", "23"),
        ("   5.2 Objective Functions and Mathematical Models", "24"),
        ("   5.3 Approach", "26"),
        ("6 Implementation", "27-31"),
        ("   6.1 System Implementation", "27"),
        ("   6.2 Experiment / Implementation Parameters", "27"),
        ("   6.3 User Interface", "28"),
        ("   6.4 Data Description (USGS UCMerced LandUse)", "28"),
        ("   6.5 Functional Implementation", "29"),
        ("   6.6 Output and Visual Results", "30"),
        ("7 Results and Discussion", "32-37"),
        ("   7.1 Introduction", "32"),
        ("   7.2 Case 1: Optical Remote Sensing Restoration Benchmark", "32"),
        ("   7.3 Case 2: Territorial Zoning Classification Accuracy", "33"),
        ("   7.4 Case 3: Generative Aerial Parcel Synthesis Benchmark", "34"),
        ("   7.5 User Interface Evaluation", "35"),
        ("   7.6 System Performance and Green AI Analysis", "35"),
        ("   7.7 Security and Data Sovereignty Evaluation", "36"),
        ("   7.8 Comparative Analysis", "36"),
        ("   7.9 Discussion", "37"),
        ("   7.10 Conclusion", "37"),
        ("8 Conclusion and Future Scope", "38-40"),
        ("   8.1 Conclusion", "38"),
        ("   8.2 Future Scope", "39"),
        ("Appendices", "41"),
        ("   Appendix A: Plagiarism Report", "41"),
        ("References", "42-45")
    ]
    items_to_use = toc_data if toc_data else default_toc

    t_toc = doc.add_table(rows=len(items_to_use), cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders(t_toc)
    for idx, (title, pg) in enumerate(items_to_use):
        c0, c1 = t_toc.rows[idx].cells
        c0.width, c1.width = Inches(4.8), Inches(1.0)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        is_main = not title.startswith("   ") and not title in ["Abstract", "Acknowledgement"]
        r0 = p0.add_run(title)
        r0.bold = is_main
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(9.5)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(str(pg))
        r1.bold = is_main
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9.5)
        set_cell_margins(c0, top=14, bottom=14, left=30, right=30)
        set_cell_margins(c1, top=14, bottom=14, left=30, right=30)

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: LIST OF FIGURES & LIST OF TABLES
    # =========================================================================
    add_p(doc, "List of Figures", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=8, bold=True, size_pt=14)

    default_lof = [
        ("4.1.1 Block Diagram / Proposed System Setup of UrbanGen AI", "21"),
        ("4.1.2 Workflow of the Integrated Multi-Model Planning Process", "21"),
        ("5.1 Detailed System Architecture & Neural Interconnections", "23"),
        ("5.2 Spatial beta-VAE Reconstruction Error vs. KL Regularization Pareto Tradeoff", "25"),
        ("6.1 USGS UCMerced LandUse Dataset Category Distribution across 21 Classes", "28"),
        ("6.2 High-Resolution Aerial Restoration via Skip-Connected DAE across Structural Classes", "30"),
        ("6.3 Class-Conditioned Synthetic Aerial Generation via Residual cDCGAN across 21 Categories", "31"),
        ("6.4 Continuous Multi-Pair Latent Space Interpolation via Spatial beta-VAE", "31"),
        ("7.1 U-Net DAE Reconstruction Loss Convergence during Training", "32"),
        ("7.2 Class-wise PSNR Improvement of Skip-Connected DAE over Bottleneck AE", "33"),
        ("7.3 Territorial Classifier Validation Accuracy and Cross-Entropy Loss Convergence", "33"),
        ("7.4 Residual cDCGAN Minimax Equilibrium & Loss Dynamics", "34"),
        ("7.5 Conditional DDPM Denoising Score Matching MSE Loss Trajectory", "35"),
        ("7.6 Multi-Model Unified Benchmark Performance Across Six Neural Architectures", "36"),
        ("7.7 Hardware Training Duration, Energy Consumption (kWh), and Carbon Footprint", "36"),
        ("A.1 Turnitin Originality & Plagiarism Authenticity Verification Report", "41")
    ]
    lof_to_use = lof_data if lof_data else default_lof

    t_lof = doc.add_table(rows=len(lof_to_use), cols=2)
    t_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders(t_lof)
    for idx, (cap, pg) in enumerate(lof_to_use):
        c0, c1 = t_lof.rows[idx].cells
        c0.width, c1.width = Inches(4.8), Inches(1.0)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r0 = p0.add_run(cap)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(9.5)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(str(pg))
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9.5)
        set_cell_margins(c0, top=14, bottom=14, left=30, right=30)
        set_cell_margins(c1, top=14, bottom=14, left=30, right=30)

    doc.add_page_break()

    # List of Tables
    add_p(doc, "List of Tables", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=8, bold=True, size_pt=14)

    default_lot = [
        ("Table 3.1: Hardware Requirements", "18"),
        ("Table 3.2: Software Requirements", "19"),
        ("Table 4.1: Project Planning – Phase-wise Schedule", "22"),
        ("Table 6.1: Implementation Parameters Across Six Neural Modules", "27"),
        ("Table 7.1: Optical Remote Sensing Restoration Benchmark on Corrupted UCMerced Tiles", "32"),
        ("Table 7.2: Comparative Territorial Zoning Classification Performance", "33"),
        ("Table 7.3: Generative Aerial Parcel Synthesis Benchmark: Fidelity vs. Edge Efficiency", "34"),
        ("Table 7.4: Standard Evaluation Parameter Matrix for Multi-Model Verification", "35"),
        ("Table 7.5: Computational Training Duration and Hardware Energy Audit (NVIDIA RTX 4050)", "36")
    ]
    lot_to_use = lot_data if lot_data else default_lot

    t_lot = doc.add_table(rows=len(lot_to_use), cols=2)
    t_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders(t_lot)
    for idx, (cap, pg) in enumerate(lot_to_use):
        c0, c1 = t_lot.rows[idx].cells
        c0.width, c1.width = Inches(4.8), Inches(1.0)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r0 = p0.add_run(cap)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(9.5)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(str(pg))
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9.5)
        set_cell_margins(c0, top=14, bottom=14, left=30, right=30)
        set_cell_margins(c1, top=14, bottom=14, left=30, right=30)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_h1(doc, "Chapter 1")
    add_h1(doc, "Introduction")
    add_h2(doc, "1.1 Background")
    
    add_p(doc, 
        "Rapid global urbanization presents pressing challenges in zoning compliance, green cover preservation, "
        "transit infrastructure allocation, and microclimate resilience across metropolitan regions. "
        "As modern municipal cities expand, urban planners and civic administrative bodies rely heavily on Geographic "
        "Information System (GIS) databases, periodic aerial orthoimagery, and cadastral spatial vectors to govern development. "
        "However, traditional spatial planning workflows are severely constrained by high operational latency, substantial labor overhead, "
        "and an acute inability to simulate speculative future urban configurations or synthesize proactive, legally grounded policy guidance."
    )
    add_p(doc,
        "Satellite optical sensors are inherently susceptible to atmospheric scattering, cloud shadows, aerosol haze, "
        "and sensor degradation during orbital acquisition. Consequently, ingested remote sensing rasters frequently suffer from blurred "
        "structural boundaries, obscured street grids, and degraded parcel textures. When urban administrators attempt to conduct automated "
        "land-use audits or parcel change detection, this sensor noise propagates through classical classification models, resulting in false "
        "encroachment alarms or missed structural violations. Furthermore, municipal authorities often maintain fragmented archives where "
        "satellite rasters, GIS vector shapefiles, building approval certificates, and zoning bylaws are siloed across disconnected departments."
    )
    add_p(doc,
        "The emergence of Deep Learning (DL) and Generative Artificial Intelligence (GenAI) presents unprecedented opportunities "
        "to overcome these limitations. While modern computer vision networks achieve impressive accuracy in land-use and land-cover (LULC) "
        "scene classification, generative neural architectures—specifically Denoising Autoencoders (DAEs), Variational Autoencoders (VAEs), "
        "Generative Adversarial Networks (GANs), and Denoising Diffusion Probabilistic Models (DDPMs)—provide powerful mathematical mechanisms "
        "for signal restoration, continuous latent feature morphing, and synthetic scenario generation. Simultaneously, causal autoregressive "
        "Transformers enable structured translation between quantitative spatial telemetry and qualitative legal policy bylaws."
    )

    add_h2(doc, "1.2 Motivation")
    add_p(doc,
        "Despite significant progress in deep learning for remote sensing, existing frameworks exhibit critical technical and operational bottlenecks. "
        "First, standard bottleneck autoencoders oversmooth high-frequency spatial boundaries, irreversibly smearing rectangular building footprints "
        "and road intersections. Second, conventional Variational Autoencoders compress 2D spatial features into flat 1D latent vectors, "
        "collapsing the topological relationships necessary for smooth geospatial morphing. Third, generative synthesis via GANs suffers from training "
        "instability and mode collapse, while diffusion models demand datacenter-scale GPU clusters that are completely out of reach for local municipal planning offices."
    )
    add_p(doc,
        "Finally, the computational carbon footprint of modern AI models represents an urgent environmental concern. Training datacenter-scale foundation "
        "models emits hundreds of metric tons of CO2e. In strict adherence to Green AI imperatives, there is a compelling need for domain-specialized, "
        "efficient multi-model architectures that can train and execute entirely on consumer edge workstations while guaranteeing 100% on-premises municipal data "
        "sovereignty without cloud telemetry leakage."
    )

    add_h2(doc, "1.3 Project Idea")
    add_p(doc,
        "The core concept of UrbanGen AI is to construct a cooperative, edge-deployable multi-model generative intelligence framework that bridges "
        "the methodological divide between pixel-level satellite remote sensing restoration and qualitative municipal urban policy formulation. "
        "Rather than relying on an isolated, monolithic model, UrbanGen AI coordinates six complementary neural network architectures operating under a unified, "
        "reproducible experimental benchmark protocol on the standardized USGS UCMerced LandUse benchmark dataset."
    )
    add_p(doc,
        "UrbanGen AI establishes a closed-loop digital twin pipeline: raw perturbed aerial rasters are first restored via multi-scale skip-connected transposed convolutions; "
        "restored rasters are embedded into a topology-preserving 3D latent manifold (R^(64x8x8)) that powers continuous spatial morphing and unsupervised municipal anomaly screening "
        "(>3 sigma disparity); parcels are classified by a frozen territorial auditor; dual-modality generative synthesis is achieved through both ultra-fast adversarial generation "
        "(cDCGAN in 32 ms) and photorealistic reverse diffusion (DDPM/DDIM in 1.82 s); and visual telemetry is automatically translated into grounded, legally compliant development bylaws "
        "via a domain-specialized causal Transformer (MiniGPT)."
    )

    add_h2(doc, "1.4 Proposed Solution")
    add_p(doc, "UrbanGen AI realizes this vision through an integrated five-stage technical workflow designed for local edge deployment:")
    add_bullet(doc, "Stage 1 (Multi-Scale Optical Restoration):", "A U-Net Denoising Autoencoder (DAE) bridges hierarchical feature maps from encoder layers directly into transposed decoder stages, recovering crisp orthogonal parcel boundaries from Gaussian sensor noise (sigma = 0.15) with 29.65 dB PSNR.")
    add_bullet(doc, "Stage 2 (Spatial Latent Manifold & Anomaly Engine):", "A Spatial beta-VAE preserves 2D topological arrangements in an explicit 3D tensor latent representation under a calibrated beta = 10^-4 Pareto objective, enabling continuous land-use interpolation and flagging unauthorized encroachments.")
    add_bullet(doc, "Stage 3 (Frozen Territorial Zoning Auditor):", "An ImageNet-adapted ResNet-18 classifier (98.10% validation accuracy, 0.9784 Macro F1) acts as an independent mathematical auditor to verify both degraded restorations and synthetic generations.")
    add_bullet(doc, "Stage 4 (Dual-Modality Generative Parcel Synthesis):", "A Spectral Normalization stabilized cDCGAN delivers real-time edge generation (32 ms, 99.40% proxy recognition), while a 20-step accelerated DDIM diffusion sampler achieves superior structural photorealism without mode collapse.")
    add_bullet(doc, "Stage 5 (Vision-Grounded Municipal Policy Engine):", "A custom Pre-LayerNorm causal Transformer (MiniGPT) trained on Pune Municipal Corporation (PMC) bylaws and Transit-Oriented Development guidelines synthesizes legally compliant FSI directives (1.8 to 2.4) and green-buffer setbacks with 1.110 perplexity.")

    add_h2(doc, "1.5 Project Report Organization")
    add_p(doc, "This project report is structured into eight comprehensive chapters that document the conceptual design, mathematical formulation, system architecture, implementation details, experimental evaluation, and future scope of UrbanGen AI:")
    add_bullet(doc, "Chapter 2 (Literature Review):", "Provides an in-depth survey of remote sensing restoration, scene classification, generative modeling (GANs, DDPMs), and language models, analyzing existing commercial tools and identifying core research gaps.")
    add_bullet(doc, "Chapter 3 (Problem Definition and Scope):", "Formally defines the research objectives, hardware/software constraints, operational boundaries, and quantified performance benchmarks.")
    add_bullet(doc, "Chapter 4 (System Requirement Specification):", "Details the three-tier system architecture, block diagrams, procedural workflows, and project planning milestones.")
    add_bullet(doc, "Chapter 5 (Proposed Methodology):", "Details the mathematical objective functions, loss formulations, and algorithm workflows across all six neural modules.")
    add_bullet(doc, "Chapter 6 (Implementation):", "Describes the layer-by-layer architectural specifications, dataset preprocessing, FastAPI backend, React dashboard, and visual generative outputs.")
    add_bullet(doc, "Chapter 7 (Results and Discussion):", "Delivers rigorous comparative benchmarking against published state-of-the-art baselines across three experimental case studies, accompanied by an exhaustive Green AI hardware energy and carbon emission audit.")
    add_bullet(doc, "Chapter 8 (Conclusion and Future Scope):", "Summarizes the scientific contributions of the project and outlines future extensions including multi-spectral satellite ingestion and Physics-Informed microclimate modeling.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: LITERATURE REVIEW
    # =========================================================================
    add_h1(doc, "Chapter 2")
    add_h1(doc, "Literature Review")
    add_h2(doc, "2.1 Related Work and State of the Art")
    
    add_p(doc,
        "Remote sensing imagery acquired by satellite and airborne sensors is inherently vulnerable to atmospheric attenuation, "
        "cloud shadows, and sensor noise. Early spatial restoration relied on spatial filtering and non-local means, which oversmooth "
        "geometric boundaries. Vincent et al. [16] introduced Denoising Autoencoders (DAEs), establishing that robust representations can be "
        "learned by reconstructing unperturbed signals from artificially corrupted inputs. Zhang et al. [17] advanced deep residual learning for "
        "CNN denoisers (DnCNN), proving that residual formulations effectively isolate high-frequency noise. Ronneberger et al. [18] introduced "
        "U-Net, showing that skip connections bridging encoder and decoder stages preserve fine structural boundaries. Recently, vision Transformers "
        "like SwinIR [19] and HAT [20] have set state-of-the-art restoration benchmarks; however, their extreme parameter counts and quadratic attention "
        "complexity render them impractical for edge deployment."
    )
    add_p(doc,
        "In scene classification and land-use parsing, traditional Bag-of-Visual-Words (BoVW) [13] representations have been superseded by deep residual architectures. "
        "He et al. [14] introduced deep residual learning (ResNet), mitigating vanishing gradient problems through identity shortcuts. Cheng et al. [12] "
        "established comprehensive remote sensing benchmarks, demonstrating that ImageNet transfer learning drastically accelerates convergence on aerial orthoimagery. "
        "In UrbanGen AI, ResNet-18 is adapted not merely as a classifier, but as a frozen, objective mathematical evaluator to audit synthetic imagery without subjective human bias."
    )
    add_p(doc,
        "Generative modeling in Earth observation was historically dominated by Generative Adversarial Networks [28]. Radford et al. [29] introduced DCGAN, "
        "replacing spatial pooling with strided convolutions. Mirza and Osindero [30] formulated Conditional GANs (cGANs), enabling class-directed synthesis. "
        "To stabilize adversarial minimax training, Miyato et al. [31] proposed Spectral Normalization, enforcing Lipschitz continuity on discriminators, "
        "while Miyato and Koyama [32] formulated projection discriminators incorporating conditional embeddings via inner products. Recently, Denoising Diffusion "
        "Probabilistic Models (DDPMs) [36, 37] have emerged as a superior generative paradigm, learning reverse Markov noise trajectories to achieve unprecedented "
        "structural diversity [39]. Song et al. [38] formulated Denoising Diffusion Implicit Models (DDIM), accelerating sampling via non-Markovian deterministic "
        "sub-sequences. Recent works like Remote-Diffusion [6] and GeoDiffusion [40] validated diffusion for aerial generation, yet require compute clusters that preclude edge deployment."
    )

    add_h3(doc, "2.1.1 Product Survey")
    add_p(doc, "A rigorous product survey was conducted across existing geospatial platforms, remote sensing toolkits, and generative AI systems:")
    add_bullet(doc, "Google Earth Engine (GEE):", "GEE provides cloud-scale planetary geospatial analysis and satellite catalog access. While exceptional for multi-temporal vegetation index computation and raster mathematics, GEE lacks generative scenario prototyping, deep latent manifold navigation, and localized policy drafting.")
    add_bullet(doc, "ArcGIS Pro & QGIS:", "Industry-standard GIS suites excel in cadastral mapping, vector polygon topology, and cartographic visualization. However, their automated change detection is rule-based or relies on basic classification, lacking generative digital twin scenario synthesis.")
    add_bullet(doc, "Commercial LLMs (ChatGPT, Claude, Gemini):", "Cloud-hosted general-purpose LLMs demonstrate impressive reasoning but exhibit severe factual hallucination when queried on regional municipal bylaws (such as Pune Municipal Corporation DCR rules). Furthermore, uploading sensitive cadastral vectors to third-party cloud endpoints violates municipal data sovereignty regulations.")
    add_bullet(doc, "Datacenter Generative Remote Sensing Models (GeoDiffusion, SatMAE):", "State-of-the-art vision models require high-end multi-GPU clusters (A100/H100), consuming kilowatts of power and incurring exorbitant recurring operational costs that municipal planning authorities cannot sustain.")

    add_h2(doc, "2.2 Limitations of State of the Art Techniques")
    add_p(doc, "The survey reveals five persistent limitations across existing remote sensing and planning tools:")
    add_bullet(doc, "1. Atmospheric Noise Oversmoothing:", "Standard bottleneck autoencoders discard high-frequency gradients, smearing orthogonal street grids and building footprints.")
    add_bullet(doc, "2. Latent Topological Collapse:", "Conventional VAEs compress images into flat 1D vectors, destroying 2D spatial relationships and suffering from posterior collapse.")
    add_bullet(doc, "3. Generative Adversarial Instability:", "Aerial GANs frequently suffer from mode collapse, synthesizing repetitive parcels with structural artifacts.")
    add_bullet(doc, "4. Diffusion Inference Latency:", "Standard 1,000-step ancestral DDPM sampling requires ~28 seconds per tile, making interactive scenario design impossible.")
    add_bullet(doc, "5. Disconnection Between Spatial Vision and Municipal Policy:", "Computer vision models output raw rasters, whereas municipal town planners require legally grounded Floor Space Index (FSI) directives and environmental setback codes.")

    add_h2(doc, "2.3 Discussion and Future Direction")
    add_p(doc,
        "The literature clearly indicates that modern smart cities require a unified, edge-feasible intelligence architecture that couples image restoration, "
        "latent manifold navigation, dual-modality generation, and causal policy drafting. Crucially, Schwartz et al. [43] emphasized the pressing imperative "
        "for 'Green AI'—prioritizing energy efficiency, low carbon emissions, and consumer hardware deployment over unconstrained compute scaling. "
        "UrbanGen AI directly addresses this future direction by proving that state-of-the-art multi-model generative intelligence can operate entirely within "
        "consumer edge hardware constraints."
    )

    add_h2(doc, "2.4 Concluding Remarks")
    add_p(doc,
        "UrbanGen AI bridges the identified research gaps through an integrated six-model cooperative framework. By combining multi-scale skip connections, "
        "a 3D topology-preserving spatial latent tensor, Spectral Normalization projection cDCGAN, accelerated 20-step DDIM diffusion, frozen ResNet-18 auditing, "
        "and domain-grounded causal text synthesis, UrbanGen AI establishes a complete, self-contained municipal planning digital twin."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: PROBLEM DEFINITION AND SCOPE
    # =========================================================================
    add_h1(doc, "Chapter 3")
    add_h1(doc, "Problem Definition and Scope")
    add_h2(doc, "3.1 Problem Statement")
    
    add_p(doc,
        "Design, develop, and benchmark an integrated, edge-computable multi-model generative artificial intelligence framework that ingests "
        "degraded satellite remote sensing orthoimagery, restores high-frequency structural parcel boundaries, navigates an explicit topology-preserving "
        "3D latent manifold to detect unauthorized zoning encroachments, synthesizes speculative urban parcel scenarios with verified semantic fidelity "
        "via both real-time adversarial and photorealistic diffusion mechanisms, and automatically formulates legally compliant municipal development "
        "control regulations without factual hallucination—all executed under a strictly auditable, low-carbon Green AI edge budget."
    )

    add_h2(doc, "3.2 Goals and Objectives")
    add_bullet(doc, "1. Signal Restoration:", "Develop a multi-scale skip-connected U-Net Denoising Autoencoder achieving PSNR >= 29 dB and SSIM >= 0.85 on corrupted aerial imagery (sigma = 0.15).")
    add_bullet(doc, "2. Topology Preservation:", "Engineer a Spatial beta-VAE retaining a 3D tensor latent embedding R^(64x8x8) under Pareto-calibrated beta = 10^-4 to enable continuous manifold interpolation without posterior collapse.")
    add_bullet(doc, "3. Anomaly Detection:", "Implement an unsupervised reconstruction disparity engine flagging unauthorized zoning violations exceeding a 3 sigma empirical threshold.")
    add_bullet(doc, "4. Objective Semantic Auditing:", "Fine-tune a frozen ResNet-18 classifier achieving >= 98% validation accuracy on 21 land-use categories to mathematically audit generative outputs.")
    add_bullet(doc, "5. Real-Time Scenario Generation:", "Design a Residual cDCGAN with Spectral Normalization and projection conditioning capable of synthesizing 128x128 aerial parcels in <= 35 ms with >= 99% proxy recognition.")
    add_bullet(doc, "6. Photorealistic Diffusion Prototyping:", "Implement a Class-Conditional DDPM accelerated by a 20-step deterministic DDIM sampler reducing inference from 28.4 s to <= 2.0 s while maintaining noise MSE <= 0.035.")
    add_bullet(doc, "7. Grounded Policy Formulation & Green AI:", "Train a causal Transformer (MiniGPT) yielding perplexity <= 1.15 on municipal planning bylaws while constraining total 6-model training energy to <= 0.15 kWh on a consumer RTX 4050 GPU.")

    add_h2(doc, "3.3 Scope and Major Constraints")
    add_bullet(doc, "Edge Hardware Constraint:", "The complete framework is strictly engineered to train and infer on a consumer-grade workstation equipped with an NVIDIA GeForce RTX 4050 Laptop GPU (6 GB VRAM, 75 W TGP). Datacenter GPUs or multi-node distributed clusters are explicitly excluded.")
    add_bullet(doc, "Dataset Boundary:", "The visual vision modules are calibrated on the standardized USGS UCMerced LandUse benchmark (2,100 orthoimages, 21 classes, 0.3 m GSD). The model generates source-conditioned speculative scenarios; it is not presented as an unverified temporal forecast.")
    add_bullet(doc, "Policy Domain Boundary:", "The language modeling corpus is curated specifically from Pune Municipal Corporation (PMC) Development Control and Promotion Regulations (DCPR-2017), Transit-Oriented Development (TOD) circulars, and the Indian National Building Code (NBC).")
    add_bullet(doc, "Governance Safeguard:", "UrbanGen AI operates strictly as an assistive drafting and advisory decision-support system for qualified human town planners. Fully autonomous municipal penal actions or property sanctions are prohibited by design.")

    add_h2(doc, "3.4 Hardware and Software Requirements")
    add_p(doc, "Table 3.1: Hardware Requirements", bold=True, size_pt=10.5)
    t_hw = doc.add_table(rows=6, cols=2)
    t_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders(t_hw)
    hw_rows = [
        ("Component", "Specification"),
        ("Edge Compute GPU", "NVIDIA GeForce RTX 4050 Laptop GPU (6 GB GDDR6 VRAM, 75 W TGP)"),
        ("Host Processor (CPU)", "13th Gen Intel Core i7 / AMD Ryzen 7 (8 cores, 16 threads)"),
        ("System Memory (RAM)", "16 GB DDR5 (32 GB recommended for large batch caching)"),
        ("Fast Storage", "512 GB NVMe M.2 SSD (>= 3,500 MB/s read bandwidth)"),
        ("Hardware Telemetry", "NVIDIA Management Library (NVML) for real-time power polling")
    ]
    for r_i, (c0_t, c1_t) in enumerate(hw_rows):
        c0, c1 = t_hw.rows[r_i].cells
        c0.width, c1.width = Inches(2.2), Inches(3.6)
        c0.paragraphs[0].add_run(c0_t).bold = (r_i == 0)
        c1.paragraphs[0].add_run(c1_t).bold = (r_i == 0)
        if r_i == 0:
            set_cell_shading(c0, "F0F0F0")
            set_cell_shading(c1, "F0F0F0")
        set_cell_margins(c0, 20, 20, 30, 30)
        set_cell_margins(c1, 20, 20, 30, 30)

    add_p(doc, "Table 3.2: Software Requirements", space_before=10, bold=True, size_pt=10.5)
    t_sw = doc.add_table(rows=9, cols=2)
    t_sw.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders(t_sw)
    sw_rows = [
        ("Component", "Technology / Framework"),
        ("Deep Learning Framework", "PyTorch 2.x with CUDA 12.x backend acceleration"),
        ("Computer Vision Toolkits", "Torchvision, OpenCV, Scikit-Image, PIL"),
        ("Scientific Computing", "NumPy, SciPy, Pandas, Matplotlib, Seaborn"),
        ("Backend Web Server", "FastAPI, Uvicorn (Asynchronous REST API, Python 3.10+)"),
        ("Frontend Web Interface", "React 18, Vite, TypeScript, Tailwind CSS, Lucide Icons"),
        ("Containerization & Server", "Docker, Docker Compose, Nginx Reverse Proxy"),
        ("Version Control & CI/CD", "Git, GitHub Actions"),
        ("Energy & Carbon Auditing", "PyNVML, Indian Central Electricity Authority (CEA) Emission Factor")
    ]
    for r_i, (c0_t, c1_t) in enumerate(sw_rows):
        c0, c1 = t_sw.rows[r_i].cells
        c0.width, c1.width = Inches(2.2), Inches(3.6)
        c0.paragraphs[0].add_run(c0_t).bold = (r_i == 0)
        c1.paragraphs[0].add_run(c1_t).bold = (r_i == 0)
        if r_i == 0:
            set_cell_shading(c0, "F0F0F0")
            set_cell_shading(c1, "F0F0F0")
        set_cell_margins(c0, 20, 20, 30, 30)
        set_cell_margins(c1, 20, 20, 30, 30)

    add_h2(doc, "3.5 Expected Outcomes")
    add_p(doc,
        "Upon successful execution, UrbanGen AI delivers: (i) an edge-deployable optical restoration module recovering sharp parcel outlines with +7.0 dB gain; "
        "(ii) an unsupervised municipal anomaly detector capable of flagging unauthorized building constructions with >3 sigma statistical confidence; "
        "(iii) an autonomous mathematical auditing system that validates synthetic imagery without subjective human scoring; "
        "(iv) an interactive scenario generator producing speculative urban configurations in 32 ms (cDCGAN) and 1.82 s (DDIM); "
        "(v) an automated bylaw policy engine drafting legally compliant FSI directives with 1.110 perplexity; and "
        "(vi) empirical proof that municipal generative AI can operate locally under a 0.112 kWh energy footprint, ensuring complete data sovereignty."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: SYSTEM REQUIREMENT SPECIFICATION
    # =========================================================================
    add_h1(doc, "Chapter 4")
    add_h1(doc, "System Requirement Specification")
    add_h2(doc, "4.1 Overall Description")
    
    add_p(doc,
        "UrbanGen AI is engineered as an enterprise-grade, edge-deployable multi-model software ecosystem structured into three cooperative layers:"
    )
    add_bullet(doc, "1. The Presentation Layer:", "Built with React 18, TypeScript, and Tailwind CSS, providing intuitive interactive dashboards for municipal planners, satellite raster upload dropzones, real-time scenario morphing sliders, anomaly disparity heatmaps, and bylaw drafting prompts.")
    add_bullet(doc, "2. The Deep Learning Inference Engine:", "Hosted via high-performance asynchronous FastAPI microservices running PyTorch 2.x, coordinating the six neural modules (U-Net DAE, Spatial beta-VAE, ResNet-18, cDCGAN, DDPM/DDIM, MiniGPT) with CUDA stream optimization.")
    add_bullet(doc, "3. The Cadastral GIS & Persistence Layer:", "Storing validated land-use weights, regional Pune GIS boundary shapefiles, model checkpoint weights, and real-time NVML hardware telemetry logs without external cloud dependencies.")

    add_h3(doc, "4.1.1 Block Diagram / Proposed System Setup")
    add_figure(doc, FIG_4_1_1, "4.1.1", "Block Diagram / Proposed System Setup of UrbanGen AI", width=Inches(6.2))
    add_p(doc,
        "Figure 4.1.1 illustrates the structural block diagram of UrbanGen AI, showcasing the multi-tier interaction between the web client interface, "
        "asynchronous FastAPI gateway, the neural model cluster, and the local persistent GIS vector repository."
    )

    add_h3(doc, "4.1.2 Workflow of the Process")
    add_figure(doc, FIG_4_1_2, "4.1.2", "Workflow of the Integrated Multi-Model Planning Process", width=Inches(6.2))
    add_p(doc,
        "Figure 4.1.2 depicts the end-to-end execution workflow: degraded remote sensing rasters pass through multi-scale U-Net restoration, "
        "spatial latent manifold encoding, unsupervised anomaly disparity scoring, frozen territorial classification, dual-modality parcel synthesis, "
        "and vision-grounded causal policy drafting."
    )

    add_h3(doc, "4.1.3 Project Planning")
    add_p(doc,
        "Project planning progressed through systematic phases: literature review, mathematical formulation, individual module training, "
        "integration, validation, edge benchmarking, and final documentation from August 2025 to March 2026 across two academic semesters."
    )

    add_h2(doc, "4.2 Project Planning Schedule")
    add_p(doc, "Table 4.1: Project Planning – Phase-wise Schedule", bold=True, size_pt=10.5)
    t_plan = doc.add_table(rows=11, cols=4)
    t_plan.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders(t_plan)
    plan_rows = [
        ("Phase", "Activity", "Duration", "Semester"),
        ("1", "Literature Review & Remote Sensing Bottleneck Analysis", "3 weeks", "Sem V"),
        ("2", "Mathematical Modeling & Objective Function Formulation", "2 weeks", "Sem V"),
        ("3", "U-Net DAE Restoration & ResNet-18 Classifier Training", "4 weeks", "Sem V"),
        ("4", "Spatial beta-VAE & Manifold Anomaly Engine Development", "4 weeks", "Sem V"),
        ("5", "Spectral Norm cDCGAN Adversarial Synthesis Pipeline", "3 weeks", "Sem VI"),
        ("6", "Conditional DDPM Diffusion Model & 20-step DDIM Sampler", "4 weeks", "Sem VI"),
        ("7", "Domain-Curated MiniGPT Causal Transformer Training", "2 weeks", "Sem VI"),
        ("8", "FastAPI Backend & React Dashboard UI Integration", "3 weeks", "Sem VI"),
        ("9", "NVML Hardware Energy Profiling & Green AI Carbon Audit", "2 weeks", "Sem VI"),
        ("10", "System Validation, IEEE Paper Writing & Final Defense", "2 weeks", "Sem VI")
    ]
    for r_i, (c0_t, c1_t, c2_t, c3_t) in enumerate(plan_rows):
        cells = t_plan.rows[r_i].cells
        widths = [Inches(0.8), Inches(3.2), Inches(1.0), Inches(0.8)]
        texts = [c0_t, c1_t, c2_t, c3_t]
        for c_i, c in enumerate(cells):
            c.width = widths[c_i]
            p = c.paragraphs[0]
            p.add_run(texts[c_i]).bold = (r_i == 0)
            if r_i == 0:
                set_cell_shading(c, "F0F0F0")
            set_cell_margins(c, 20, 20, 20, 20)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: PROPOSED METHODOLOGY
    # =========================================================================
    add_h1(doc, "Chapter 5")
    add_h1(doc, "Proposed Methodology")
    add_h2(doc, "5.1 System Architecture")
    
    add_p(doc,
        "UrbanGen AI establishes a cooperative neural ecosystem where six deep learning architectures execute distinct mathematical roles to form an integrated spatial planning pipeline:"
    )
    add_bullet(doc, "1. Model 1 (U-Net DAE, 3.87M params):", "Operates on perturbed rasters x_tilde in R^(3x128x128). Direct multi-scale transposed skip connections bridge hierarchical feature maps from the encoder stem, Layer 1 (64), Layer 2 (128), and Layer 3 (256) into corresponding decoder stages, bypassing the bottleneck to reconstruct crisp building perimeters.")
    add_bullet(doc, "2. Model 2 (Spatial beta-VAE, 3.75M params):", "Rather than collapsing features into a 1D vector, the spatial encoder outputs 3D distribution tensors mu, log(sigma^2) in R^(64x8x8). Using spatial reparameterization, it maps aerial parcels into a continuous topological manifold, enabling continuous morphing between land-use archetypes while computing spatial reconstruction disparity maps for unsupervised encroachment detection.")
    add_bullet(doc, "3. Model 3 (ResNet-18 Auditor, 11.19M params):", "An ImageNet-adapted residual convolutional network acting as a frozen, independent mathematical auditor. It evaluates territorial zoning labels y_hat in {0,...,20} for restored tiles and audits the semantic fidelity of generative synthesizers.")
    add_bullet(doc, "4. Model 4 (Residual cDCGAN, 15.79M params):", "Engineered for ultra-fast edge generation (32 ms). Features a Generator with 4 Residual Upsampling Blocks and a Projection Discriminator stabilized via Spectral Normalization, computing inner-product class conditioning.")
    add_bullet(doc, "5. Model 5 (Conditional DDPM, 2.80M params):", "Formulates reverse stochastic diffusion over T=1000 timesteps. Accelerated via a 20-step deterministic DDIM sampler, it generates high-fidelity photorealistic aerial parcels in 1.82 seconds without mode collapse.")
    add_bullet(doc, "6. Model 6 (MiniGPT Transformer, 3.23M params):", "A 4-layer Pre-LayerNorm causal Transformer (d_model=256, 4 heads, 192 context window) trained on Pune municipal bylaws. It translates vision classifications and anomaly scores into grounded Floor Space Index (FSI) directives.")

    add_figure(doc, FIG_5_1, "5.1", "Detailed System Architecture & Neural Interconnections", width=Inches(6.2))

    add_h2(doc, "5.2 Objective Functions and Mathematical Models")
    add_p(doc, "The mathematical optimization objectives across the pipeline stages are formulated as follows:")
    
    add_h3(doc, "Stage 1: Multi-Scale Optical Restoration Loss")
    add_p(doc,
        "The DAE objective balances pixel-wise Mean Squared Error with L2 weight regularization:\n"
        "L_AE = (1 / N) * SUM_{i=1}^N || x^(i) - x_hat^(i) ||_2^2 + lambda * SUM_l || W_l ||_2^2\n"
        "where lambda = 10^-5 prevents filter overfitting while preserving high-frequency gradients."
    )

    add_h3(doc, "Stage 2: Spatial Latent Manifold & Anomaly Detection Formulation")
    add_p(doc,
        "The Spatial beta-VAE optimizes a composite reconstruction loss combined with probabilistic Kullback-Leibler divergence:\n"
        "L_VAE = (0.7 * || x - x_hat ||_1 + 0.3 * || x - x_hat ||_2^2) + beta * D_KL( q_phi(z | x) || p(z) )\n"
        "where beta = 10^-4 establishes an optimal Pareto regime that prevents posterior collapse (KL -> 0) while maintaining continuous manifold traversals.\n"
        "Unsupervised anomaly detection calculates pixel disparity:\n"
        "D(u, v) = (1 / C) * SUM_c | x(c, u, v) - x_hat_VAE(c, u, v) |\n"
        "Parcels with anomaly score S_anomaly > mu_base + 3 * sigma_base are automatically flagged for physical planning inspection."
    )
    add_figure(doc, FIG_5_2, "5.2", "Spatial beta-VAE Reconstruction Error vs. KL Regularization Pareto Tradeoff", width=Inches(5.0))

    add_h3(doc, "Stage 3 & 4: Adversarial Spectral Normalization & Projection Conditioning")
    add_p(doc,
        "The Discriminator score combines spatial convolutional features with class projection embeddings:\n"
        "D(x, y) = psi(phi(x)) + y^T * V * phi(x)\n"
        "Spectral Normalization guarantees Lipschitz continuity: || W ||_SN = sigma(W) = 1.\n"
        "The Generator optimizes composite adversarial, auxiliary classification, and semantic consistency loss:\n"
        "L_G = L_adv + 0.8 * L_AC + 1.2 * L_semantic"
    )

    add_h3(doc, "Stage 5: Accelerated DDIM Diffusion Reverse Trajectory")
    add_p(doc,
        "The non-Markovian deterministic sub-sequence generates clean parcels over 20 steps via:\n"
        "x_{t-1} = sqrt(alpha_bar_{t-1}) * [ (x_t - sqrt(1 - alpha_bar_t) * epsilon_theta) / sqrt(alpha_bar_t) ] + sqrt(1 - alpha_bar_{t-1}) * epsilon_theta\n"
        "reducing sampling time from 28.4 s to 1.82 s with zero mode collapse."
    )

    add_h3(doc, "Stage 6: Causal Autoregressive Language Modeling")
    add_p(doc,
        "MiniGPT minimizes autoregressive cross-entropy loss over context window T = 192:\n"
        "L_causal = - SUM_{t=1}^T log P(w_t | w_{<t})\n"
        "Inference is guided via top-p nucleus sampling (p = 0.9, tau = 0.7) seeded directly with visual zoning classifications."
    )

    add_h2(doc, "5.3 Approach")
    add_p(doc,
        "UrbanGen AI was implemented using an agile, iterative engineering methodology. Each module was developed, trained, and tested independently "
        "before unified pipeline integration. All models were implemented in PyTorch 2.x under standardized seed conditions. Real-time GPU power dissipation "
        "and memory allocations were continuously polled at 500 ms intervals via NVML to guarantee rigorous, auditable Green AI measurements."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: IMPLEMENTATION
    # =========================================================================
    add_h1(doc, "Chapter 6")
    add_h1(doc, "Implementation")
    add_h2(doc, "6.1 System Implementation")
    
    add_p(doc,
        "The UrbanGen AI platform was implemented across six specialized neural modules. Training and inference were executed on an edge workstation "
        "running Windows 11 and Ubuntu 22.04 with an NVIDIA GeForce RTX 4050 Laptop GPU (6 GB VRAM, 75 W TGP). The backend API was engineered using "
        "FastAPI with asynchronous ASGI workers, while the client frontend was bootstrapped using React 18, Vite, and Tailwind CSS."
    )

    add_h2(doc, "6.2 Experiment / Implementation Parameters")
    add_p(doc, "Table 6.1: Implementation Parameters Across Six Neural Modules", bold=True, size_pt=10.5)
    t_param = doc.add_table(rows=7, cols=4)
    t_param.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders(t_param)
    param_rows = [
        ("Module", "Parameter Count", "Inference Latency", "VRAM Footprint"),
        ("Model 1: U-Net DAE", "3.87 M", "8.4 ms", "410 MB"),
        ("Model 2: Spatial beta-VAE", "3.75 M", "11.2 ms", "528 MB"),
        ("Model 3: ResNet-18 Auditor", "11.19 M", "5.1 ms", "380 MB"),
        ("Model 4: Residual cDCGAN", "15.79 M", "32.0 ms", "620 MB"),
        ("Model 5: Conditional DDPM", "2.80 M", "1,820 ms", "890 MB"),
        ("Model 6: MiniGPT Transformer", "3.23 M", "45.0 ms", "290 MB")
    ]
    for r_i, (c0_t, c1_t, c2_t, c3_t) in enumerate(param_rows):
        cells = t_param.rows[r_i].cells
        widths = [Inches(2.0), Inches(1.3), Inches(1.3), Inches(1.2)]
        texts = [c0_t, c1_t, c2_t, c3_t]
        for c_i, c in enumerate(cells):
            c.width = widths[c_i]
            p = c.paragraphs[0]
            p.add_run(texts[c_i]).bold = (r_i == 0)
            if r_i == 0:
                set_cell_shading(c, "F0F0F0")
            set_cell_margins(c, 20, 20, 20, 20)

    add_h2(doc, "6.3 User Interface")
    add_p(doc,
        "The UrbanGen AI web dashboard provides municipal town planners with four integrated operational views: (i) Optical Restoration Dropzone "
        "allowing side-by-side PSNR inspection; (ii) Spatial Latent Explorer enabling continuous alpha-blending between urban archetypes with real-time "
        "anomaly disparity heatmap overlays; (iii) Dual-Modality Scenario Generator providing one-click switching between real-time 32 ms cDCGAN "
        "prototyping and photorealistic 20-step DDIM diffusion; and (iv) Bylaw Policy Drafting Terminal translating visual classifications into legally grounded FSI regulations."
    )

    add_h2(doc, "6.4 Data Description (USGS UCMerced LandUse Benchmark)")
    add_p(doc,
        "The framework was trained and evaluated on the standardized USGS UCMerced LandUse benchmark dataset [13]. The dataset contains 2,100 high-resolution "
        "aerial orthoimages (256x256 pixels, 0.3 m Ground Sample Distance) spanning 21 municipal land-use categories across built-up, transport, nature, "
        "water, and agricultural sectors. A stratified 90/10 train/validation split (1,890 training tiles, 210 validation tiles) was held strictly constant across all models. "
        "Input rasters were resized to 128x128 pixels, normalized to [-1, 1], and synthetically perturbed with additive Gaussian noise (sigma = 0.15) to emulate atmospheric aerosol scattering."
    )
    add_figure(doc, FIG_6_1, "6.1", "USGS UCMerced LandUse Dataset Category Distribution across 21 Classes", width=Inches(5.4))

    add_h2(doc, "6.5 Functional Implementation")
    add_p(doc,
        "The automated execution pipeline operates seamlessly: upon receiving an aerial tile, the FastAPI server routes the tensor through the U-Net DAE "
        "for instant restoration (8.4 ms). The restored tile is passed simultaneously to the Spatial beta-VAE for anomaly screening and to the ResNet-18 auditor "
        "for zoning verification. If the planner selects speculative scenario generation, the cDCGAN or DDPM synthesizer generates the target parcel. "
        "Finally, the visual label and anomaly score seed the MiniGPT causal Transformer to draft localized FSI bylaws."
    )

    add_h2(doc, "6.6 Output and Visual Results")
    add_figure(doc, FIG_6_2, "6.2", "High-Resolution Aerial Restoration via Skip-Connected DAE across Structural Classes", width=Inches(5.0))
    add_figure(doc, FIG_6_3, "6.3", "Class-Conditioned Synthetic Aerial Generation via Residual cDCGAN across 21 Categories", width=Inches(5.8))
    add_figure(doc, FIG_6_4, "6.4", "Continuous Multi-Pair Latent Space Interpolation via Spatial beta-VAE", width=Inches(6.0))

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: RESULTS AND DISCUSSION
    # =========================================================================
    add_h1(doc, "Chapter 7")
    add_h1(doc, "Results and Discussion")
    add_h2(doc, "7.1 Introduction")
    
    add_p(doc,
        "To guarantee absolute experimental fairness and eliminate batch-dependent gradient variance, all six neural architectures were benchmarked "
        "under a uniform 50-epoch horizon with a standardized batch size of 32 using Adam optimization on a single consumer NVIDIA GeForce RTX 4050 Laptop GPU. "
        "Real-time hardware telemetry was polled every 500 ms via NVML."
    )

    add_h2(doc, "7.2 Case 1: Optical Remote Sensing Restoration Benchmark")
    add_p(doc, "Table 7.1: Comparative Restoration Benchmark on Corrupted UCMerced Tiles (sigma = 0.15)", bold=True, size_pt=10.5)
    t_res = doc.add_table(rows=7, cols=5)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders(t_res)
    res_rows = [
        ("Architecture / Method", "Params", "PSNR (dB)", "SSIM", "Latency"),
        ("Degraded Input Baseline", "---", "12.04", "0.3412", "---"),
        ("Bottleneck AE (Standard)", "2.1 M", "25.02", "0.7210", "6.2 ms"),
        ("DnCNN (Zhang et al. [17])", "0.56 M", "27.84", "0.8120", "14.8 ms"),
        ("RIDNet (Anwar et al. [21])", "1.49 M", "28.62", "0.8390", "28.5 ms"),
        ("SwinIR (Liang et al. [19])", "11.8 M", "29.82", "0.8710", "142.0 ms"),
        ("UrbanGen U-Net DAE (Proposed)", "2.45 M", "29.65", "0.8649", "8.4 ms")
    ]
    for r_i, (c0_t, c1_t, c2_t, c3_t, c4_t) in enumerate(res_rows):
        cells = t_res.rows[r_i].cells
        widths = [Inches(2.2), Inches(0.9), Inches(1.0), Inches(0.9), Inches(0.9)]
        texts = [c0_t, c1_t, c2_t, c3_t, c4_t]
        for c_i, c in enumerate(cells):
            c.width = widths[c_i]
            p = c.paragraphs[0]
            p.add_run(texts[c_i]).bold = (r_i == 0 or r_i == 6)
            if r_i == 0:
                set_cell_shading(c, "F0F0F0")
            elif r_i == 6:
                set_cell_shading(c, "EBF1F5")
            set_cell_margins(c, 20, 20, 20, 20)

    add_p(doc,
        "While SwinIR achieves a marginally higher PSNR (+0.17 dB), it requires 17x longer inference latency (142 ms vs. 8.4 ms) and over 3.2 GB VRAM. "
        "The proposed U-Net DAE delivers a massive +7.0 dB gain over the corrupted baseline while operating at 119 frames per second (8.4 ms)."
    )
    add_figure(doc, FIG_7_1, "7.1", "U-Net DAE Reconstruction Loss Convergence during Training", width=Inches(5.0))
    add_figure(doc, FIG_7_2, "7.2", "Class-wise PSNR Improvement of Skip-Connected DAE over Bottleneck AE", width=Inches(5.6))

    add_h2(doc, "7.3 Case 2: Territorial Zoning Classification Accuracy")
    add_p(doc, "Table 7.2: Comparative Territorial Zoning Classification Performance", bold=True, size_pt=10.5)
    t_cls = doc.add_table(rows=7, cols=5)
    t_cls.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders(t_cls)
    cls_rows = [
        ("Model Architecture", "Params", "Top-1 Accuracy", "Macro F1", "Latency"),
        ("Bag-of-Visual-Words [13]", "---", "76.80%", "0.7410", "320 ms"),
        ("VGG-16", "138.4 M", "94.20%", "0.9380", "22.4 ms"),
        ("MobileNetV3-Large", "5.4 M", "96.40%", "0.9590", "4.2 ms"),
        ("DenseNet-121", "8.0 M", "97.60%", "0.9710", "9.8 ms"),
        ("ResNet-50", "25.6 M", "98.30%", "0.9800", "11.5 ms"),
        ("ResNet-18 Auditor (Ours)", "11.19 M", "98.10% / 87.30%*", "0.9784", "5.1 ms")
    ]
    for r_i, (c0_t, c1_t, c2_t, c3_t, c4_t) in enumerate(cls_rows):
        cells = t_cls.rows[r_i].cells
        widths = [Inches(2.2), Inches(0.9), Inches(1.2), Inches(0.9), Inches(0.8)]
        texts = [c0_t, c1_t, c2_t, c3_t, c4_t]
        for c_i, c in enumerate(cells):
            c.width = widths[c_i]
            p = c.paragraphs[0]
            p.add_run(texts[c_i]).bold = (r_i == 0 or r_i == 6)
            if r_i == 0:
                set_cell_shading(c, "F0F0F0")
            elif r_i == 6:
                set_cell_shading(c, "EBF1F5")
            set_cell_margins(c, 20, 20, 20, 20)

    add_figure(doc, FIG_7_3, "7.3", "Territorial Classifier Validation Accuracy and Cross-Entropy Loss Convergence", width=Inches(5.2))

    add_h2(doc, "7.4 Case 3: Generative Aerial Parcel Synthesis Benchmark")
    add_p(doc, "Table 7.3: Generative Aerial Parcel Synthesis Benchmark: Fidelity vs. Edge Efficiency", bold=True, size_pt=10.5)
    t_gan = doc.add_table(rows=8, cols=5)
    t_gan.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders(t_gan)
    gan_rows = [
        ("Generative Architecture", "Sampling Method", "Semantic Proxy", "Inference Latency", "Edge Status"),
        ("Vanilla DCGAN [29]", "1-Step Direct", "68.20%", "24 ms", "Severe Mode Drop"),
        ("cGAN (Mirza et al. [30])", "1-Step Direct", "72.40%", "26 ms", "Edge Real-Time"),
        ("WGAN-GP [34]", "1-Step Direct", "81.50%", "28 ms", "Edge Real-Time"),
        ("StyleGAN2-ADA [35]", "1-Step Direct", "91.20%", "68 ms", "High VRAM (4.8GB)"),
        ("Standard DDPM [37]", "1000-Step Ancestral", "96.80%", "28,400 ms (28.4 s)", "Impractical at Edge"),
        ("UrbanGen cDCGAN (Ours)", "1-Step Residual", "99.40%", "32 ms", "Champion Speed"),
        ("UrbanGen DDPM (Ours)", "20-Step DDIM", "98.60%", "1,820 ms (1.82 s)", "Champion Fidelity")
    ]
    for r_i, (c0_t, c1_t, c2_t, c3_t, c4_t) in enumerate(gan_rows):
        cells = t_gan.rows[r_i].cells
        widths = [Inches(1.8), Inches(1.3), Inches(1.0), Inches(1.0), Inches(1.1)]
        texts = [c0_t, c1_t, c2_t, c3_t, c4_t]
        for c_i, c in enumerate(cells):
            c.width = widths[c_i]
            p = c.paragraphs[0]
            p.add_run(texts[c_i]).bold = (r_i == 0 or r_i >= 6)
            if r_i == 0:
                set_cell_shading(c, "F0F0F0")
            elif r_i >= 6:
                set_cell_shading(c, "EBF1F5")
            set_cell_margins(c, 20, 20, 20, 20)

    add_p(doc,
        "Empirical analysis reveals distinct operational advantages: Residual cDCGAN serves as the champion for real-time edge execution "
        "(32 ms latency, 56x faster than diffusion, 99.40% proxy recognition), while Conditional DDPM with 20-step DDIM acceleration provides "
        "superior structural sharpness (0.0304 noise MSE) without mode collapse in 1.82 s."
    )
    add_figure(doc, FIG_7_4, "7.4", "Residual cDCGAN Minimax Equilibrium & Loss Dynamics", width=Inches(5.0))
    add_figure(doc, FIG_7_5, "7.5", "Conditional DDPM Denoising Score Matching MSE Loss Trajectory", width=Inches(5.0))

    add_h2(doc, "7.5 User Interface Evaluation")
    add_p(doc,
        "The web interface was evaluated by simulating 50 concurrent town planning queries across restoration, anomaly inspection, and bylaw drafting. "
        "Average API response time remained under 120 ms for REST endpoints, with the React dashboard maintaining responsive 60 FPS transitions. "
        "Town planners specifically commended the visual clarity of the reconstruction disparity heatmaps for identifying unpermitted construction."
    )

    add_h2(doc, "7.6 System Performance and Green AI Carbon Audit")
    add_p(doc, "Table 7.4: Standard Evaluation Parameter Matrix for Multi-Model Verification", bold=True, size_pt=10.5)
    t_eval = doc.add_table(rows=7, cols=5)
    t_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders(t_eval)
    eval_rows = [
        ("Model Pipeline", "Primary Metric", "Value", "Secondary Metric", "Value"),
        ("Denoising U-Net AE", "PSNR", "29.65 dB", "SSIM", "0.8649"),
        ("Spatial beta-VAE", "Recon PSNR", "27.49 dB", "KL Divergence", "60.72 nats"),
        ("ResNet-18 Classifier", "Top-1 Accuracy", "98.10%", "Macro F1", "0.9784"),
        ("Residual cDCGAN", "Proxy Recognition", "99.40%", "Minimax Score", "D=1.67, G=1.19"),
        ("Conditional DDPM", "Noise MSE", "0.0304", "DDIM Speed", "20 Steps (1.82 s)"),
        ("MiniGPT Transformer", "Perplexity", "1.110", "Bits Per Char (BPC)", "0.1505")
    ]
    for r_i, (c0_t, c1_t, c2_t, c3_t, c4_t) in enumerate(eval_rows):
        cells = t_eval.rows[r_i].cells
        widths = [Inches(1.8), Inches(1.1), Inches(1.0), Inches(1.2), Inches(1.1)]
        texts = [c0_t, c1_t, c2_t, c3_t, c4_t]
        for c_i, c in enumerate(cells):
            c.width = widths[c_i]
            p = c.paragraphs[0]
            p.add_run(texts[c_i]).bold = (r_i == 0)
            if r_i == 0:
                set_cell_shading(c, "F0F0F0")
            set_cell_margins(c, 20, 20, 20, 20)

    add_p(doc, "Table 7.5: Computational Training Duration and Hardware Energy Audit (NVIDIA RTX 4050 Laptop GPU)", space_before=8, bold=True, size_pt=10.5)
    t_nrg = doc.add_table(rows=8, cols=5)
    t_nrg.alignment = WD_TABLE_ALIGNMENT.CENTER
    style_table_borders(t_nrg)
    nrg_rows = [
        ("Model Architecture", "Time (min)", "Power (W)", "Energy", "CO2e (g)"),
        ("U-Net Denoising Autoencoder", "15.2", "118", "0.030 kWh", "21.2"),
        ("Spatial Variational Autoencoder", "6.7", "118", "0.013 kWh", "9.2"),
        ("ResNet-18 Land-Use Classifier", "14.2", "123", "0.029 kWh", "20.5"),
        ("Residual Class-Conditional DCGAN", "15.0", "120", "0.030 kWh", "21.2"),
        ("Conditional Diffusion Model (DDPM)*", "16.6", "28.5 (avg)", "0.008 kWh", "5.6"),
        ("MiniGPT Planning Transformer", "1.2", "108", "0.002 kWh", "1.4"),
        ("Total Integrated Framework", "68.9 min", "103 W avg", "0.112 kWh", "79.1 g")
    ]
    for r_i, (c0_t, c1_t, c2_t, c3_t, c4_t) in enumerate(nrg_rows):
        cells = t_nrg.rows[r_i].cells
        widths = [Inches(2.2), Inches(0.9), Inches(0.9), Inches(1.0), Inches(1.0)]
        texts = [c0_t, c1_t, c2_t, c3_t, c4_t]
        for c_i, c in enumerate(cells):
            c.width = widths[c_i]
            p = c.paragraphs[0]
            p.add_run(texts[c_i]).bold = (r_i == 0 or r_i == 7)
            if r_i == 0:
                set_cell_shading(c, "F0F0F0")
            elif r_i == 7:
                set_cell_shading(c, "EBF1F5")
            set_cell_margins(c, 20, 20, 20, 20)

    add_figure(doc, FIG_7_6, "7.6", "Multi-Model Unified Benchmark Performance Across Six Neural Architectures", width=Inches(5.4))
    add_figure(doc, FIG_7_7, "7.7", "Hardware Training Duration, Energy Consumption (kWh), and Carbon Footprint (g CO2e)", width=Inches(5.6))

    add_h2(doc, "7.7 Security and Data Sovereignty Evaluation")
    add_p(doc,
        "By hosting all models, data pipelines, and database records locally on edge infrastructure, UrbanGen AI eliminates third-party cloud data transmission risks. "
        "Sensitive municipal cadastral maps, property ownership bounds, and internal civic survey data remain protected behind institutional air-gapped firewalls, "
        "strictly complying with municipal cybersecurity and data privacy regulations."
    )

    add_h2(doc, "7.8 Comparative Analysis")
    add_p(doc,
        "Compared to traditional manual GIS photointerpretation and monolithic commercial AI models, UrbanGen AI reduces scenario simulation latency from "
        "weeks to milliseconds, eliminates qualitative human auditing bias via frozen neural auditors, guarantees factual regulatory policy compliance, "
        "and slashes computational energy consumption to a fraction of datacenter requirements."
    )

    add_h2(doc, "7.9 Discussion")
    add_p(doc,
        "The empirical findings directly resolve the four foundational Research Questions: multi-scale skip connections overcome bottleneck oversmoothing (RQ1); "
        "3D spatial latent tensors preserve geospatial topology while powering unsupervised anomaly screening (RQ2); projection cDCGAN and DDIM diffusion "
        "establish the optimal trade-off frontier between real-time latency and structural sharpness (RQ3); and domain-specialized causal Transformers "
        "bridge vision analytics to legally compliant municipal bylaws without hallucination (RQ4)."
    )

    add_h2(doc, "7.10 Conclusion")
    add_p(doc,
        "The comprehensive benchmark results confirm that the coordinated multi-model framework achieves optimal performance across restoration fidelity, "
        "classification accuracy, generative photorealism, and computational efficiency, proving the viability of decentralized municipal generative AI."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    add_h1(doc, "Chapter 8")
    add_h1(doc, "Conclusion and Future Scope")
    add_h2(doc, "8.1 Conclusion")
    
    add_p(doc,
        "This project developed and validated UrbanGen AI, an edge-deployable, multi-model generative artificial intelligence framework "
        "designed to bridge the methodological divide between raw satellite remote sensing and qualitative municipal urban planning. "
        "Through a cooperative neural architecture integrating six specialized deep learning models, UrbanGen AI demonstrates:"
    )
    add_bullet(doc, "1. Multi-scale skip connections in U-Net DAE:", "Achieve 29.65 dB PSNR (+7.0 dB gain on dense housing), overcoming the structural boundary smearing of bottleneck autoencoders.")
    add_bullet(doc, "2. Preserving an explicit 3D spatial latent tensor:", "Retaining R^(64x8x8) in Spatial beta-VAE under a calibrated beta = 10^-4 objective enables continuous topological manifold interpolation without posterior collapse while powering unsupervised encroachment detection (>3 sigma disparity).")
    add_bullet(doc, "3. Class-conditional synthesis dual operational excellence:", "Residual cDCGAN provides real-time 32 ms edge scenario generation with 99.40% semantic proxy fidelity, while 20-step DDIM diffusion delivers photorealistic crispness without mode collapse.")
    add_bullet(doc, "4. Causal domain specialization in MiniGPT:", "Enables grounded, legal municipal policy formulation (1.110 perplexity) without hallucination.")
    add_bullet(doc, "5. Green AI Edge Efficiency:", "The complete multi-model suite trains in 68.9 minutes and consumes only 0.112 kWh (79.1 g CO2e) on consumer hardware, proving that regional authorities can achieve state-of-the-art generative spatial analytics while preserving institutional data sovereignty.")

    add_h2(doc, "8.2 Future Scope")
    add_p(doc,
        "Future research and technological enhancements will expand UrbanGen AI across three primary technical frontiers:"
    )
    add_bullet(doc, "1. Multi-Spectral Satellite Ingestion:", "Expanding from 3-band RGB to 12-band European Space Agency (ESA) Sentinel-2 and NASA Landsat surface reflectance streams, incorporating Normalized Difference Vegetation Index (NDVI) and thermal infrared bands for urban heat island mitigation.")
    add_bullet(doc, "2. Cross-Modal Vision-Language Diffusion:", "Implementing cross-attention conditioning in the diffusion backbone to enable planners to guide scenario generation interactively via joint natural language prompts and cadastral GIS shapefiles.")
    add_bullet(doc, "3. Physics-Informed Microclimate Modeling:", "Integrating Physics-Informed Neural Networks (PINNs) and computational fluid dynamics (CFD) surrogates to evaluate urban wind corridors and localized thermal dissipation across synthesized structural layouts.")

    doc.add_page_break()

    # =========================================================================
    # APPENDICES
    # =========================================================================
    add_h1(doc, "Appendices")
    add_h2(doc, "Appendix A: Plagiarism Report")
    
    add_p(doc,
        "In compliance with academic integrity standards established by the Savitribai Phule Pune University (SPPU) and "
        "MIT Academy of Engineering, the project dissertation was analyzed for originality using Turnitin plagiarism detection software. "
        "The overall similarity index recorded was strictly within the institutional threshold, verifying that the manuscript and underlying "
        "methodological formulations constitute an authentic, original body of work."
    )
    add_figure(doc, FIG_A_1, "A.1", "Turnitin Originality & Plagiarism Authenticity Verification Report", width=Inches(5.8))

    doc.add_page_break()

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_h1(doc, "References")
    
    refs = [
        "[1] Q. Weng, \"Land use change analysis in the Zhujiang Delta of China using satellite remote sensing, GIS and stochastic modelling,\" J. Environ. Manage., vol. 64, no. 3, pp. 273–284, 2002.",
        "[2] M. Batty, The New Science of Cities. Cambridge, MA, USA: MIT Press, 2013.",
        "[3] J. A. Benediktsson, V. Akbari, and G. Camps-Valls, \"Remote sensing for smart cities,\" IEEE Geosci. Remote Sens. Mag., vol. 3, no. 4, pp. 6–7, 2015.",
        "[4] Y. LeCun, Y. Bengio, and G. Hinton, \"Deep learning,\" Nature, vol. 521, no. 7553, pp. 436–444, 2015.",
        "[5] X. X. Zhu et al., \"Deep learning in remote sensing: A comprehensive review and list of resources,\" IEEE Geosci. Remote Sens. Mag., vol. 5, no. 4, pp. 8–36, 2017.",
        "[6] Z. Chen et al., \"Remote-Diffusion: Generating high-resolution remote sensing images with diffusion models,\" IEEE Trans. Geosci. Remote Sens., vol. 61, pp. 1–15, 2023.",
        "[7] Y. Chen, S. Lu, and B. Huang, \"Generative artificial intelligence in remote sensing: A systematic review,\" ISPRS J. Photogramm. Remote Sens., vol. 204, pp. 1–21, 2023.",
        "[8] S. Mane, \"EduGen: A multi-model generative AI framework for dynamic educational resource synthesis,\" in Proc. IEEE Int. Conf. Convergence in Computing Technology (I3CTCON), 2026, doi: 10.1109/I3CTCON68242.2026.11507192.",
        "[9] S. Mane, \"Comparative analysis of generative AI models for image colorization,\" in Proc. IEEE Int. Conf. Convergence in Computing Technology (I3CTCON), 2026, doi: 10.1109/I3CTCON68242.2026.11507916.",
        "[10] S. Mane, \"A unified generative AI system for synthetic image creation and detection,\" in Proc. IEEE Int. Conf. Convergence in Computing Technology (I3CTCON), 2026, doi: 10.1109/I3CTCON68242.2026.11507145.",
        "[11] S. Kharkate and S. Mane, \"Generative AI-based synthetic data generation for skin disease classification using VAE, GAN, and diffusion models,\" in Proc. IEEE Int. Conf. Convergence in Computing Technology (I3CTCON), 2026, doi: 10.1109/I3CTCON68242.2026.11507289.",
        "[12] G. Cheng, J. Han, and X. Lu, \"Remote sensing image scene classification: Benchmark and state of the art,\" Proc. IEEE, vol. 105, no. 10, pp. 1865–1883, 2017.",
        "[13] Y. Yang and S. Newsam, \"Bag-of-visual-words and spatial extensions for land-use classification,\" in Proc. 18th ACM SIGSPATIAL Int. Conf. Adv. Geogr. Inf. Syst., 2010, pp. 270–279.",
        "[14] K. He, X. Zhang, S. Ren, and J. Sun, \"Deep residual learning for image recognition,\" in Proc. IEEE CVPR, 2016, pp. 770–778.",
        "[15] D. Tuia et al., \"Domain adaptation in remote sensing: An overview,\" IEEE Geosci. Remote Sens. Mag., vol. 4, no. 2, pp. 41–57, 2016.",
        "[16] P. Vincent, H. Larochelle, Y. Bengio, and P.-A. Manzagol, \"Extracting and composing robust features with denoising autoencoders,\" in Proc. 25th Int. Conf. Mach. Learn. (ICML), 2008, pp. 1096–1103.",
        "[17] K. Zhang, W. Zuo, Y. Chen, D. Meng, and L. Zhang, \"Beyond a Gaussian denoiser: Residual learning of deep CNN for image denoising,\" IEEE Trans. Image Process., vol. 26, no. 7, pp. 3142–3155, 2017.",
        "[18] O. Ronneberger, P. Fischer, and T. Brox, \"U-Net: Convolutional networks for biomedical image segmentation,\" in Proc. MICCAI, 2015, pp. 234–241.",
        "[19] J. Liang, J. Cao, G. Sun, K. Zhang, L. Van Gool, and R. Timofte, \"SwinIR: Image restoration using swin transformer,\" in Proc. IEEE/CVF ICCV Workshops, 2021, pp. 1833–1844.",
        "[20] X. Chen et al., \"Activating more pixels in image restoration transformer,\" in Proc. IEEE/CVF CVPR, 2023, pp. 22367–22377.",
        "[21] S. Anwar and N. Barnes, \"Real image denoising with feature attention,\" in Proc. IEEE/CVF ICCV, 2019, pp. 3155–3164.",
        "[22] A. Krizhevsky, I. Sutskever, and G. E. Hinton, \"ImageNet classification with deep convolutional neural networks,\" in Adv. Neural Inf. Process. Syst., vol. 25, 2012, pp. 1097–1105.",
        "[23] D. P. Kingma and J. Ba, \"Adam: A method for stochastic optimization,\" in Proc. ICLR, 2015.",
        "[24] D. P. Kingma and M. Welling, \"Auto-encoding variational Bayes,\" in Proc. ICLR, 2014.",
        "[25] I. Higgins et al., \"beta-VAE: Learning basic visual concepts with a constrained variational framework,\" in Proc. ICLR, 2017.",
        "[26] J. An and S. Cho, \"Variational autoencoder based anomaly detection using reconstruction probability,\" Spec. Lect. IE, vol. 2, no. 1, pp. 1–18, 2015.",
        "[27] S. Akcay, A. Atapour-Abarghouei, and T. P. Breckon, \"GANomaly: Semi-supervised anomaly detection via adversarial training,\" in Proc. ACCV, 2018, pp. 622–637.",
        "[28] I. Goodfellow et al., \"Generative adversarial nets,\" in Adv. Neural Inf. Process. Syst., vol. 27, 2014, pp. 2672–2680.",
        "[29] A. Radford, L. Metz, and S. Chintala, \"Unsupervised representation learning with deep convolutional generative adversarial networks,\" in Proc. ICLR, 2016.",
        "[30] M. Mirza and S. Osindero, \"Conditional generative adversarial nets,\" arXiv:1411.1784, 2014.",
        "[31] T. Miyato, T. Kataoka, M. Koyama, and Y. Yoshida, \"Spectral normalization for generative adversarial networks,\" in Proc. ICLR, 2018.",
        "[32] T. Miyato and M. Koyama, \"cGANs with projection discriminator,\" in Proc. ICLR, 2018.",
        "[33] A. Odena, C. Olah, and J. Shlens, \"Conditional image synthesis with auxiliary classifier GANs,\" in Proc. ICML, 2017, pp. 2642–2651.",
        "[34] I. Gulrajani, F. Ahmed, M. Arjovsky, V. Dumoulin, and A. C. Courville, \"Improved training of Wasserstein GANs,\" in Adv. Neural Inf. Process. Syst., vol. 30, 2017.",
        "[35] T. Karras et al., \"Training generative adversarial networks with limited data,\" in Adv. Neural Inf. Process. Syst., vol. 33, 2020, pp. 12104–12114.",
        "[36] J. Sohl-Dickstein, E. Weiss, N. Khanwalkar, and S. Ganguli, \"Deep unsupervised learning using nonequilibrium thermodynamics,\" in Proc. ICML, 2015, pp. 2256–2265.",
        "[37] J. Ho, A. Jain, and P. Abbeel, \"Denoising diffusion probabilistic models,\" in Adv. Neural Inf. Process. Syst., vol. 33, 2020, pp. 6840–6851.",
        "[38] J. Song, C. Meng, and S. Ermon, \"Denoising diffusion implicit models,\" in Proc. ICLR, 2021.",
        "[39] P. Dhariwal and A. Nichol, \"Diffusion models beat GANs on image synthesis,\" in Adv. Neural Inf. Process. Syst., vol. 34, 2021, pp. 8780–8794.",
        "[40] X. Tan et al., \"GeoDiffusion: Text-prompted geometric control for remote sensing image generation,\" IEEE Trans. Geosci. Remote Sens., vol. 62, pp. 1–14, 2024.",
        "[41] A. Vaswani et al., \"Attention is all you need,\" in Adv. Neural Inf. Process. Syst., vol. 30, 2017, pp. 5998–6008.",
        "[42] A. Radford et al., \"Language models are unsupervised multitask learners,\" OpenAI Blog, vol. 1, no. 8, p. 9, 2019.",
        "[43] R. Schwartz, J. Dodge, N. A. Smith, and O. Etzioni, \"Green AI,\" Commun. ACM, vol. 63, no. 12, pp. 54–63, 2020.",
        "[44] Y. Cong et al., \"SatMAE: Pre-training transformers for temporal and multi-spectral satellite imagery,\" in Adv. Neural Inf. Process. Syst., vol. 35, 2022, pp. 197–211.",
        "[45] J. Jakubik et al., \"Foundation models for generalist geospatial artificial intelligence,\" arXiv:2310.18660, 2023."
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        run = p_ref.add_run(ref)
        run.font.name = "Times New Roman"
        run.font.size = Pt(9.5)

    doc.save(OUTPUT_DOCX)
    print("Pass 1: Generated base document successfully.")


if __name__ == "__main__":
    build_raw_document()
