from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

OUTPUT = "reports/insight_report.pdf"

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    topMargin=12*mm, bottomMargin=12*mm,
    leftMargin=16*mm, rightMargin=16*mm
)

# ── Colours ────────────────────────────────────────────────
NAVY   = colors.HexColor("#1e3a5f")
BLUE   = colors.HexColor("#2563eb")
RED    = colors.HexColor("#dc2626")
GREEN  = colors.HexColor("#16a34a")
ORANGE = colors.HexColor("#ea580c")
LGRAY  = colors.HexColor("#f1f5f9")
MGRAY  = colors.HexColor("#94a3b8")
WHITE  = colors.white

# ── Styles ─────────────────────────────────────────────────
base = getSampleStyleSheet()

def style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=base[parent], **kw)
    return s

S = {
    "header_name" : style("hn", fontSize=9,  textColor=MGRAY, leading=11),
    "header_title": style("ht", fontSize=18, textColor=WHITE, fontName="Helvetica-Bold", leading=22),
    "header_sub"  : style("hs", fontSize=9,  textColor=colors.HexColor("#bfdbfe"), leading=12),
    "section"     : style("sec", fontSize=8, textColor=BLUE,  fontName="Helvetica-Bold",
                          leading=10, spaceBefore=6),
    "body"        : style("body", fontSize=8.5, textColor=colors.HexColor("#1e293b"),
                          leading=13, spaceAfter=3),
    "kpi_val"     : style("kv", fontSize=20, fontName="Helvetica-Bold",
                          textColor=NAVY, leading=24, alignment=TA_CENTER),
    "kpi_lbl"     : style("kl", fontSize=7.5, textColor=MGRAY, leading=10, alignment=TA_CENTER),
    "find_title"  : style("ft", fontSize=8.5, fontName="Helvetica-Bold",
                          textColor=NAVY, leading=11),
    "find_body"   : style("fb", fontSize=8,   textColor=colors.HexColor("#334155"), leading=12),
    "rec_title"   : style("rt", fontSize=8.5, fontName="Helvetica-Bold",
                          textColor=WHITE, leading=11),
    "rec_body"    : style("rb", fontSize=8,   textColor=colors.HexColor("#e2e8f0"), leading=12),
    "footer"      : style("ft2", fontSize=7.5, textColor=MGRAY, alignment=TA_CENTER, leading=10),
    "tag"         : style("tag", fontSize=7,  textColor=WHITE, fontName="Helvetica-Bold",
                          alignment=TA_CENTER, leading=9),
}

story = []

# ═══════════════════════════════════════════════════════════
# HEADER BANNER
# ═══════════════════════════════════════════════════════════
header_data = [[
    Paragraph("BUSINESS INSIGHT REPORT", S["header_name"]),
    Paragraph("", S["header_name"]),
    Paragraph("Juvana Dsouza  |  juvanadsouza81@gmail.com", S["header_name"]),
],[
    Paragraph("India E-Commerce Pulse", S["header_title"]),
    Paragraph("", S["header_title"]),
    Paragraph("", S["header_title"]),
],[
    Paragraph("Amazon Sales Analysis  •  128,975 Rows  •  Apr – Jun 2022  •  Python | SQL | Power BI", S["header_sub"]),
    Paragraph("", S["header_sub"]),
    Paragraph("", S["header_sub"]),
]]

header_table = Table(header_data, colWidths=[110*mm, 20*mm, 48*mm])
header_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), NAVY),
    ("SPAN",       (0,1), (1,1)),
    ("SPAN",       (0,2), (2,2)),
    ("SPAN",       (0,0), (1,0)),
    ("ALIGN",      (2,0), (2,0), "RIGHT"),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ("ROUNDEDCORNERS", [4,4,4,4]),
]))
story.append(header_table)
story.append(Spacer(1, 5*mm))

# ═══════════════════════════════════════════════════════════
# KPI ROW
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("KEY METRICS AT A GLANCE", S["section"]))
story.append(Spacer(1, 2*mm))

kpi_vals = [
    ("Rs.78.6M", "Total GMV"),
    ("128,975", "Total Orders"),
    ("Rs.648.56", "Avg Order Value"),
    ("8.35%", "Cancellation Rate"),
    ("Rs.69.2L", "Revenue at Risk"),
]

kpi_cells = [[Paragraph(v, S["kpi_val"]) for v,_ in kpi_vals],
             [Paragraph(l, S["kpi_lbl"]) for _,l in kpi_vals]]

kpi_table = Table(kpi_cells, colWidths=[36*mm]*5)
kpi_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), LGRAY),
    ("TOPPADDING",    (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LINEAFTER",     (0,0), (3,-1), 0.5, colors.HexColor("#cbd5e1")),
    ("ROUNDEDCORNERS", [4,4,4,4]),
]))
story.append(kpi_table)
story.append(Spacer(1, 5*mm))

# ═══════════════════════════════════════════════════════════
# BUSINESS PROBLEM
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("BUSINESS PROBLEM", S["section"]))
story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=3))
story.append(Paragraph(
    "An Indian e-commerce platform selling apparel on Amazon is experiencing a critical paradox: "
    "order volumes remain strong at 128,975 transactions, yet significant revenue is being eroded "
    "through high cancellation rates, category-level margin inefficiencies, and geographic concentration risk. "
    "This analysis investigates root causes across three dimensions — category performance, regional opportunity, "
    "and operational risk — to deliver three actionable business recommendations.",
    S["body"]
))
story.append(Spacer(1, 4*mm))

# ═══════════════════════════════════════════════════════════
# KEY FINDINGS  (2-column layout)
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("KEY FINDINGS", S["section"]))
story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=3))

findings = [
    (RED,   "01", "Cancellations Are Costing Rs.69.2 Lakhs",
     "8.35% of all orders are cancelled, representing Rs.69,19,284 in lost revenue. "
     "Critically, the two highest-revenue categories — Set (Rs.35.7M) and Kurta (Rs.19.4M) — "
     "also carry the highest cancellation rates at 14.59% and 14.55% respectively. "
     "This means the platform's core revenue drivers are simultaneously its biggest leakage points."),

    (ORANGE, "02", "Sets Earn 83% More Per Order Than Kurtas",
     "Average order value for Sets is Rs.834 vs Rs.457 for Kurtas — yet both categories "
     "receive similar order volumes (~42K each). The business is under-investing in its "
     "highest-value category. Shifting even 20% of Kurta acquisition spend toward Sets "
     "would significantly increase revenue per marketing rupee spent."),

    (BLUE,  "03", "Maharashtra + Karnataka = 28% of All Revenue",
     "These two states alone drive Rs.2.18 Crore. Bengaluru leads all cities at Rs.72.5L, "
     "followed by Hyderabad (Rs.55.7L) and Mumbai (Rs.42.9L). This geographic concentration "
     "creates systemic risk — any demand disruption in these states directly impacts overall performance."),

    (GREEN, "04", "High-Value Opportunity Markets Are Untapped",
     "Ladakh (Rs.929 AOV), Nagaland (Rs.825 AOV), and Chandigarh (Rs.823 AOV) show "
     "above-average willingness to pay but near-zero order volumes. These states sit in the "
     "high-AOV, low-volume quadrant — signalling unmet demand with strong revenue potential "
     "that can be unlocked through targeted digital campaigns at low CAC."),
]

find_rows = []
for i in range(0, len(findings), 2):
    row = []
    for color, num, title, body in findings[i:i+2]:
        tag = Table([[Paragraph(f"FINDING {num}", S["tag"])]],
                    colWidths=[22*mm])
        tag.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), color),
            ("TOPPADDING",    (0,0), (-1,-1), 2),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2),
            ("ROUNDEDCORNERS", [3,3,3,3]),
        ]))
        cell_content = Table([
            [tag],
            [Paragraph(title, S["find_title"])],
            [Paragraph(body,  S["find_body"])],
        ], colWidths=[86*mm])
        cell_content.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), LGRAY),
            ("TOPPADDING",    (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
            ("RIGHTPADDING",  (0,0), (-1,-1), 6),
            ("ROUNDEDCORNERS", [4,4,4,4]),
        ]))
        row.append(cell_content)
    if len(row) == 1:
        row.append("")
    find_rows.append(row)

find_table = Table(find_rows, colWidths=[89*mm, 89*mm], spaceBefore=2)
find_table.setStyle(TableStyle([
    ("VALIGN",      (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("RIGHTPADDING",(0,0), (-1,-1), 3),
    ("TOPPADDING",  (0,0), (-1,-1), 0),
    ("BOTTOMPADDING",(0,0),(-1,-1), 4),
]))
story.append(find_table)
story.append(Spacer(1, 4*mm))

# ═══════════════════════════════════════════════════════════
# RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("BUSINESS RECOMMENDATIONS", S["section"]))
story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=3))

recs = [
    (RED,   "01", "Reduce Cancellations in Top Categories — Target: <10%",
     "Set and Kurta together lose Rs.40L+ annually to cancellations. Immediate actions: "
     "(1) Conduct root cause analysis via customer exit surveys — sizing? imagery? delivery SLA? "
     "(2) Implement real-time size recommendation engine. "
     "(3) Add 'cancellation reason' tagging to build a structured dataset for further analysis. "
     "Reducing cancellation rate from 14.5% to 10% recovers an estimated Rs.20L+ annually."),

    (ORANGE, "02", "Reallocate Marketing Budget Toward High-AOV Categories",
     "Sets generate Rs.834 per order vs Rs.457 for Kurtas at the same acquisition cost. "
     "Recommendation: Shift 20-25% of Kurta ad spend to Sets and Western Dress (Rs.764 AOV). "
     "This reallocation requires no new customers — just better spend allocation across existing traffic. "
     "Projected impact: 12-15% increase in revenue per marketing rupee."),

    (GREEN, "03", "Launch Targeted Campaigns in Opportunity States",
     "Ladakh, Nagaland, Chandigarh and other high-AOV low-volume states represent Rs.X Crore "
     "in addressable revenue that is currently untapped. "
     "Recommendation: Run 60-day targeted digital campaigns in Top 5 opportunity states "
     "before committing to logistics expansion. "
     "Success metric: AOV maintained above Rs.800 with order volume growing 3x within 90 days."),
]

rec_rows = []
for color, num, title, body in recs:
    num_cell = Table([[Paragraph(num, ParagraphStyle("rn", fontSize=16,
                      fontName="Helvetica-Bold", textColor=WHITE,
                      alignment=TA_CENTER, leading=20))]],
                    colWidths=[14*mm], rowHeights=[14*mm])
    num_cell.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), color),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ROUNDEDCORNERS",[3,3,3,3]),
    ]))

    text_cell = Table([
        [Paragraph(title, S["find_title"])],
        [Paragraph(body,  S["find_body"])],
    ], colWidths=[160*mm])
    text_cell.setStyle(TableStyle([
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ]))

    row_table = Table([[num_cell, text_cell]], colWidths=[16*mm, 162*mm])
    row_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LGRAY),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("ROUNDEDCORNERS",[4,4,4,4]),
    ]))
    rec_rows.append([row_table])
    rec_rows.append([Spacer(1, 3*mm)])

rec_table = Table(rec_rows, colWidths=[178*mm])
rec_table.setStyle(TableStyle([
    ("LEFTPADDING",  (0,0), (-1,-1), 0),
    ("RIGHTPADDING", (0,0), (-1,-1), 0),
    ("TOPPADDING",   (0,0), (-1,-1), 0),
    ("BOTTOMPADDING",(0,0), (-1,-1), 0),
]))
story.append(rec_table)
story.append(Spacer(1, 4*mm))

# ═══════════════════════════════════════════════════════════
# NEXT STEPS
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("NEXT STEPS & METHODOLOGY", S["section"]))
story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=3))

next_data = [
    ["IMMEDIATE (0-30 days)", "SHORT TERM (30-90 days)", "LONG TERM (90+ days)"],
    [
        "- Tag cancellation reasons\n- A/B test size guide on Set PDPs\n- Export opportunity state list",
        "- Launch pilot campaigns in Ladakh, Nagaland\n- Reallocate 20% ad budget to Sets\n- Build cancellation tracking dashboard",
        "- Expand logistics to Tier-2 opportunity states\n- Develop B2B sales motion\n- Implement predictive cancellation model"
    ]
]

next_table = Table(next_data, colWidths=[59*mm, 59*mm, 60*mm])
next_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), NAVY),
    ("BACKGROUND",    (0,1), (-1,1), LGRAY),
    ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
    ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,-1), 7.5),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ("RIGHTPADDING",  (0,0), (-1,-1), 6),
    ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
]))
story.append(next_table)
story.append(Spacer(1, 5*mm))

# ═══════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════
footer_data = [[
    Paragraph("Juvana Dsouza  |  B.E. AI & Data Science, Fr. CRCE Mumbai", S["footer"]),
    Paragraph("github.com/juvana81/india-ecommerce-bi-analysis", S["footer"]),
    Paragraph("Tools: Python • SQL • Power BI • Excel", S["footer"]),
]]
footer_table = Table(footer_data, colWidths=[60*mm, 70*mm, 48*mm])
footer_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), NAVY),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ("ROUNDEDCORNERS",[4,4,4,4]),
]))
story.append(footer_table)

# ── Build ──────────────────────────────────────────────────
doc.build(story)
print(f"Report saved to {OUTPUT}")
