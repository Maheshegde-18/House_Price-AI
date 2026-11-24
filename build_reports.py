"""
HousePrice AI - Academic Project Report Generator (Optimized for 8-9 Page Academic Standard)
Builds:
1. HousePrice_AI_Project_Report.docx (Fully editable Microsoft Word document)
2. HousePrice_AI_Project_Report.pdf (Matching high-fidelity compiled PDF document)
Complies strictly with NMAM Institute of Technology, Department of MCA academic formatting standards.
"""

import os
import sys
import subprocess
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

base_dir = os.path.dirname(os.path.abspath(__file__))
screenshots_dir = os.path.join(base_dir, 'screenshots')
logo_path = os.path.join(base_dir, 'nitte_logo.jpg')
workflow_path = os.path.join(base_dir, 'workflow_diagram.png')

fig2_path = os.path.join(screenshots_dir, 'app_dashboard.png')
fig3_path = os.path.join(screenshots_dir, 'app_prediction.png')
fig4_path = os.path.join(screenshots_dir, 'app_analytics.png')
fig5_path = os.path.join(screenshots_dir, 'app_performance.png')
fig6_path = os.path.join(screenshots_dir, 'app_history.png')

docx_output_path = os.path.join(base_dir, 'HousePrice_AI_Project_Report.docx')
html_output_path = os.path.join(base_dir, 'HousePrice_AI_Project_Report.html')
pdf_output_path = os.path.join(base_dir, 'HousePrice_AI_Project_Report.pdf')

# ==============================================================================
# PART 1: MICROSOFT WORD DOCUMENT (.DOCX) BUILDER
# ==============================================================================
doc = Document()

# Configure Margins & Page Size (A4)
for s in doc.sections:
    s.page_width = Inches(8.27)
    s.page_height = Inches(11.69)
    s.top_margin = Inches(0.7)
    s.bottom_margin = Inches(0.7)
    s.left_margin = Inches(0.8)
    s.right_margin = Inches(0.8)
    s.different_first_page_header_footer = True

def fmt_run(run, font_name="Times New Roman", size_pt=10.5, bold=False, italic=False, color=None):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color

def add_p(doc, text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=3, line_spacing=1.12):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        fmt_run(r, "Times New Roman", 10.5)
    return p

def add_h1(doc, text, space_before=8, space_after=2):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    fmt_run(r, "Times New Roman", 12.5, bold=True, color=RGBColor(15, 23, 42))
    return p

def add_h2(doc, text, space_before=6, space_after=2):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    fmt_run(r, "Times New Roman", 11, bold=True, color=RGBColor(30, 41, 59))
    return p

def add_caption(doc, label, text, space_before=1, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    r1 = p.add_run(label + ": ")
    fmt_run(r1, "Times New Roman", 9, bold=True, color=RGBColor(51, 65, 85))
    r2 = p.add_run(text)
    fmt_run(r2, "Times New Roman", 9, italic=True, color=RGBColor(71, 85, 105))
    return p

# Running Header & Footer for Subsequent Pages
body_header = doc.sections[0].header
hp = body_header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
hrun = hp.add_run("AIML | HousePrice AI – Smart House Price Prediction System")
fmt_run(hrun, "Times New Roman", 8.5, italic=True, color=RGBColor(100, 116, 139))

body_footer = doc.sections[0].footer
fp = body_footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
frun1 = fp.add_run("Department of MCA, NMAM Institute of Technology, Nitte  |  Page ")
fmt_run(frun1, "Times New Roman", 8.5, color=RGBColor(100, 116, 139))
fld_xml = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
fp._p.append(fld_xml)

# ------------------------------------------------------------------------------
# 1. COVER PAGE
# ------------------------------------------------------------------------------
sectPr = doc.sections[0]._sectPr
pgBorders = parse_xml(
    r'<w:pgBorders %s w:offsetFrom="page">'
    r'<w:top w:val="single" w:sz="8" w:space="24" w:color="0F172A"/>'
    r'<w:left w:val="single" w:sz="8" w:space="24" w:color="0F172A"/>'
    r'<w:bottom w:val="single" w:sz="8" w:space="24" w:color="0F172A"/>'
    r'<w:right w:val="single" w:sz="8" w:space="24" w:color="0F172A"/>'
    r'</w:pgBorders>' % nsdecls('w')
)
sectPr.append(pgBorders)

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=4)
r = p.add_run("PROJECT REPORT")
fmt_run(r, "Times New Roman", 15, bold=True, color=RGBColor(15, 23, 42))

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=8)
r = p.add_run("On")
fmt_run(r, "Times New Roman", 12, bold=False)

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=14)
r = p.add_run("HOUSEPRICE AI – SMART HOUSE PRICE PREDICTION SYSTEM\nUSING MULTIPLE LINEAR REGRESSION")
fmt_run(r, "Times New Roman", 15, bold=True, color=RGBColor(15, 23, 42))

if os.path.exists(logo_path):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(4)
    p_logo.paragraph_format.space_after = Pt(12)
    run_logo = p_logo.add_run()
    run_logo.add_picture(logo_path, width=Inches(1.7))

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=1)
r = p.add_run("Submitted by:")
fmt_run(r, "Times New Roman", 11, italic=True)

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=1)
r = p.add_run("[Editable Student Name]")
fmt_run(r, "Times New Roman", 12, bold=True, color=RGBColor(15, 23, 42))

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=10)
r = p.add_run("[Editable USN]")
fmt_run(r, "Times New Roman", 10.5, bold=True, color=RGBColor(71, 85, 105))

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=1)
r = p.add_run("In partial fulfillment of the requirements for the award of the degree of")
fmt_run(r, "Times New Roman", 10, italic=True)

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=10)
r = p.add_run("MASTER OF COMPUTER APPLICATIONS")
fmt_run(r, "Times New Roman", 12.5, bold=True, color=RGBColor(15, 23, 42))

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=1)
r = p.add_run("Under the guidance of:")
fmt_run(r, "Times New Roman", 11, italic=True)

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=14)
r = p.add_run("[Editable Guide Name]")
fmt_run(r, "Times New Roman", 12, bold=True, color=RGBColor(15, 23, 42))

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=1)
r = p.add_run("NMAM INSTITUTE OF TECHNOLOGY, NITTE")
fmt_run(r, "Times New Roman", 12.5, bold=True, color=RGBColor(15, 23, 42))

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=1)
r = p.add_run("(An Autonomous Institution Affiliated to Nitte Deemed to be University)")
fmt_run(r, "Times New Roman", 9.5, italic=True)

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=1)
r = p.add_run("DEPARTMENT OF MASTER OF COMPUTER APPLICATIONS")
fmt_run(r, "Times New Roman", 11, bold=True, color=RGBColor(30, 41, 59))

p = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1, space_after=8)
r = p.add_run("November 2026")
fmt_run(r, "Times New Roman", 10.5, bold=True)

doc.add_page_break()

# ------------------------------------------------------------------------------
# 2. ABSTRACT
# ------------------------------------------------------------------------------
add_h1(doc, "2. Abstract", space_before=6)
add_p(doc, 
    "Accurate residential property valuation is an indispensable prerequisite for transparent real estate transactions, mortgage underwriting, municipal property tax assessment, and investment portfolio risk management. Traditional manual appraisal methodologies frequently suffer from subjective human bias, lack of standardized computational baselines, and temporal valuation latency. This project presents HousePrice AI – Smart House Price Prediction System, an end-to-end Machine Learning web application designed to deliver objective, real-time residential property price estimations strictly leveraging Multiple Linear Regression (MLR) implemented via Scikit-learn's Ordinary Least Squares (OLS) framework. To preserve complete mathematical interpretability, the application utilizes exactly one regression algorithm rather than opaque ensemble trees or deep neural networks. The system is trained on a curated demonstration benchmark dataset comprising 1,800 residential property records across 10 prominent metropolitan micro-markets, capturing super built-up area in square feet, bedroom count, bathroom count, total floors, property age, assigned parking facilities, and geographical location. A Scikit-learn Pipeline with ColumnTransformer is engineered to apply OneHotEncoder to categorical locations (with handle_unknown='ignore') and StandardScaler to continuous numeric features. Rigorous 80:20 train-test partitioning prevents data leakage by fitting transformers strictly on training data. On held-out test data, the trained Multiple Linear Regression model achieves a high coefficient of determination (R² = 0.9404), a Mean Absolute Error (MAE) of ₹ 13,13,652.40, and a Root Mean Squared Error (RMSE) of ₹ 19,02,051.95. The machine learning pipeline is serialized using Joblib and integrated into a Python Flask backend paired with an SQLite database for property listings and prediction audit logging. An intuitive web dashboard built with HTML5, CSS3, Bootstrap 5, and Chart.js surfaces dynamic key performance indicators, four market analytical charts, diagnostic actual-versus-predicted regression lines, and Gaussian residual error distributions. All valuations are presented in Indian Rupees (₹) alongside formal academic disclaimers, successfully demonstrating the practical synergy between rigorous statistical regression modeling and interactive full-stack software engineering."
)

# ------------------------------------------------------------------------------
# 3. INTRODUCTION
# ------------------------------------------------------------------------------
add_h1(doc, "3. Introduction", space_before=6)
add_p(doc, 
    "The residential real estate sector represents one of the most substantial contributors to gross domestic capital formation and personal wealth accumulation globally. Property valuation plays a foundational role in enabling equitable buyer-seller negotiations, securing bank home financing, calculating ad-valorem local taxes, and directing commercial infrastructure investments. However, determining the fair market price of a residential house is inherently multifaceted due to the heterogeneous composition of real estate assets. Unlike standardized commodity markets, no two houses are identical; every home embodies a unique combination of structural physical characteristics, architectural configurations, temporal depreciation, and spatial location premiums."
)
add_p(doc, 
    "Historically, property valuation has relied heavily on comparative market analysis (CMA) executed by certified appraisers or real estate brokers. While human expert intuition remains valuable, manual appraisal processes are susceptible to cognitive bias, selective comparable sampling, and negotiation pressure. Furthermore, manual property evaluations cannot scale to process thousands of simultaneous market listings or provide instant exploratory estimates for prospective homebuyers navigating online portals. Applied machine learning offers a powerful paradigm shift by formalizing property valuation as a multivariate regression task. By analyzing empirical market transactions, machine learning algorithms can learn the underlying mathematical mapping that relates physical and spatial property attributes to final transaction prices."
)
add_p(doc, 
    "Within the spectrum of predictive algorithms, Multiple Linear Regression serves as the gold standard for transparent, explainable modeling. Unlike complex non-linear ensemble models or neural networks whose decision boundaries function as opaque 'black boxes', Multiple Linear Regression explicitly estimates distinct marginal coefficients for every property attribute. This allows appraisers, developers, and students to quantify precisely how much value an additional square foot, an extra bathroom, or a prime neighborhood adds to a home's valuation in Indian Rupees (₹). HousePrice AI was developed to demonstrate this transparent modeling paradigm through an end-to-end, full-stack software system that couples rigorous Scikit-learn statistical modeling with interactive Flask web visualization."
)

# ------------------------------------------------------------------------------
# 4. PROBLEM STATEMENT AND OBJECTIVES
# ------------------------------------------------------------------------------
add_h1(doc, "4. Problem Statement and Objectives", space_before=6)
add_h2(doc, "4.1 Problem Statement")
add_p(doc, 
    "Residential real estate valuation in modern urban centers is characterized by significant price volatility, localized submarket disparities, and widespread information asymmetry. Prospective buyers, independent sellers, and financial institutions frequently lack access to standardized, data-driven valuation tools that compute fair market prices based on quantitative property attributes. Manual estimations conducted by brokers are frequently inconsistent, subjective, and prone to speculative inflation or personal bias. Furthermore, many existing academic machine learning implementations either utilize opaque algorithms without explaining coefficient interpretability or remain isolated as offline Python scripts without a functional, interactive user interface. There is a definitive need for an accessible, mathematically transparent, and fully functional web-based valuation system powered strictly by Multiple Linear Regression."
)
add_h2(doc, "4.2 Project Objectives")
add_p(doc, "To resolve these challenges, the HousePrice AI project was executed with the following core objectives:")
objectives = [
    ("Develop a Machine Learning-Based House Price Prediction System: ", "Engineer an end-to-end web application that accepts user-specified residential property attributes and computes instant, objective market valuations."),
    ("Strictly Apply Multiple Linear Regression: ", "Implement and train exactly one predictive algorithm using Scikit-learn's LinearRegression (Ordinary Least Squares) to maintain total mathematical interpretability without relying on decision trees, random forests, or neural networks."),
    ("Analyze Multi-Dimensional Property Features: ", "Evaluate the simultaneous predictive contributions of super built-up area in square feet, bedroom count, bathroom count, number of floors, property age in years, parking availability, and geographical location categories."),
    ("Prevent Data Leakage via Modular Pipelines: ", "Construct a reproducible Scikit-learn Pipeline incorporating ColumnTransformer to perform categorical one-hot encoding and numeric standard scaling fitted strictly on training data."),
    ("Persist and Manage Valuation Records: ", "Integrate an SQLite relational database to store curated listing records and automatically log all user-generated valuation queries with complete timestamps and record deletion capabilities."),
    ("Deliver an Interactive Real-Estate Analytics Dashboard: ", "Design a modern, responsive user interface utilizing Bootstrap 5 and Chart.js to visualize multi-dimensional market distributions, actual-versus-predicted test regressions, and residual error distributions in Indian Rupees (₹).")
]
for title_obj, desc_obj in objectives:
    p = add_p(doc, space_before=1, space_after=1.5)
    p.paragraph_format.left_indent = Inches(0.18)
    r1 = p.add_run("•  " + title_obj)
    fmt_run(r1, "Times New Roman", 10, bold=True)
    r2 = p.add_run(desc_obj)
    fmt_run(r2, "Times New Roman", 10)

# ------------------------------------------------------------------------------
# 5. TECHNOLOGIES AND TOOLS USED
# ------------------------------------------------------------------------------
add_h1(doc, "5. Technologies and Tools Used", space_before=6)
add_p(doc, 
    "The HousePrice AI project integrates modern, industry-standard open-source libraries across the backend, machine learning, database, and frontend presentation layers. Table 1 enumerates the technologies utilized in the project along with their functional roles."
)

# Table 1: Tech Stack
tbl1 = doc.add_table(rows=1, cols=3)
tbl1.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl1.autofit = False

hdr_cells = tbl1.rows[0].cells
hdr_cells[0].text = "Technology / Tool"
hdr_cells[1].text = "Category"
hdr_cells[2].text = "Functional Role in HousePrice AI"

col_widths = [Inches(1.5), Inches(1.3), Inches(3.7)]
for row in tbl1.rows:
    for i, w in enumerate(col_widths):
        row.cells[i].width = w

for cell in hdr_cells:
    shading_xml = parse_xml(r'<w:shd %s w:fill="0F172A"/>' % nsdecls('w'))
    cell._tc.get_or_add_tcPr().append(shading_xml)
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            fmt_run(r, "Times New Roman", 9.5, bold=True, color=RGBColor(255, 255, 255))

tech_data = [
    ("Python 3.14", "Core Language", "Primary programming environment for machine learning, data engineering, and web execution."),
    ("Scikit-learn 1.8", "Machine Learning", "Implements LinearRegression (OLS), Pipeline, ColumnTransformer, OneHotEncoder, and metrics."),
    ("Pandas 3.0", "Data Processing", "Performs structured tabular data manipulation, CSV ingestion, feature slicing, and descriptive stats."),
    ("NumPy 2.3", "Numerical Engine", "Executes high-performance linear algebra calculations, array operations, and residual histogram binning."),
    ("Flask 3.1", "Backend Web Framework", "Provides WSGI HTTP routing, REST API endpoints (/api/predict, /api/analytics/charts), and Jinja2 rendering."),
    ("SQLite 3", "Relational Database", "Embedded SQL database engine storing 1,800 property listing records and persistent prediction history logs."),
    ("Joblib 1.5", "Model Serialization", "Serializes the complete trained Pipeline (preprocessing + OLS regressor) into house_price_model.joblib."),
    ("HTML5 & CSS3", "Frontend Interface", "Structures semantic web pages and applies a custom real-estate styling system with navy and emerald accents."),
    ("Bootstrap 5.3", "UI Component Library", "Delivers responsive CSS grid layouts, form styling, modal dialogs, navigation bars, and mobile responsiveness."),
    ("Chart.js 4.4", "Data Visualization", "Renders interactive HTML5 Canvas charts: location price bars, area scatter plots, date trends, and residuals."),
    ("Curated Benchmark CSV", "Dataset Source", "Synthetic benchmark residential dataset (1,800 records) modeling realistic Indian metropolitan real-estate metrics.")
]

for tech, cat, role in tech_data:
    row = tbl1.add_row()
    row.cells[0].text = tech
    row.cells[1].text = cat
    row.cells[2].text = role
    for i, w in enumerate(col_widths):
        row.cells[i].width = w
    for i, cell in enumerate(row.cells):
        shading = parse_xml(r'<w:shd %s w:fill="%s"/>' % (nsdecls('w'), "F8FAFC" if len(tbl1.rows) % 2 == 0 else "FFFFFF"))
        cell._tc.get_or_add_tcPr().append(shading)
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            for r in p.runs:
                fmt_run(r, "Times New Roman", 9, bold=(i == 0))

tblPr = tbl1._tbl.tblPr
borders = parse_xml(
    r'<w:tblBorders %s>'
    r'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
    r'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="0F172A"/>'
    r'<w:left w:val="none"/>'
    r'<w:right w:val="none"/>'
    r'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
    r'<w:insideV w:val="none"/>'
    r'</w:tblBorders>' % nsdecls('w')
)
tblPr.append(borders)

add_caption(doc, "Table 1", "Hardware and Software Technology Stack Utilized in HousePrice AI")

# ------------------------------------------------------------------------------
# 6. DATASET
# ------------------------------------------------------------------------------
add_h1(doc, "6. Dataset", space_before=6)
add_p(doc, 
    "To ensure complete academic transparency and integrity, the dataset utilized in this project is explicitly identified as a carefully curated synthetic benchmark demonstration dataset. Rather than presenting procedurally generated numbers as real-world market transactions, the dataset was generated using an authentic domain-informed parametric generator (dataset/generate_dataset.py with a fixed random_state=42). The generator models realistic real-estate price distributions based on Bangalore metropolitan micro-markets, incorporating baseline square footage rates, incremental bedroom/bathroom premiums, floor adjustments, annual age depreciation, assigned parking premiums, and calibrated Gaussian market noise (σ ≈ 4%)."
)
add_p(doc, 
    "The resulting dataset contains exactly 1,800 property records and is stored as dataset/house_prices.csv. Table 2 details the dataset feature architecture, data types, value domains, and statistical summaries."
)

# Table 2: Dataset Features
tbl2 = doc.add_table(rows=1, cols=4)
tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl2.autofit = False

hdr2 = tbl2.rows[0].cells
hdr2[0].text = "Feature Column"
hdr2[1].text = "Data Type"
hdr2[2].text = "Domain / Range"
hdr2[3].text = "Analytical Role & Interpretation"

col_w2 = [Inches(1.4), Inches(1.1), Inches(1.4), Inches(2.6)]
for row in tbl2.rows:
    for i, w in enumerate(col_w2):
        row.cells[i].width = w

for cell in hdr2:
    shading_xml = parse_xml(r'<w:shd %s w:fill="0F172A"/>' % nsdecls('w'))
    cell._tc.get_or_add_tcPr().append(shading_xml)
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            fmt_run(r, "Times New Roman", 9.5, bold=True, color=RGBColor(255, 255, 255))

dataset_features = [
    ("Location", "Categorical (str)", "10 Bangalore zones", "Input feature. Encoded into 10 orthogonal binary columns via OneHotEncoder."),
    ("Area_sqft", "Continuous (int)", "550 – 4,471 sq.ft", "Input feature. Primary physical dimension governing baseline construction value."),
    ("Bedrooms", "Discrete (int)", "1 – 5 BHK", "Input feature. Structural room count reflecting residential accommodation capacity."),
    ("Bathrooms", "Discrete (int)", "1 – 5 baths", "Input feature. Plumbing and sanitation amenity configuration."),
    ("Floors", "Discrete (int)", "1 – 4 floors", "Input feature. Vertical architectural levels of the residential structure."),
    ("Property_Age", "Continuous (int)", "0 – 25 years", "Input feature. Structural depreciation metric (0 denotes brand new construction)."),
    ("Parking", "Binary (int)", "0 (No) or 1 (Yes)", "Input feature. Vehicle parking amenity status (dedicated covered space)."),
    ("Date_Listed", "Temporal (str)", "2025-01-01 to 2026-05", "Auxiliary metadata. Used for chronological time-series price trend analytics."),
    ("Price_INR", "Continuous (int)", "₹ 30.9L – ₹ 5.58 Cr", "Target variable (Y). Total residential market valuation in Indian Rupees (₹).")
]

for col, dtype, rng, desc in dataset_features:
    row = tbl2.add_row()
    row.cells[0].text = col
    row.cells[1].text = dtype
    row.cells[2].text = rng
    row.cells[3].text = desc
    for i, w in enumerate(col_w2):
        row.cells[i].width = w
    for i, cell in enumerate(row.cells):
        shading = parse_xml(r'<w:shd %s w:fill="%s"/>' % (nsdecls('w'), "F8FAFC" if len(tbl2.rows) % 2 == 0 else "FFFFFF"))
        cell._tc.get_or_add_tcPr().append(shading)
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            for r in p.runs:
                fmt_run(r, "Times New Roman", 9, bold=(i == 0))

tblPr2 = tbl2._tbl.tblPr
borders2 = parse_xml(
    r'<w:tblBorders %s>'
    r'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
    r'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="0F172A"/>'
    r'<w:left w:val="none"/>'
    r'<w:right w:val="none"/>'
    r'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
    r'<w:insideV w:val="none"/>'
    r'</w:tblBorders>' % nsdecls('w')
)
tblPr2.append(borders2)

add_caption(doc, "Table 2", "Schema and Description of Dataset Features in HousePrice AI")

add_h2(doc, "6.1 Data Preprocessing and Partitioning")
add_p(doc, 
    "Data integrity and leakage prevention are fundamental to valid machine learning modeling. The dataset was partitioned into 80% training data (1,440 records) and 20% testing data (360 records) using train_test_split with random_state=42. Preprocessing is encapsulated within a unified Scikit-learn ColumnTransformer: (1) Location is encoded using OneHotEncoder(handle_unknown='ignore', sparse_output=False), which constructs orthogonal one-hot indicator columns while gracefully handling unforeseen location categories during live inference; and (2) Continuous numerical features (Area_sqft, Bedrooms, Bathrooms, Floors, Property_Age, and Parking) are scaled using StandardScaler. Crucially, the preprocessor is fitted strictly on the training partition and subsequently applied to transform test and live production queries, completely preventing data leakage."
)

# ------------------------------------------------------------------------------
# 7. METHODOLOGY AND SYSTEM DESIGN
# ------------------------------------------------------------------------------
add_h1(doc, "7. Methodology and System Design", space_before=6)
add_p(doc, 
    "The architectural design of HousePrice AI follows a modular, decoupled engineering pattern spanning eight sequential stages: data ingestion, data preprocessing, feature engineering, categorical encoding, Multiple Linear Regression training, price prediction engine, dynamic results visualization, and user dashboard presentation. Figure 1 depicts the complete system workflow."
)

# Insert Workflow Diagram
if os.path.exists(workflow_path):
    p_wf = doc.add_paragraph()
    p_wf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_wf.paragraph_format.space_before = Pt(4)
    p_wf.paragraph_format.space_after = Pt(2)
    run_wf = p_wf.add_run()
    run_wf.add_picture(workflow_path, width=Inches(5.8))
    add_caption(doc, "Figure 1", "End-to-End Architectural Pipeline of HousePrice AI")

add_p(doc, "The operational workflow proceeds through the following numbered phases:")
workflow_steps = [
    ("Step 1 – Dataset Ingestion & Validation: ", "The curated CSV dataset comprising 1,800 records is loaded using Pandas. Column types, boundary constraints, and non-null guarantees are validated."),
    ("Step 2 – Preprocessing & Column Transformation: ", "Features are routed through Scikit-learn's ColumnTransformer. Location is one-hot encoded and numerical features are standardized to unit variance."),
    ("Step 3 – Partitioning & Leakage Prevention: ", "Data is partitioned into 80% training (1,440 samples) and 20% testing (360 samples) with seed=42. Transformations are fitted strictly on X_train."),
    ("Step 4 – Multiple Linear Regression Fitting: ", "Scikit-learn's LinearRegression estimator is fitted to minimize Ordinary Least Squares (OLS) residual sum of squares across the multi-dimensional feature space."),
    ("Step 5 – Statistical Performance Diagnostics: ", "Predictions on held-out test data are evaluated using MAE, MSE, RMSE, and R² scores. Residual errors (y - ŷ) are analyzed for normality."),
    ("Step 6 – Pipeline Serialization (Joblib): ", "The unified Pipeline containing both fitted preprocessors and the trained regression model is saved to models/house_price_model.joblib for sub-millisecond production inference."),
    ("Step 7 – SQLite Database Synchronization: ", "All 1,800 property records are seeded into the SQLite properties table. An auxiliary predictions table is provisioned for auditing live user predictions."),
    ("Step 8 – Interactive Web Presentation: ", "Flask web routes serve interactive Bootstrap 5 interfaces. Chart.js visualizes dynamic location averages, area scatters, monthly trends, and model residuals.")
]
for step_num, step_desc in workflow_steps:
    p = add_p(doc, space_before=1, space_after=1.5)
    p.paragraph_format.left_indent = Inches(0.18)
    r1 = p.add_run("•  " + step_num)
    fmt_run(r1, "Times New Roman", 10, bold=True)
    r2 = p.add_run(step_desc)
    fmt_run(r2, "Times New Roman", 10)

# ------------------------------------------------------------------------------
# 8. ALGORITHM USED: MULTIPLE LINEAR REGRESSION
# ------------------------------------------------------------------------------
add_h1(doc, "8. Algorithm Used: Multiple Linear Regression", space_before=6)
add_p(doc, 
    "Multiple Linear Regression (MLR) is a supervised parametric machine learning algorithm that models the linear relationship between a continuous scalar dependent variable (target price Y) and two or more independent explanatory variables (X₁, X₂, ..., Xₙ). In accordance with the strict project requirements, MLR is the sole machine learning algorithm implemented in HousePrice AI."
)
add_h2(doc, "8.1 Mathematical Model")
add_p(doc, 
    "The general population regression equation for Multiple Linear Regression is formulated as follows:"
)
p_eq = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=4)
r_eq = p_eq.add_run("Y = β₀ + β₁X₁ + β₂X₂ + β₃X₃ + ... + βₙXₙ + ε")
fmt_run(r_eq, "Times New Roman", 11, bold=True, color=RGBColor(15, 23, 42))

add_p(doc, "Translating this mathematical formulation to the specific features instantiated in HousePrice AI yields:")
p_eq2 = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=4)
r_eq2 = p_eq2.add_run(
    "Price_INR = β₀ + β_Area·(Area_sqft) + β_Beds·(Bedrooms) + β_Baths·(Bathrooms) +\n"
    "β_Floors·(Floors) + β_Age·(Property_Age) + β_Park·(Parking) + Σ [γ_k · Loc_k] + ε"
)
fmt_run(r_eq2, "Times New Roman", 10.5, bold=True, color=RGBColor(30, 41, 59))

add_p(doc, "Where the equation components represent:")
eq_components = [
    ("Y (Price_INR): ", "The continuous dependent target variable denoting estimated property market price in Indian Rupees (₹)."),
    ("β₀ (Intercept): ", "The regression constant representing the expected baseline property valuation when all standardized continuous features equal zero (fitted at ₹ 1,52,54,340)."),
    ("β₁, ..., βₙ (Slopes / Coefficients): ", "The partial regression coefficients measuring the marginal change in house price per unit increase in the corresponding independent feature, holding all other features constant."),
    ("γ_k (Location Coefficients): ", "The discrete valuation adjustments associated with individual one-hot encoded geographical zones relative to reference baselines."),
    ("ε (Residual Error Term): ", "The stochastic error capturing unobserved market variance, assumed to follow an independent normal distribution: ε ~ N(0, σ²).")
]
for comp_title, comp_desc in eq_components:
    p = add_p(doc, space_before=1, space_after=1.5)
    p.paragraph_format.left_indent = Inches(0.18)
    r1 = p.add_run("•  " + comp_title)
    fmt_run(r1, "Times New Roman", 10, bold=True)
    r2 = p.add_run(comp_desc)
    fmt_run(r2, "Times New Roman", 10)

add_h2(doc, "8.2 Ordinary Least Squares (OLS) Optimization")
add_p(doc, 
    "The regression weights β are estimated using Ordinary Least Squares (OLS), which solves for the coefficient vector that minimizes the Residual Sum of Squares (RSS) between observed actual prices y_i and predicted prices ŷ_i across all N training samples:"
)
p_ols = add_p(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=3)
r_ols = p_ols.add_run("RSS = Σ (y_i - ŷ_i)² = (y - Xβ)ᵀ(y - Xβ)")
fmt_run(r_ols, "Times New Roman", 10.5, bold=True, color=RGBColor(15, 23, 42))

add_p(doc, 
    "Taking the matrix derivative with respect to β and setting it to zero yields the closed-form normal equation: β = (XᵀX)⁻¹Xᵀy. Because Scikit-learn's LinearRegression utilizes LAPACK singular value decomposition (SVD), computation is executed with near-instantaneous latency."
)

add_h2(doc, "8.3 Model Evaluation Metrics & Empirical Results")
add_p(doc, 
    "To rigorously assess generalization, the trained model was evaluated strictly against the held-out test dataset (N = 360). Table 3 reports the four required evaluation metrics alongside their statistical definitions and actual empirical values calculated from the project's model_metrics.json file."
)

# Table 3: Performance Metrics
tbl3 = doc.add_table(rows=1, cols=4)
tbl3.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl3.autofit = False

hdr3 = tbl3.rows[0].cells
hdr3[0].text = "Metric"
hdr3[1].text = "Mathematical Definition"
hdr3[2].text = "Empirical Test Result"
hdr3[3].text = "Interpretation & Context"

col_w3 = [Inches(1.2), Inches(1.8), Inches(1.5), Inches(2.0)]
for row in tbl3.rows:
    for i, w in enumerate(col_w3):
        row.cells[i].width = w

for cell in hdr3:
    shading_xml = parse_xml(r'<w:shd %s w:fill="0F172A"/>' % nsdecls('w'))
    cell._tc.get_or_add_tcPr().append(shading_xml)
    for p in cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            fmt_run(r, "Times New Roman", 9.5, bold=True, color=RGBColor(255, 255, 255))

metrics_rows = [
    ("MAE", "MAE = (1/N) Σ |y_i - ŷ_i|", "₹ 13,13,652.40", "Average absolute valuation error on unseen properties."),
    ("MSE", "MSE = (1/N) Σ (y_i - ŷ_i)²", "3.62 × 10¹²", "Mean squared residual variance penalizing larger errors."),
    ("RMSE", "RMSE = √MSE", "₹ 19,02,051.95", "Standard deviation of residuals in original currency units (₹)."),
    ("R-Squared (R²)", "R² = 1 - (SS_res / SS_tot)", "0.9404 (94.04%)", "Proportion of total property price variance explained by MLR.")
]

for mtr, m_def, res_val, interp in metrics_rows:
    row = tbl3.add_row()
    row.cells[0].text = mtr
    row.cells[1].text = m_def
    row.cells[2].text = res_val
    row.cells[3].text = interp
    for i, w in enumerate(col_w3):
        row.cells[i].width = w
    for i, cell in enumerate(row.cells):
        shading = parse_xml(r'<w:shd %s w:fill="%s"/>' % (nsdecls('w'), "F8FAFC" if len(tbl3.rows) % 2 == 0 else "FFFFFF"))
        cell._tc.get_or_add_tcPr().append(shading)
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            for r in p.runs:
                fmt_run(r, "Times New Roman", 9, bold=(i == 0))

tblPr3 = tbl3._tbl.tblPr
borders3 = parse_xml(
    r'<w:tblBorders %s>'
    r'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
    r'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="0F172A"/>'
    r'<w:left w:val="none"/>'
    r'<w:right w:val="none"/>'
    r'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>'
    r'<w:insideV w:val="none"/>'
    r'</w:tblBorders>' % nsdecls('w')
)
tblPr3.append(borders3)

add_caption(doc, "Table 3", "Empirical Evaluation Metrics of Multiple Linear Regression on Held-Out Test Data")

add_p(doc, 
    "Academic Clarification regarding R²: In strict machine learning theory, R² is the coefficient of determination measuring goodness-of-fit for continuous targets; it must never be mislabeled as 'classification accuracy'. An R² score of 0.9404 confirms that approximately 94.04% of the variance in residential property prices is accounted for by our linear combination of structural and spatial features, while the remaining 5.96% represents stochastic market noise. Furthermore, the training R² score was 0.9548, demonstrating healthy generalization with no severe overfitting."
)

# ------------------------------------------------------------------------------
# 9. IMPLEMENTATION
# ------------------------------------------------------------------------------
add_h1(doc, "9. Implementation", space_before=6)
add_p(doc, 
    "The HousePrice AI application is organized into a clean, modular repository structure. The primary functional modules include: (1) train_model.py for dataset partitioning, pipeline construction, and metric export; (2) database/db.py for SQLite database operations and historical prediction storage; (3) app.py for Flask WSGI routing and JSON API endpoints; and (4) templates/ and static/ for frontend UI rendering and Chart.js visualization."
)

add_h2(doc, "9.1 Machine Learning Pipeline (train_model.py)")
add_p(doc, 
    "The training pipeline assembles ColumnTransformer and LinearRegression into a unified Scikit-learn Pipeline object. The code snippet below demonstrates how categorical one-hot encoding and standard scaling are chained with the regressor without data leakage:"
)

p_code1 = add_p(doc, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2, space_after=3)
r_code1 = p_code1.add_run(
    "# Unified Scikit-learn Pipeline Construction\n"
    "preprocessor = ColumnTransformer(\n"
    "    transformers=[\n"
    "        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['Location']),\n"
    "        ('num', StandardScaler(), ['Area_sqft', 'Bedrooms', 'Bathrooms', 'Floors', 'Property_Age', 'Parking'])\n"
    "    ],\n"
    "    remainder='drop'\n"
    ")\n"
    "pipeline = Pipeline(steps=[\n"
    "    ('preprocessor', preprocessor),\n"
    "    ('regressor', LinearRegression(fit_intercept=True))\n"
    "])\n"
    "pipeline.fit(X_train, y_train)\n"
    "joblib.dump(pipeline, 'models/house_price_model.joblib')"
)
fmt_run(r_code1, "Courier New", 8, color=RGBColor(30, 41, 59))
p_code1.paragraph_format.left_indent = Inches(0.18)

add_h2(doc, "9.2 Flask Application Backend (app.py)")
add_p(doc, 
    "The Flask backend exposes seven web routes and two RESTful JSON API endpoints: (1) / or /dashboard renders the executive KPI dashboard and recent valuations; (2) /predict processes property valuation submissions and returns formatted INR prices; (3) /api/predict provides an AJAX endpoint for instant, asynchronous client valuations; (4) /listings supports property search, multi-factor filtering, and pagination across 1,800 records; (5) /analytics and /api/analytics/charts serve market distribution charts; (6) /performance visualizes diagnostic residuals and actual vs. predicted test samples; and (7) /history allows users to view and delete persistent valuation records from SQLite."
)

# ------------------------------------------------------------------------------
# 10. EXPECTED OUTPUT
# ------------------------------------------------------------------------------
add_h1(doc, "10. Expected Output", space_before=6)
add_p(doc, 
    "This section presents authentic graphical user interface screenshots captured directly from the running HousePrice AI web application. Each figure illustrates an active page of the system with genuine dataset values and live Multiple Linear Regression predictions."
)

# Figures with optimized width (Inches(4.8)) to comfortably preserve academic page budget
if os.path.exists(fig2_path):
    p_f2 = doc.add_paragraph()
    p_f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_f2.paragraph_format.space_before = Pt(3)
    p_f2.paragraph_format.space_after = Pt(1)
    run_f2 = p_f2.add_run()
    run_f2.add_picture(fig2_path, width=Inches(4.8))
    add_caption(doc, "Figure 2", "Main Dashboard with Dynamic KPI Cards, Location Price Comparison, and Area-Price Scatter Plot")

if os.path.exists(fig3_path):
    p_f3 = doc.add_paragraph()
    p_f3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_f3.paragraph_format.space_before = Pt(3)
    p_f3.paragraph_format.space_after = Pt(1)
    run_f3 = p_f3.add_run()
    run_f3.add_picture(fig3_path, width=Inches(4.8))
    add_caption(doc, "Figure 3", "Property Valuation Page with Input Specification Form and Live Linear Regression Output Card")

if os.path.exists(fig4_path):
    p_f4 = doc.add_paragraph()
    p_f4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_f4.paragraph_format.space_before = Pt(3)
    p_f4.paragraph_format.space_after = Pt(1)
    run_f4 = p_f4.add_run()
    run_f4.add_picture(fig4_path, width=Inches(4.8))
    add_caption(doc, "Figure 4", "Market Analytics Dashboard Displaying Four Multi-Dimensional Real-Estate Visualization Charts")

if os.path.exists(fig5_path):
    p_f5 = doc.add_paragraph()
    p_f5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_f5.paragraph_format.space_before = Pt(3)
    p_f5.paragraph_format.space_after = Pt(1)
    run_f5 = p_f5.add_run()
    run_f5.add_picture(fig5_path, width=Inches(4.8))
    add_caption(doc, "Figure 5", "Model Performance Dashboard Showing Metric Summary, Actual vs. Predicted Plot, and Residual Histogram")

if os.path.exists(fig6_path):
    p_f6 = doc.add_paragraph()
    p_f6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_f6.paragraph_format.space_before = Pt(3)
    p_f6.paragraph_format.space_after = Pt(1)
    run_f6 = p_f6.add_run()
    run_f6.add_picture(fig6_path, width=Inches(4.8))
    add_caption(doc, "Figure 6", "Prediction History Log Displaying User Valuations Persisted in SQLite with Record Deletion Support")

# ------------------------------------------------------------------------------
# 11. ADVANTAGES AND LIMITATIONS
# ------------------------------------------------------------------------------
add_h1(doc, "11. Advantages and Limitations", space_before=6)
add_h2(doc, "11.1 Advantages")
adv_list = [
    ("Total Mathematical Interpretability: ", "Every regression slope represents an exact financial contribution in Indian Rupees (₹), completely avoiding opaque black-box decisions."),
    ("Leakage-Free Modular Pipeline: ", "Encapsulating OneHotEncoder and StandardScaler inside Scikit-learn's ColumnTransformer ensures sound data hygiene and reproducible production inference."),
    ("Sub-Millisecond Inference Latency: ", "Multiple Linear Regression requires only vector dot products (O(n) complexity), executing predictions in less than 2 milliseconds on standard CPU hardware."),
    ("Comprehensive Full-Stack Integration: ", "Seamlessly connects Scikit-learn statistical modeling with an SQLite database and interactive Chart.js visualizations."),
    ("Robust Categorical Handling: ", "The OneHotEncoder configuration with handle_unknown='ignore' prevents runtime crashes when novel or unseen locations are queried.")
]
for t, d in adv_list:
    p = add_p(doc, space_before=1, space_after=1.5)
    p.paragraph_format.left_indent = Inches(0.18)
    r1 = p.add_run("•  " + t)
    fmt_run(r1, "Times New Roman", 10, bold=True)
    r2 = p.add_run(d)
    fmt_run(r2, "Times New Roman", 10)

add_h2(doc, "11.2 Limitations")
lim_list = [
    ("Assumption of Linearity: ", "Multiple Linear Regression assumes strictly linear relationships between features and prices; complex interaction effects (e.g., luxury super-villas) may be slightly underfitted without polynomial expansion."),
    ("Synthetic Benchmark Data Boundaries: ", "The model is trained on a curated synthetic demonstration dataset (seed=42). While statistically calibrated, synthetic data cannot capture macro-economic interest rate shocks or sudden regulatory changes."),
    ("Absence of Geospatial Micro-Coordinates: ", "Properties are aggregated by discrete zone categories rather than continuous latitude/longitude coordinates or proximity to metro stations."),
    ("Sensitivity to Severe Outliers: ", "Ordinary Least Squares minimizes squared residuals, making parameter estimates somewhat sensitive to extreme statistical anomalies.")
]
for t, d in lim_list:
    p = add_p(doc, space_before=1, space_after=1.5)
    p.paragraph_format.left_indent = Inches(0.18)
    r1 = p.add_run("•  " + t)
    fmt_run(r1, "Times New Roman", 10, bold=True)
    r2 = p.add_run(d)
    fmt_run(r2, "Times New Roman", 10)

# ------------------------------------------------------------------------------
# 12. FUTURE SCOPE
# ------------------------------------------------------------------------------
add_h1(doc, "12. Future Scope", space_before=6)
add_p(doc, 
    "While the current implementation achieves its objective of providing a functional, transparent linear regression valuation system, several promising technical avenues can expand its capabilities:"
)
future_items = [
    ("Real-World Multiple Listing Service (MLS) Integration: ", "Connect the database to real-time real-estate API feeds (e.g., 99acres, MagicBricks) to continuously ingest live market transactions."),
    ("Geospatial Distance Feature Engineering: ", "Incorporate GIS mapping APIs to calculate exact travel times to major IT tech parks, metro stations, international airports, and hospitals."),
    ("Polynomial & Regularized Regression Benchmarking: ", "Implement Ridge (L2) and Lasso (L1) regression variants with cross-validated hyperparameter tuning to benchmark feature shrinkage and multi-collinearity control."),
    ("Automated Comparable Property Matcher: ", "Develop a nearest-neighbor Euclidean distance recommender to display the top three most similar historical properties alongside each price prediction."),
    ("Cloud Containerization & Production Deployment: ", "Package the application into lightweight Docker containers and deploy onto AWS or Google Cloud Run with automated CI/CD pipelines.")
]
for t, d in future_items:
    p = add_p(doc, space_before=1, space_after=1.5)
    p.paragraph_format.left_indent = Inches(0.18)
    r1 = p.add_run("•  " + t)
    fmt_run(r1, "Times New Roman", 10, bold=True)
    r2 = p.add_run(d)
    fmt_run(r2, "Times New Roman", 10)

# ------------------------------------------------------------------------------
# 13. CONCLUSION
# ------------------------------------------------------------------------------
add_h1(doc, "13. Conclusion", space_before=6)
add_p(doc, 
    "The HousePrice AI project successfully demonstrates the design, empirical training, diagnostic evaluation, and full-stack deployment of a residential property price prediction system powered strictly by Multiple Linear Regression. By adhering to the single-algorithm constraint, the project exemplifies the enduring value of statistical interpretability in applied machine learning. Rather than treating property valuation as an impenetrable black-box, the trained Ordinary Least Squares model makes every marginal feature coefficient explicit, providing understandable valuations in Indian Rupees (₹)."
)
add_p(doc, 
    "Rigorous data engineering practices—including reproducible 80:20 train-test partitioning, ColumnTransformer-based categorical one-hot encoding, and train-only standard scaling—ensured that the model completely avoids data leakage. On held-out testing data, the model achieved an impressive R² score of 0.9404, an MAE of ₹ 13,13,652.40, and an RMSE of ₹ 19,02,051.95, while residual diagnostics confirmed an unbiased Gaussian error distribution. Integrating the serialized Joblib pipeline into a responsive Flask web application supported by SQLite persistence and dynamic Chart.js visualizations bridges the gap between academic statistical theory and practical software engineering. HousePrice AI stands as a robust, fully functional academic project that illustrates how classical machine learning algorithms can solve meaningful real-world valuation challenges."
)

# ------------------------------------------------------------------------------
# 14. REFERENCES
# ------------------------------------------------------------------------------
add_h1(doc, "14. References", space_before=6)
references = [
    ("F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, et al., \"Scikit-learn: Machine Learning in Python,\" ", "Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011."),
    ("D. C. Montgomery, E. A. Peck, and G. G. Vining, ", "Introduction to Linear Regression Analysis, 6th ed., Hoboken, NJ: John Wiley & Sons, 2021."),
    ("W. McKinney, \"Data Structures for Statistical Computing in Python,\" ", "in Proceedings of the 9th Python in Science Conference (SciPy 2010), pp. 56–61, 2010."),
    ("C. R. Harris, K. J. Millman, S. J. van der Walt, R. Gommers, P. Virtanen, et al., \"Array programming with NumPy,\" ", "Nature, vol. 585, no. 7825, pp. 357–362, 2020."),
    ("G. James, D. Witten, T. Hastie, and R. Tibshirani, ", "An Introduction to Statistical Learning: with Applications in R, 2nd ed., New York, NY: Springer, 2021."),
    ("Pallets Projects, \"Flask Documentation (v3.1.x): Web Development, One Drop at a Time,\" ", "https://flask.palletsprojects.com"),
    ("Scikit-learn Documentation, \"Linear Models: Ordinary Least Squares & Multiple Regression,\" ", "https://scikit-learn.org/stable/modules/linear_model.html"),
    ("Chart.js Documentation, \"Open-source HTML5 Canvas Charts for Modern Web Applications (v4.4),\" ", "https://www.chartjs.org/docs/latest/"),
    ("SQLite Consortium, \"SQLite Database Engine Official Documentation (v3.x),\" ", "https://www.sqlite.org/docs.html")
]
for ref_part1, ref_part2 in references:
    p = add_p(doc, space_before=1, space_after=1.5)
    p.paragraph_format.left_indent = Inches(0.18)
    r1 = p.add_run("•  " + ref_part1)
    fmt_run(r1, "Times New Roman", 9.5)
    r2 = p.add_run(ref_part2)
    fmt_run(r2, "Times New Roman", 9.5, italic=True)

# Save Word Document safely
try:
    doc.save(docx_output_path)
    print(f"Generated DOCX: {docx_output_path} ({os.path.getsize(docx_output_path)} bytes)")
except PermissionError:
    alt_docx_path = os.path.join(base_dir, 'HousePrice_AI_Project_Report_Final.docx')
    doc.save(alt_docx_path)
    print(f"HousePrice_AI_Project_Report.docx is currently open in Word. Saved updated copy to: {alt_docx_path} ({os.path.getsize(alt_docx_path)} bytes)")

# ==============================================================================
# PART 2: GENERATE MATCHING HIGH-FIDELITY PDF VIA HEADLESS CHROME
# ==============================================================================
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HousePrice AI - Project Report</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 15mm 16mm 15mm 16mm;
    @top-right {{
      content: "AIML | HousePrice AI – Smart House Price Prediction System";
      font-family: "Times New Roman", Times, serif;
      font-size: 8pt;
      font-style: italic;
      color: #64748b;
    }}
    @bottom-right {{
      content: "Department of MCA, NMAM Institute of Technology, Nitte  |  Page " counter(page);
      font-family: "Times New Roman", Times, serif;
      font-size: 8pt;
      color: #64748b;
    }}
  }}

  body {{
    font-family: "Times New Roman", Times, Georgia, serif;
    font-size: 10pt;
    line-height: 1.2;
    color: #0f172a;
    margin: 0;
    padding: 0;
    text-align: justify;
  }}

  .cover-page {{
    page-break-after: always;
    border: 2px solid #0f172a;
    padding: 24px 18px;
    box-sizing: border-box;
    text-align: center;
    height: 980px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .cover-title {{
    font-size: 16pt;
    font-weight: bold;
    color: #0f172a;
    margin: 8px 0 4px 0;
    line-height: 1.2;
    text-transform: uppercase;
  }}

  .cover-subtitle {{
    font-size: 12pt;
    font-style: italic;
    color: #334155;
    margin: 2px 0 10px 0;
  }}

  .cover-project-name {{
    font-size: 15pt;
    font-weight: bold;
    color: #0f172a;
    margin: 10px 0;
    line-height: 1.3;
  }}

  .cover-logo {{
    margin: 8px auto;
    max-width: 160px;
    display: block;
  }}

  .cover-section-label {{
    font-size: 10pt;
    font-style: italic;
    color: #475569;
    margin-bottom: 2px;
  }}

  .cover-student-name {{
    font-size: 12pt;
    font-weight: bold;
    color: #0f172a;
  }}

  .cover-degree {{
    font-size: 12.5pt;
    font-weight: bold;
    color: #0f172a;
    margin: 4px 0;
  }}

  .cover-college {{
    font-size: 12.5pt;
    font-weight: bold;
    color: #0f172a;
    margin-top: 6px;
  }}

  .cover-dept {{
    font-size: 11pt;
    font-weight: bold;
    color: #1e293b;
  }}

  .cover-date {{
    font-size: 10pt;
    font-weight: bold;
    color: #334155;
    margin-top: 4px;
  }}

  h1 {{
    font-size: 12pt;
    font-weight: bold;
    color: #0f172a;
    margin-top: 10px;
    margin-bottom: 3px;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 2px;
    page-break-after: avoid;
  }}

  h2 {{
    font-size: 10.5pt;
    font-weight: bold;
    color: #1e293b;
    margin-top: 8px;
    margin-bottom: 2px;
    page-break-after: avoid;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 4px;
    text-align: justify;
    text-justify: inter-word;
  }}

  ul {{
    margin-top: 2px;
    margin-bottom: 4px;
    padding-left: 18px;
  }}

  li {{
    margin-bottom: 2px;
    font-size: 9.8pt;
  }}

  .math-box {{
    text-align: center;
    font-weight: bold;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 4px 10px;
    margin: 4px 0;
    font-size: 10pt;
    color: #0f172a;
  }}

  .code-box {{
    background: #f1f5f9;
    border-left: 3px solid #0f172a;
    padding: 5px 8px;
    font-family: "Courier New", Courier, monospace;
    font-size: 8pt;
    margin: 4px 0;
    white-space: pre-wrap;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0;
    font-size: 9pt;
  }}

  th {{
    background-color: #0f172a;
    color: #ffffff;
    font-weight: bold;
    text-align: left;
    padding: 4px 6px;
    border-top: 1px solid #0f172a;
    border-bottom: 2px solid #0f172a;
  }}

  td {{
    padding: 3px 6px;
    border-bottom: 1px solid #e2e8f0;
    vertical-align: top;
  }}

  tr:nth-child(even) td {{
    background-color: #f8fafc;
  }}

  .caption {{
    text-align: center;
    font-size: 8.5pt;
    font-style: italic;
    color: #475569;
    margin-top: 2px;
    margin-bottom: 6px;
  }}

  .caption strong {{
    font-style: normal;
    color: #0f172a;
  }}

  .figure-img {{
    display: block;
    margin: 4px auto 1px auto;
    max-width: 72%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    page-break-inside: avoid;
  }}

  .header-rule {{
    display: flex;
    justify-content: flex-end;
    font-size: 8pt;
    font-style: italic;
    color: #64748b;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 2px;
    margin-bottom: 8px;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div>
    <div class="cover-title">PROJECT REPORT</div>
    <div class="cover-subtitle">On</div>
    <div class="cover-project-name">
      HOUSEPRICE AI – SMART HOUSE PRICE PREDICTION SYSTEM<br>
      USING MULTIPLE LINEAR REGRESSION
    </div>
  </div>

  <div>
    <img src="file:///{logo_path.replace(os.sep, '/')}" class="cover-logo" alt="Nitte Logo">
  </div>

  <div>
    <div class="cover-section-label">Submitted by:</div>
    <div class="cover-student-name">[Editable Student Name]</div>
    <div style="font-size:10.5pt; font-weight:bold; color:#475569;">[Editable USN]</div>
  </div>

  <div>
    <div class="cover-section-label">In partial fulfillment of the requirements for the award of the degree of</div>
    <div class="cover-degree">MASTER OF COMPUTER APPLICATIONS</div>
  </div>

  <div>
    <div class="cover-section-label">Under the guidance of:</div>
    <div class="cover-student-name">[Editable Guide Name]</div>
  </div>

  <div style="border-top:1px solid #cbd5e1; padding-top:6px;">
    <div class="cover-college">NMAM INSTITUTE OF TECHNOLOGY, NITTE</div>
    <div style="font-size:9pt; font-style:italic; color:#475569;">(An Autonomous Institution Affiliated to Nitte Deemed to be University)</div>
    <div class="cover-dept">DEPARTMENT OF MASTER OF COMPUTER APPLICATIONS</div>
    <div class="cover-date">November 2026</div>
  </div>
</div>

<!-- PAGE 2 ONWARDS BODY CONTENT -->
<div class="header-rule">AIML | HousePrice AI – Smart House Price Prediction System</div>

<h1>2. Abstract</h1>
<p>
Accurate residential property valuation is an indispensable prerequisite for transparent real estate transactions, mortgage underwriting, municipal property tax assessment, and investment portfolio risk management. Traditional manual appraisal methodologies frequently suffer from subjective human bias, lack of standardized computational baselines, and temporal valuation latency. This project presents HousePrice AI – Smart House Price Prediction System, an end-to-end Machine Learning web application designed to deliver objective, real-time residential property price estimations strictly leveraging Multiple Linear Regression (MLR) implemented via Scikit-learn's Ordinary Least Squares (OLS) framework. To preserve complete mathematical interpretability, the application utilizes exactly one regression algorithm rather than opaque ensemble trees or deep neural networks. The system is trained on a curated demonstration benchmark dataset comprising 1,800 residential property records across 10 prominent metropolitan micro-markets, capturing super built-up area in square feet, bedroom count, bathroom count, total floors, property age, assigned parking facilities, and geographical location. A Scikit-learn Pipeline with ColumnTransformer is engineered to apply OneHotEncoder to categorical locations (with handle_unknown='ignore') and StandardScaler to continuous numeric features. Rigorous 80:20 train-test partitioning prevents data leakage by fitting transformers strictly on training data. On held-out test data, the trained Multiple Linear Regression model achieves a high coefficient of determination (R² = 0.9404), a Mean Absolute Error (MAE) of ₹ 13,13,652.40, and a Root Mean Squared Error (RMSE) of ₹ 19,02,051.95. The machine learning pipeline is serialized using Joblib and integrated into a Python Flask backend paired with an SQLite database for property listings and prediction audit logging. An intuitive web dashboard built with HTML5, CSS3, Bootstrap 5, and Chart.js surfaces dynamic key performance indicators, four market analytical charts, diagnostic actual-versus-predicted regression lines, and Gaussian residual error distributions. All valuations are presented in Indian Rupees (₹) alongside formal academic disclaimers, successfully demonstrating the practical synergy between rigorous statistical regression modeling and interactive full-stack software engineering.
</p>

<h1>3. Introduction</h1>
<p>
The residential real estate sector represents one of the most substantial contributors to gross domestic capital formation and personal wealth accumulation globally. Property valuation plays a foundational role in enabling equitable buyer-seller negotiations, securing bank home financing, calculating ad-valorem local taxes, and directing commercial infrastructure investments. However, determining the fair market price of a residential house is inherently multifaceted due to the heterogeneous composition of real estate assets. Unlike standardized commodity markets, no two houses are identical; every home embodies a unique combination of structural physical characteristics, architectural configurations, temporal depreciation, and spatial location premiums.
</p>
<p>
Historically, property valuation has relied heavily on comparative market analysis (CMA) executed by certified appraisers or real estate brokers. While human expert intuition remains valuable, manual appraisal processes are susceptible to cognitive bias, selective comparable sampling, and negotiation pressure. Furthermore, manual property evaluations cannot scale to process thousands of simultaneous market listings or provide instant exploratory estimates for prospective homebuyers navigating online portals. Applied machine learning offers a powerful paradigm shift by formalizing property valuation as a multivariate regression task. By analyzing empirical market transactions, machine learning algorithms can learn the underlying mathematical mapping that relates physical and spatial property attributes to final transaction prices.
</p>
<p>
Within the spectrum of predictive algorithms, Multiple Linear Regression serves as the gold standard for transparent, explainable modeling. Unlike complex non-linear ensemble models or neural networks whose decision boundaries function as opaque 'black boxes', Multiple Linear Regression explicitly estimates distinct marginal coefficients for every property attribute. This allows appraisers, developers, and students to quantify precisely how much value an additional square foot, an extra bathroom, or a prime neighborhood adds to a home's valuation in Indian Rupees (₹). HousePrice AI was developed to demonstrate this transparent modeling paradigm through an end-to-end, full-stack software system that couples rigorous Scikit-learn statistical modeling with interactive Flask web visualization.
</p>

<h1>4. Problem Statement and Objectives</h1>
<h2>4.1 Problem Statement</h2>
<p>
Residential real estate valuation in modern urban centers is characterized by significant price volatility, localized submarket disparities, and widespread information asymmetry. Prospective buyers, independent sellers, and financial institutions frequently lack access to standardized, data-driven valuation tools that compute fair market prices based on quantitative property attributes. Manual estimations conducted by brokers are frequently inconsistent, subjective, and prone to speculative inflation or personal bias. Furthermore, many existing academic machine learning implementations either utilize opaque algorithms without explaining coefficient interpretability or remain isolated as offline Python scripts without a functional, interactive user interface. There is a definitive need for an accessible, mathematically transparent, and fully functional web-based valuation system powered strictly by Multiple Linear Regression.
</p>

<h2>4.2 Project Objectives</h2>
<p>To resolve these challenges, the HousePrice AI project was executed with the following core objectives:</p>
<ul>
  <li><strong>Develop a Machine Learning-Based House Price Prediction System:</strong> Engineer an end-to-end web application that accepts user-specified residential property attributes and computes instant, objective market valuations.</li>
  <li><strong>Strictly Apply Multiple Linear Regression:</strong> Implement and train exactly one predictive algorithm using Scikit-learn's LinearRegression (Ordinary Least Squares) to maintain total mathematical interpretability without relying on decision trees, random forests, or neural networks.</li>
  <li><strong>Analyze Multi-Dimensional Property Features:</strong> Evaluate the simultaneous predictive contributions of super built-up area in square feet, bedroom count, bathroom count, number of floors, property age in years, parking availability, and geographical location categories.</li>
  <li><strong>Prevent Data Leakage via Modular Pipelines:</strong> Construct a reproducible Scikit-learn Pipeline incorporating ColumnTransformer to perform categorical one-hot encoding and numeric standard scaling fitted strictly on training data.</li>
  <li><strong>Persist and Manage Valuation Records:</strong> Integrate an SQLite relational database to store curated listing records and automatically log all user-generated valuation queries with complete timestamps and record deletion capabilities.</li>
  <li><strong>Deliver an Interactive Real-Estate Analytics Dashboard:</strong> Design a modern, responsive user interface utilizing Bootstrap 5 and Chart.js to visualize multi-dimensional market distributions, actual-versus-predicted test regressions, and residual error distributions in Indian Rupees (₹).</li>
</ul>

<h1>5. Technologies and Tools Used</h1>
<p>
The HousePrice AI project integrates modern, industry-standard open-source libraries across the backend, machine learning, database, and frontend presentation layers. Table 1 enumerates the technologies utilized in the project along with their functional roles.
</p>

<table>
  <thead>
    <tr>
      <th style="width:22%;">Technology / Tool</th>
      <th style="width:20%;">Category</th>
      <th style="width:58%;">Functional Role in HousePrice AI</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><strong>Python 3.14</strong></td><td>Core Language</td><td>Primary programming environment for machine learning, data engineering, and web execution.</td></tr>
    <tr><td><strong>Scikit-learn 1.8</strong></td><td>Machine Learning</td><td>Implements LinearRegression (OLS), Pipeline, ColumnTransformer, OneHotEncoder, and metrics.</td></tr>
    <tr><td><strong>Pandas 3.0</strong></td><td>Data Processing</td><td>Performs structured tabular data manipulation, CSV ingestion, feature slicing, and descriptive stats.</td></tr>
    <tr><td><strong>NumPy 2.3</strong></td><td>Numerical Engine</td><td>Executes high-performance linear algebra calculations, array operations, and residual histogram binning.</td></tr>
    <tr><td><strong>Flask 3.1</strong></td><td>Backend Web Framework</td><td>Provides WSGI HTTP routing, REST API endpoints (/api/predict, /api/analytics/charts), and Jinja2 rendering.</td></tr>
    <tr><td><strong>SQLite 3</strong></td><td>Relational Database</td><td>Embedded SQL database engine storing 1,800 property listing records and persistent prediction history logs.</td></tr>
    <tr><td><strong>Joblib 1.5</strong></td><td>Model Serialization</td><td>Serializes the complete trained Pipeline (preprocessing + OLS regressor) into house_price_model.joblib.</td></tr>
    <tr><td><strong>HTML5 & CSS3</strong></td><td>Frontend Interface</td><td>Structures semantic web pages and applies a custom real-estate styling system with navy and emerald accents.</td></tr>
    <tr><td><strong>Bootstrap 5.3</strong></td><td>UI Component Library</td><td>Delivers responsive CSS grid layouts, form styling, modal dialogs, navigation bars, and mobile responsiveness.</td></tr>
    <tr><td><strong>Chart.js 4.4</strong></td><td>Data Visualization</td><td>Renders interactive HTML5 Canvas charts: location price bars, area scatter plots, date trends, and residuals.</td></tr>
    <tr><td><strong>Curated Benchmark CSV</strong></td><td>Dataset Source</td><td>Synthetic benchmark residential dataset (1,800 records) modeling realistic Indian metropolitan real-estate metrics.</td></tr>
  </tbody>
</table>
<div class="caption"><strong>Table 1:</strong> Hardware and Software Technology Stack Utilized in HousePrice AI</div>

<h1>6. Dataset</h1>
<p>
To ensure complete academic transparency and integrity, the dataset utilized in this project is explicitly identified as a carefully curated synthetic benchmark demonstration dataset. Rather than presenting procedurally generated numbers as real-world market transactions, the dataset was generated using an authentic domain-informed parametric generator (dataset/generate_dataset.py with a fixed random_state=42). The generator models realistic real-estate price distributions based on Bangalore metropolitan micro-markets, incorporating baseline square footage rates, incremental bedroom/bathroom premiums, floor adjustments, annual age depreciation, assigned parking premiums, and calibrated Gaussian market noise (σ ≈ 4%).
</p>
<p>
The resulting dataset contains exactly 1,800 property records and is stored as dataset/house_prices.csv. Table 2 details the dataset feature architecture, data types, value domains, and statistical summaries.
</p>

<table>
  <thead>
    <tr>
      <th style="width:20%;">Feature Column</th>
      <th style="width:18%;">Data Type</th>
      <th style="width:22%;">Domain / Range</th>
      <th style="width:40%;">Analytical Role & Interpretation</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><strong>Location</strong></td><td>Categorical (str)</td><td>10 Bangalore zones</td><td>Input feature. Encoded into 10 orthogonal binary columns via OneHotEncoder.</td></tr>
    <tr><td><strong>Area_sqft</strong></td><td>Continuous (int)</td><td>550 – 4,471 sq.ft</td><td>Input feature. Primary physical dimension governing baseline construction value.</td></tr>
    <tr><td><strong>Bedrooms</strong></td><td>Discrete (int)</td><td>1 – 5 BHK</td><td>Input feature. Structural room count reflecting residential accommodation capacity.</td></tr>
    <tr><td><strong>Bathrooms</strong></td><td>Discrete (int)</td><td>1 – 5 baths</td><td>Input feature. Plumbing and sanitation amenity configuration.</td></tr>
    <tr><td><strong>Floors</strong></td><td>Discrete (int)</td><td>1 – 4 floors</td><td>Input feature. Vertical architectural levels of the residential structure.</td></tr>
    <tr><td><strong>Property_Age</strong></td><td>Continuous (int)</td><td>0 – 25 years</td><td>Input feature. Structural depreciation metric (0 denotes brand new construction).</td></tr>
    <tr><td><strong>Parking</strong></td><td>Binary (int)</td><td>0 (No) or 1 (Yes)</td><td>Input feature. Vehicle parking amenity status (dedicated covered space).</td></tr>
    <tr><td><strong>Date_Listed</strong></td><td>Temporal (str)</td><td>2025-01-01 to 2026-05</td><td>Auxiliary metadata. Used for chronological time-series price trend analytics.</td></tr>
    <tr><td><strong>Price_INR</strong></td><td>Continuous (int)</td><td>₹ 30.9L – ₹ 5.58 Cr</td><td>Target variable (Y). Total residential market valuation in Indian Rupees (₹).</td></tr>
  </tbody>
</table>
<div class="caption"><strong>Table 2:</strong> Schema and Description of Dataset Features in HousePrice AI</div>

<h2>6.1 Data Preprocessing and Partitioning</h2>
<p>
Data integrity and leakage prevention are fundamental to valid machine learning modeling. The dataset was partitioned into 80% training data (1,440 records) and 20% testing data (360 records) using train_test_split with random_state=42. Preprocessing is encapsulated within a unified Scikit-learn ColumnTransformer: (1) Location is encoded using OneHotEncoder(handle_unknown='ignore', sparse_output=False), which constructs orthogonal one-hot indicator columns while gracefully handling unforeseen location categories during live inference; and (2) Continuous numerical features (Area_sqft, Bedrooms, Bathrooms, Floors, Property_Age, and Parking) are scaled using StandardScaler. Crucially, the preprocessor is fitted strictly on the training partition and subsequently applied to transform test and live production queries, completely preventing data leakage.
</p>

<h1>7. Methodology and System Design</h1>
<p>
The architectural design of HousePrice AI follows a modular, decoupled engineering pattern spanning eight sequential stages: data ingestion, data preprocessing, feature engineering, categorical encoding, Multiple Linear Regression training, price prediction engine, dynamic results visualization, and user dashboard presentation. Figure 1 depicts the complete system workflow.
</p>

<img src="file:///{workflow_path.replace(os.sep, '/')}" class="figure-img" alt="Workflow Diagram">
<div class="caption"><strong>Figure 1:</strong> End-to-End Architectural Pipeline of HousePrice AI</div>

<p>The operational workflow proceeds through the following numbered phases:</p>
<ul>
  <li><strong>Step 1 – Dataset Ingestion & Validation:</strong> The curated CSV dataset comprising 1,800 records is loaded using Pandas. Column types, boundary constraints, and non-null guarantees are validated.</li>
  <li><strong>Step 2 – Preprocessing & Column Transformation:</strong> Features are routed through Scikit-learn's ColumnTransformer. Location is one-hot encoded and numerical features are standardized to unit variance.</li>
  <li><strong>Step 3 – Partitioning & Leakage Prevention:</strong> Data is partitioned into 80% training (1,440 samples) and 20% testing (360 samples) with seed=42. Transformations are fitted strictly on X_train.</li>
  <li><strong>Step 4 – Multiple Linear Regression Fitting:</strong> Scikit-learn's LinearRegression estimator is fitted to minimize Ordinary Least Squares (OLS) residual sum of squares across the multi-dimensional feature space.</li>
  <li><strong>Step 5 – Statistical Performance Diagnostics:</strong> Predictions on held-out test data are evaluated using MAE, MSE, RMSE, and R² scores. Residual errors (y - ŷ) are analyzed for normality.</li>
  <li><strong>Step 6 – Pipeline Serialization (Joblib):</strong> The unified Pipeline containing both fitted preprocessors and the trained regression model is saved to models/house_price_model.joblib for sub-millisecond production inference.</li>
  <li><strong>Step 7 – SQLite Database Synchronization:</strong> All 1,800 property records are seeded into the SQLite properties table. An auxiliary predictions table is provisioned for auditing live user predictions.</li>
  <li><strong>Step 8 – Interactive Web Presentation:</strong> Flask web routes serve interactive Bootstrap 5 interfaces. Chart.js visualizes dynamic location averages, area scatters, monthly trends, and model residuals.</li>
</ul>

<h1>8. Algorithm Used: Multiple Linear Regression</h1>
<p>
Multiple Linear Regression (MLR) is a supervised parametric machine learning algorithm that models the linear relationship between a continuous scalar dependent variable (target price Y) and two or more independent explanatory variables (X₁, X₂, ..., Xₙ). In accordance with the strict project requirements, MLR is the sole machine learning algorithm implemented in HousePrice AI.
</p>

<h2>8.1 Mathematical Model</h2>
<p>The general population regression equation for Multiple Linear Regression is formulated as follows:</p>
<div class="math-box">Y = β₀ + β₁X₁ + β₂X₂ + β₃X₃ + ... + βₙXₙ + ε</div>

<p>Translating this mathematical formulation to the specific features instantiated in HousePrice AI yields:</p>
<div class="math-box">
Price_INR = β₀ + β_Area·(Area_sqft) + β_Beds·(Bedrooms) + β_Baths·(Bathrooms) + β_Floors·(Floors) + β_Age·(Property_Age) + β_Park·(Parking) + Σ [γ_k · Loc_k] + ε
</div>

<p>Where the equation components represent:</p>
<ul>
  <li><strong>Y (Price_INR):</strong> The continuous dependent target variable denoting estimated property market price in Indian Rupees (₹).</li>
  <li><strong>β₀ (Intercept):</strong> The regression constant representing the expected baseline property valuation when all standardized continuous features equal zero (fitted at ₹ 1,52,54,340).</li>
  <li><strong>β₁, ..., βₙ (Slopes / Coefficients):</strong> The partial regression coefficients measuring the marginal change in house price per unit increase in the corresponding independent feature, holding all other features constant.</li>
  <li><strong>γ_k (Location Coefficients):</strong> The discrete valuation adjustments associated with individual one-hot encoded geographical zones relative to reference baselines.</li>
  <li><strong>ε (Residual Error Term):</strong> The stochastic error capturing unobserved market variance, assumed to follow an independent normal distribution: ε ~ N(0, σ²).</li>
</ul>

<h2>8.2 Ordinary Least Squares (OLS) Optimization</h2>
<p>
The regression weights β are estimated using Ordinary Least Squares (OLS), which solves for the coefficient vector that minimizes the Residual Sum of Squares (RSS) between observed actual prices y_i and predicted prices ŷ_i across all N training samples:
</p>
<div class="math-box">RSS = Σ (y_i - ŷ_i)² = (y - Xβ)ᵀ(y - Xβ)</div>
<p>
Taking the matrix derivative with respect to β and setting it to zero yields the closed-form normal equation: β = (XᵀX)⁻¹Xᵀy. Because Scikit-learn's LinearRegression utilizes LAPACK singular value decomposition (SVD), computation is executed with near-instantaneous latency.
</p>

<h2>8.3 Model Evaluation Metrics & Empirical Results</h2>
<p>
To rigorously assess generalization, the trained model was evaluated strictly against the held-out test dataset (N = 360). Table 3 reports the four required evaluation metrics alongside their statistical definitions and actual empirical values calculated from the project's model_metrics.json file.
</p>

<table>
  <thead>
    <tr>
      <th style="width:18%;">Metric</th>
      <th style="width:28%;">Mathematical Definition</th>
      <th style="width:24%;">Empirical Test Result</th>
      <th style="width:30%;">Interpretation & Context</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><strong>MAE</strong></td><td>MAE = (1/N) Σ |y_i - ŷ_i|</td><td>₹ 13,13,652.40</td><td>Average absolute valuation error on unseen properties.</td></tr>
    <tr><td><strong>MSE</strong></td><td>MSE = (1/N) Σ (y_i - ŷ_i)²</td><td>3.62 × 10¹²</td><td>Mean squared residual variance penalizing larger errors.</td></tr>
    <tr><td><strong>RMSE</strong></td><td>RMSE = √MSE</td><td>₹ 19,02,051.95</td><td>Standard deviation of residuals in original currency units (₹).</td></tr>
    <tr><td><strong>R-Squared (R²)</strong></td><td>R² = 1 - (SS_res / SS_tot)</td><td>0.9404 (94.04%)</td><td>Proportion of total property price variance explained by MLR.</td></tr>
  </tbody>
</table>
<div class="caption"><strong>Table 3:</strong> Empirical Evaluation Metrics of Multiple Linear Regression on Held-Out Test Data</div>

<p>
<strong>Academic Clarification regarding R²:</strong> In strict machine learning theory, R² is the coefficient of determination measuring goodness-of-fit for continuous targets; it must never be mislabeled as 'classification accuracy'. An R² score of 0.9404 confirms that approximately 94.04% of the variance in residential property prices is accounted for by our linear combination of structural and spatial features, while the remaining 5.96% represents stochastic market noise. Furthermore, the training R² score was 0.9548, demonstrating healthy generalization with no severe overfitting.
</p>

<h1>9. Implementation</h1>
<p>
The HousePrice AI application is organized into a clean, modular repository structure. The primary functional modules include: (1) train_model.py for dataset partitioning, pipeline construction, and metric export; (2) database/db.py for SQLite database operations and historical prediction storage; (3) app.py for Flask WSGI routing and JSON API endpoints; and (4) templates/ and static/ for frontend UI rendering and Chart.js visualization.
</p>

<h2>9.1 Machine Learning Pipeline (train_model.py)</h2>
<p>
The training pipeline assembles ColumnTransformer and LinearRegression into a unified Scikit-learn Pipeline object. The code snippet below demonstrates how categorical one-hot encoding and standard scaling are chained with the regressor without data leakage:
</p>
<div class="code-box"># Unified Scikit-learn Pipeline Construction
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['Location']),
        ('num', StandardScaler(), ['Area_sqft', 'Bedrooms', 'Bathrooms', 'Floors', 'Property_Age', 'Parking'])
    ],
    remainder='drop'
)
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression(fit_intercept=True))
])
pipeline.fit(X_train, y_train)
joblib.dump(pipeline, 'models/house_price_model.joblib')</div>

<h2>9.2 Flask Application Backend (app.py)</h2>
<p>
The Flask backend exposes seven web routes and two RESTful JSON API endpoints: (1) / or /dashboard renders the executive KPI dashboard and recent valuations; (2) /predict processes property valuation submissions and returns formatted INR prices; (3) /api/predict provides an AJAX endpoint for instant, asynchronous client valuations; (4) /listings supports property search, multi-factor filtering, and pagination across 1,800 records; (5) /analytics and /api/analytics/charts serve market distribution charts; (6) /performance visualizes diagnostic residuals and actual vs. predicted test samples; and (7) /history allows users to view and delete persistent valuation records from SQLite.
</p>

<h1>10. Expected Output</h1>
<p>
This section presents authentic graphical user interface screenshots captured directly from the running HousePrice AI web application. Each figure illustrates an active page of the system with genuine dataset values and live Multiple Linear Regression predictions.
</p>

<img src="file:///{fig2_path.replace(os.sep, '/')}" class="figure-img" alt="Main Dashboard Screenshot">
<div class="caption"><strong>Figure 2:</strong> Main Dashboard with Dynamic KPI Cards, Location Price Comparison, and Area-Price Scatter Plot</div>

<img src="file:///{fig3_path.replace(os.sep, '/')}" class="figure-img" alt="Prediction Page Screenshot">
<div class="caption"><strong>Figure 3:</strong> Property Valuation Page with Input Specification Form and Live Linear Regression Output Card</div>

<img src="file:///{fig4_path.replace(os.sep, '/')}" class="figure-img" alt="Market Analytics Screenshot">
<div class="caption"><strong>Figure 4:</strong> Market Analytics Dashboard Displaying Four Multi-Dimensional Real-Estate Visualization Charts</div>

<img src="file:///{fig5_path.replace(os.sep, '/')}" class="figure-img" alt="Model Performance Screenshot">
<div class="caption"><strong>Figure 5:</strong> Model Performance Dashboard Showing Metric Summary, Actual vs. Predicted Plot, and Residual Histogram</div>

<img src="file:///{fig6_path.replace(os.sep, '/')}" class="figure-img" alt="Prediction History Screenshot">
<div class="caption"><strong>Figure 6:</strong> Prediction History Log Displaying User Valuations Persisted in SQLite with Record Deletion Support</div>

<h1>11. Advantages and Limitations</h1>
<h2>11.1 Advantages</h2>
<ul>
  <li><strong>Total Mathematical Interpretability:</strong> Every regression slope represents an exact financial contribution in Indian Rupees (₹), completely avoiding opaque black-box decisions.</li>
  <li><strong>Leakage-Free Modular Pipeline:</strong> Encapsulating OneHotEncoder and StandardScaler inside Scikit-learn's ColumnTransformer ensures sound data hygiene and reproducible production inference.</li>
  <li><strong>Sub-Millisecond Inference Latency:</strong> Multiple Linear Regression requires only vector dot products (O(n) complexity), executing predictions in less than 2 milliseconds on standard CPU hardware.</li>
  <li><strong>Comprehensive Full-Stack Integration:</strong> Seamlessly connects Scikit-learn statistical modeling with an SQLite database and interactive Chart.js visualizations.</li>
  <li><strong>Robust Categorical Handling:</strong> The OneHotEncoder configuration with handle_unknown='ignore' prevents runtime crashes when novel or unseen locations are queried.</li>
</ul>

<h2>11.2 Limitations</h2>
<ul>
  <li><strong>Assumption of Linearity:</strong> Multiple Linear Regression assumes strictly linear relationships between features and prices; complex interaction effects (e.g., luxury super-villas) may be slightly underfitted without polynomial expansion.</li>
  <li><strong>Synthetic Benchmark Data Boundaries:</strong> The model is trained on a curated synthetic demonstration dataset (seed=42). While statistically calibrated, synthetic data cannot capture macro-economic interest rate shocks or sudden regulatory changes.</li>
  <li><strong>Absence of Geospatial Micro-Coordinates:</strong> Properties are aggregated by discrete zone categories rather than continuous latitude/longitude coordinates or proximity to metro stations.</li>
  <li><strong>Sensitivity to Severe Outliers:</strong> Ordinary Least Squares minimizes squared residuals, making parameter estimates somewhat sensitive to extreme statistical anomalies.</li>
</ul>

<h1>12. Future Scope</h1>
<p>
While the current implementation achieves its objective of providing a functional, transparent linear regression valuation system, several promising technical avenues can expand its capabilities:
</p>
<ul>
  <li><strong>Real-World Multiple Listing Service (MLS) Integration:</strong> Connect the database to real-time real-estate API feeds (e.g., 99acres, MagicBricks) to continuously ingest live market transactions.</li>
  <li><strong>Geospatial Distance Feature Engineering:</strong> Incorporate GIS mapping APIs to calculate exact travel times to major IT tech parks, metro stations, international airports, and hospitals.</li>
  <li><strong>Polynomial & Regularized Regression Benchmarking:</strong> Implement Ridge (L2) and Lasso (L1) regression variants with cross-validated hyperparameter tuning to benchmark feature shrinkage and multi-collinearity control.</li>
  <li><strong>Automated Comparable Property Matcher:</strong> Develop a nearest-neighbor Euclidean distance recommender to display the top three most similar historical properties alongside each price prediction.</li>
  <li><strong>Cloud Containerization & Production Deployment:</strong> Package the application into lightweight Docker containers and deploy onto AWS or Google Cloud Run with automated CI/CD pipelines.</li>
</ul>

<h1>13. Conclusion</h1>
<p>
The HousePrice AI project successfully demonstrates the design, empirical training, diagnostic evaluation, and full-stack deployment of a residential property price prediction system powered strictly by Multiple Linear Regression. By adhering to the single-algorithm constraint, the project exemplifies the enduring value of statistical interpretability in applied machine learning. Rather than treating property valuation as an impenetrable black-box, the trained Ordinary Least Squares model makes every marginal feature coefficient explicit, providing understandable valuations in Indian Rupees (₹).
</p>
<p>
Rigorous data engineering practices—including reproducible 80:20 train-test partitioning, ColumnTransformer-based categorical one-hot encoding, and train-only standard scaling—ensured that the model completely avoids data leakage. On held-out testing data, the model achieved an impressive R² score of 0.9404, an MAE of ₹ 13,13,652.40, and an RMSE of ₹ 19,02,051.95, while residual diagnostics confirmed an unbiased Gaussian error distribution. Integrating the serialized Joblib pipeline into a responsive Flask web application supported by SQLite persistence and dynamic Chart.js visualizations bridges the gap between academic statistical theory and practical software engineering. HousePrice AI stands as a robust, fully functional academic project that illustrates how classical machine learning algorithms can solve meaningful real-world valuation challenges.
</p>

<h1>14. References</h1>
<ul>
  <li>•  F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, et al., "Scikit-learn: Machine Learning in Python," <em>Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.</em></li>
  <li>•  D. C. Montgomery, E. A. Peck, and G. G. Vining, <em>Introduction to Linear Regression Analysis, 6th ed., Hoboken, NJ: John Wiley & Sons, 2021.</em></li>
  <li>•  W. McKinney, "Data Structures for Statistical Computing in Python," <em>in Proceedings of the 9th Python in Science Conference (SciPy 2010), pp. 56–61, 2010.</em></li>
  <li>•  C. R. Harris, K. J. Millman, S. J. van der Walt, R. Gommers, P. Virtanen, et al., "Array programming with NumPy," <em>Nature, vol. 585, no. 7825, pp. 357–362, 2020.</em></li>
  <li>•  G. James, D. Witten, T. Hastie, and R. Tibshirani, <em>An Introduction to Statistical Learning: with Applications in R, 2nd ed., New York, NY: Springer, 2021.</em></li>
  <li>•  Pallets Projects, "Flask Documentation (v3.1.x): Web Development, One Drop at a Time," <em>https://flask.palletsprojects.com</em></li>
  <li>•  Scikit-learn Documentation, "Linear Models: Ordinary Least Squares & Multiple Regression," <em>https://scikit-learn.org/stable/modules/linear_model.html</em></li>
  <li>•  Chart.js Documentation, "Open-source HTML5 Canvas Charts for Modern Web Applications (v4.4)," <em>https://www.chartjs.org/docs/latest/</em></li>
  <li>•  SQLite Consortium, "SQLite Database Engine Official Documentation (v3.x)," <em>https://www.sqlite.org/docs.html</em></li>
</ul>

</body>
</html>
"""

with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated HTML: {html_output_path} ({os.path.getsize(html_output_path)} bytes)")

# Compile to PDF using headless Chrome
chrome_exe = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
if not os.path.exists(chrome_exe):
    chrome_exe = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

cmd = [
    chrome_exe,
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu',
    f'--print-to-pdf={pdf_output_path}',
    '--no-pdf-header-footer',
    f'file:///{html_output_path.replace(os.sep, "/")}'
]
res = subprocess.run(cmd, capture_output=True, timeout=30)

with open(pdf_output_path, 'rb') as f:
    pdf_bytes = f.read()

pages = len(re.findall(rb'/Type\s*/Page\b', pdf_bytes))
print(f"Generated PDF: {pdf_output_path} ({len(pdf_bytes)} bytes, Pages: {pages})")

print("\nReport generation completed successfully!")
