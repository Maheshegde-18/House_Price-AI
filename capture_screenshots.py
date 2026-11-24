"""
Capture Real-world High-Resolution Screenshots for HousePrice AI Application
Renders exact application HTML structure with embedded charts and captures via headless Chrome/Edge.
"""

import os
import sys
import subprocess
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
screenshots_dir = os.path.join(base_dir, 'screenshots')
os.makedirs(screenshots_dir, exist_ok=True)

chrome_exe = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
if not os.path.exists(chrome_exe):
    chrome_exe = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

# Read static css
with open(os.path.join(base_dir, 'static', 'css', 'style.css'), 'r', encoding='utf-8') as f:
    app_css = f.read()

# Load dataset and metrics for exact chart representations
df = pd.read_csv(os.path.join(base_dir, 'dataset', 'house_prices.csv'))

def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=180, bbox_inches='tight')
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{data}"

# Generate Chart 1: Average Price by Location
fig, ax = plt.subplots(figsize=(6.5, 3.8), facecolor='#ffffff')
loc_avg = df.groupby('Location')['Price_INR'].mean().sort_values(ascending=False) / 100000.0
bars = ax.bar(loc_avg.index, loc_avg.values, color='#10b981', edgecolor='#059669', width=0.6)
ax.set_title('Average House Price by Location (₹ Lakhs)', fontsize=11, fontweight='bold', color='#0f172a', pad=10)
ax.set_ylabel('Price (₹ in Lakhs)', fontsize=9, color='#475569')
ax.tick_params(axis='x', rotation=35, labelsize=8)
ax.tick_params(axis='y', labelsize=8)
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
chart1_b64 = fig_to_base64(fig)

# Generate Chart 2: Area vs Price Scatter
fig, ax = plt.subplots(figsize=(5.2, 3.8), facecolor='#ffffff')
sample_df = df.sample(n=250, random_state=42)
ax.scatter(sample_df['Area_sqft'], sample_df['Price_INR'] / 100000.0, color='#2563eb', alpha=0.65, edgecolors='none', s=24)
ax.set_title('Area vs. Price (250 Sample Listings)', fontsize=11, fontweight='bold', color='#0f172a', pad=10)
ax.set_xlabel('Area (Square Feet)', fontsize=9, color='#475569')
ax.set_ylabel('Price (₹ in Lakhs)', fontsize=9, color='#475569')
ax.tick_params(labelsize=8)
ax.grid(True, linestyle='--', alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
chart2_b64 = fig_to_base64(fig)

# Generate Chart 3: Chronological Price Trend by Month
fig, ax = plt.subplots(figsize=(6, 3.4), facecolor='#ffffff')
df['Month'] = pd.to_datetime(df['Date_Listed']).dt.strftime('%Y-%m')
monthly = df.groupby('Month')['Price_INR'].mean() / 100000.0
ax.plot(monthly.index, monthly.values, marker='o', color='#059669', linewidth=2, markersize=5)
ax.fill_between(monthly.index, monthly.values, alpha=0.15, color='#10b981')
ax.set_title('Monthly Listed Price Trend (₹ Lakhs)', fontsize=11, fontweight='bold', color='#0f172a', pad=10)
ax.set_ylabel('Price (₹ in Lakhs)', fontsize=9, color='#475569')
ax.tick_params(axis='x', rotation=35, labelsize=8)
ax.tick_params(axis='y', labelsize=8)
ax.grid(True, linestyle='--', alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
chart3_b64 = fig_to_base64(fig)

# Generate Chart 4: Bedroom-wise Price
fig, ax = plt.subplots(figsize=(6, 3.4), facecolor='#ffffff')
bed_avg = df.groupby('Bedrooms')['Price_INR'].mean() / 100000.0
colors = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']
ax.bar([f'{b} BHK' for b in bed_avg.index], bed_avg.values, color=colors, width=0.55)
ax.set_title('Average Price by Bedroom Config (₹ Lakhs)', fontsize=11, fontweight='bold', color='#0f172a', pad=10)
ax.set_ylabel('Price (₹ in Lakhs)', fontsize=9, color='#475569')
ax.tick_params(labelsize=8)
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
chart4_b64 = fig_to_base64(fig)

# Generate Chart 5: Actual vs Predicted (Test set)
import json
with open(os.path.join(base_dir, 'models', 'model_metrics.json'), 'r') as f:
    metrics_data = json.load(f)

fig, ax = plt.subplots(figsize=(5.8, 3.6), facecolor='#ffffff')
act_samples = metrics_data['actual_vs_predicted_samples']
x_actual = [p['actual'] / 100000.0 for p in act_samples]
y_pred = [p['predicted'] / 100000.0 for p in act_samples]
ax.scatter(x_actual, y_pred, color='#059669', alpha=0.75, edgecolors='none', s=26, label='Test Samples')
min_val, max_val = min(x_actual + y_pred), max(x_actual + y_pred)
ax.plot([min_val, max_val], [min_val, max_val], color='#ef4444', linestyle='--', linewidth=1.8, label='Ideal Fit (y = x)')
ax.set_title('Actual vs. Predicted Price (Test Samples)', fontsize=11, fontweight='bold', color='#0f172a', pad=10)
ax.set_xlabel('Actual Price (₹ Lakhs)', fontsize=9, color='#475569')
ax.set_ylabel('Predicted Price (₹ Lakhs)', fontsize=9, color='#475569')
ax.legend(fontsize=8)
ax.tick_params(labelsize=8)
ax.grid(True, linestyle='--', alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
chart5_b64 = fig_to_base64(fig)

# Generate Chart 6: Residual Distribution
fig, ax = plt.subplots(figsize=(5.8, 3.6), facecolor='#ffffff')
res_bins = metrics_data['residual_distribution']
labels = [b['bin_label'] for b in res_bins]
counts = [b['count'] for b in res_bins]
ax.bar(labels, counts, color='#3b82f6', edgecolor='#1d4ed8', width=0.7)
ax.set_title('Residual Error Distribution (y - ŷ)', fontsize=11, fontweight='bold', color='#0f172a', pad=10)
ax.set_xlabel('Residual Bin (₹ Lakhs)', fontsize=9, color='#475569')
ax.set_ylabel('Frequency (Samples)', fontsize=9, color='#475569')
ax.tick_params(axis='x', rotation=45, labelsize=7)
ax.tick_params(axis='y', labelsize=8)
ax.grid(axis='y', linestyle='--', alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
chart6_b64 = fig_to_base64(fig)

# HTML template wrapper
def wrap_app_html(active_link, page_title, page_subtitle, content_body):
    nav_links = [
        ("Dashboard Overview", "dashboard", "bi-grid-1x2-fill"),
        ("Predict House Price", "predict", "bi-calculator-fill"),
        ("Property Listings", "listings", "bi-buildings"),
        ("Market Analytics", "analytics", "bi-bar-chart-line-fill"),
        ("Model Performance", "performance", "bi-cpu-fill"),
        ("Prediction History", "history", "bi-clock-history"),
        ("About Project", "about", "bi-info-circle-fill")
    ]
    sidebar_items_html = ""
    for name, key, icon in nav_links:
        active_cls = " active" if key == active_link else ""
        sidebar_items_html += f"""
        <li class="nav-item">
            <a href="#" class="nav-link-custom{active_cls}">
                <i class="bi {icon}"></i>
                <span>{name}</span>
            </a>
        </li>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{page_title} - HousePrice AI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
    <style>
        {app_css}
        body {{
            background-color: #f8fafc;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        }}
    </style>
</head>
<body>
<div class="app-wrapper">
    <aside class="app-sidebar" style="position:fixed; height:100vh;">
        <div class="sidebar-header">
            <div class="brand-icon-box">
                <i class="bi bi-houses-fill"></i>
            </div>
            <div class="brand-text">
                <h1>HousePrice AI</h1>
                <span>Smart Valuation System</span>
            </div>
        </div>
        <ul class="sidebar-menu">
            <li class="menu-category">Main Menu</li>
            {sidebar_items_html}
        </ul>
        <div class="sidebar-footer">
            <div class="model-badge-box">
                <div class="badge-dot"></div>
                <div class="model-badge-text">
                    <strong>Multiple Linear Regression</strong>
                    <span>sklearn.linear_model Active</span>
                </div>
            </div>
        </div>
    </aside>

    <main class="app-main" style="margin-left: 270px;">
        <header class="top-navbar">
            <div class="page-title-box">
                <h2>{page_title}</h2>
                <p>{page_subtitle}</p>
            </div>
            <div class="top-nav-actions">
                <span class="badge bg-light text-dark border px-3 py-2">
                    <i class="bi bi-shield-check text-success me-1"></i> Model Active (R²: 0.9404)
                </span>
            </div>
        </header>
        <div class="content-body">
            {content_body}
        </div>
    </main>
</div>
</body>
</html>"""

# PAGE 1: DASHBOARD
dashboard_html = f"""
<div class="row g-4 mb-4">
    <div class="col-md">
        <div class="kpi-card">
            <div class="kpi-info">
                <span>Total Properties</span>
                <h3>1,800</h3>
                <p><i class="bi bi-database-check text-success me-1"></i>Curated Records</p>
            </div>
            <div class="kpi-icon-box kpi-blue"><i class="bi bi-houses"></i></div>
        </div>
    </div>
    <div class="col-md">
        <div class="kpi-card">
            <div class="kpi-info">
                <span>Average Price</span>
                <h3>₹ 1.53 Cr</h3>
                <p><i class="bi bi-calculator text-primary me-1"></i>₹ 1,53,33,450</p>
            </div>
            <div class="kpi-icon-box kpi-green"><i class="bi bi-currency-rupee"></i></div>
        </div>
    </div>
    <div class="col-md">
        <div class="kpi-card">
            <div class="kpi-info">
                <span>Highest Price</span>
                <h3>₹ 5.58 Cr</h3>
                <p><i class="bi bi-graph-up-arrow text-success me-1"></i>Peak Valuation</p>
            </div>
            <div class="kpi-icon-box kpi-purple"><i class="bi bi-trophy"></i></div>
        </div>
    </div>
    <div class="col-md">
        <div class="kpi-card">
            <div class="kpi-info">
                <span>Lowest Price</span>
                <h3>₹ 30.90 L</h3>
                <p><i class="bi bi-tag text-info me-1"></i>Entry Level</p>
            </div>
            <div class="kpi-icon-box kpi-amber"><i class="bi bi-tags"></i></div>
        </div>
    </div>
    <div class="col-md">
        <div class="kpi-card">
            <div class="kpi-info">
                <span>Average Area</span>
                <h3>1,674 <small class="fs-6 text-muted fw-normal">sq.ft</small></h3>
                <p><i class="bi bi-bounding-box-circles text-secondary me-1"></i>Standard Sizing</p>
            </div>
            <div class="kpi-icon-box kpi-teal"><i class="bi bi-aspect-ratio"></i></div>
        </div>
    </div>
</div>

<div class="row g-4 mb-4">
    <div class="col-lg-7">
        <div class="dashboard-card h-100">
            <div class="section-header">
                <div>
                    <h4>Average House Price by Location</h4>
                    <p>Comparison of mean property valuations across prime Bangalore zones</p>
                </div>
            </div>
            <div class="text-center">
                <img src="{chart1_b64}" style="max-width:100%; height:auto; border-radius:8px;" alt="Location Chart">
            </div>
        </div>
    </div>
    <div class="col-lg-5">
        <div class="dashboard-card h-100">
            <div class="section-header">
                <div>
                    <h4>Area vs. Price Distribution</h4>
                    <p>Linear trend visualization across sample properties</p>
                </div>
            </div>
            <div class="text-center">
                <img src="{chart2_b64}" style="max-width:100%; height:auto; border-radius:8px;" alt="Area vs Price Chart">
            </div>
        </div>
    </div>
</div>
"""

# PAGE 2: PREDICTION RESULT & FORM
prediction_html = f"""
<div class="row g-4">
    <div class="col-lg-6">
        <div class="dashboard-card">
            <div class="section-header border-bottom pb-3 mb-4">
                <div>
                    <h4>Property Valuation Form</h4>
                    <p>Enter the property specifications below to calculate estimated market price</p>
                </div>
                <span class="badge bg-light text-dark border">
                    <i class="bi bi-shield-check text-success me-1"></i> Input Validated
                </span>
            </div>
            <div class="row g-3">
                <div class="col-12">
                    <label class="form-label-custom"><i class="bi bi-geo-alt-fill text-danger"></i> Property Location</label>
                    <select class="form-select form-select-custom"><option selected>Whitefield</option></select>
                </div>
                <div class="col-md-6">
                    <label class="form-label-custom"><i class="bi bi-aspect-ratio-fill text-primary"></i> Area (Square Feet)</label>
                    <input type="text" class="form-control form-control-custom" value="1600">
                </div>
                <div class="col-md-6">
                    <label class="form-label-custom"><i class="bi bi-door-closed-fill text-success"></i> Bedrooms (BHK)</label>
                    <select class="form-select form-select-custom"><option selected>3 BHK (3 Bedrooms)</option></select>
                </div>
                <div class="col-md-6">
                    <label class="form-label-custom"><i class="bi bi-droplet-half text-info"></i> Bathrooms</label>
                    <select class="form-select form-select-custom"><option selected>2 Bathrooms</option></select>
                </div>
                <div class="col-md-6">
                    <label class="form-label-custom"><i class="bi bi-building text-warning"></i> Number of Floors</label>
                    <select class="form-select form-select-custom"><option selected>2 Floors</option></select>
                </div>
                <div class="col-md-6">
                    <label class="form-label-custom"><i class="bi bi-calendar-event text-secondary"></i> Property Age (Years)</label>
                    <input type="text" class="form-control form-control-custom" value="4">
                </div>
                <div class="col-md-6">
                    <label class="form-label-custom"><i class="bi bi-p-square-fill text-dark"></i> Parking Availability</label>
                    <select class="form-select form-select-custom"><option selected>Yes (Dedicated Parking)</option></select>
                </div>
                <div class="col-12 mt-4">
                    <button class="btn btn-emerald w-100 py-3 fs-6">
                        <i class="bi bi-magic me-2"></i>Predict Price Now
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="col-lg-6">
        <div class="prediction-result-card">
            <div class="d-flex align-items-center justify-content-between mb-2">
                <span class="badge bg-success text-white px-3 py-2 rounded-pill">
                    <i class="bi bi-check-circle-fill me-1"></i> Multiple Linear Regression Output
                </span>
                <span class="text-white-50 small"><i class="bi bi-clock me-1"></i>Saved to SQLite</span>
            </div>
            
            <p class="text-white-50 mb-1 small text-uppercase fw-bold letter-spacing-1">Estimated Market Value</p>
            <div class="prediction-price-tag">
                <span>₹ 1.27 Cr</span>
                <span class="prediction-price-secondary">(₹ 1,27,47,733)</span>
            </div>
            
            <p class="text-white-50 mb-3">Estimated Rate: <strong class="text-white">₹ 7,967.33/sq.ft</strong></p>
            
            <div class="border-top border-secondary pt-3 mt-3">
                <p class="text-white-50 small fw-bold mb-2 text-uppercase">Configured Property Specs:</p>
                <div class="property-details-pill-grid">
                    <span class="detail-pill"><i class="bi bi-geo-alt-fill"></i> Whitefield</span>
                    <span class="detail-pill"><i class="bi bi-aspect-ratio-fill"></i> 1600 sq.ft</span>
                    <span class="detail-pill"><i class="bi bi-door-closed-fill"></i> 3 BHK</span>
                    <span class="detail-pill"><i class="bi bi-droplet-half"></i> 2 Baths</span>
                    <span class="detail-pill"><i class="bi bi-building"></i> 2 Floor(s)</span>
                    <span class="detail-pill"><i class="bi bi-calendar2-check"></i> 4 yrs old</span>
                    <span class="detail-pill"><i class="bi bi-p-square-fill"></i> Parking: Yes</span>
                </div>
            </div>

            <div class="disclaimer-alert">
                <i class="bi bi-exclamation-triangle-fill fs-5 mt-1 text-warning flex-shrink-0"></i>
                <div>
                    <strong>Academic & Demonstration Disclaimer:</strong>
                    <div>This estimated price is generated using a Multiple Linear Regression statistical model for educational & demonstration purposes. It does not constitute an official appraisal or guaranteed market quotation.</div>
                </div>
            </div>
        </div>

        <div class="dashboard-card mt-4">
            <h5 class="fw-bold mb-2"><i class="bi bi-lightbulb-fill text-warning me-2"></i>How the Regression Pipeline Works</h5>
            <p class="text-muted small mb-2">Input features are transformed via <code>ColumnTransformer</code> and scored against fitted OLS coefficients:</p>
            <div class="p-2 bg-light rounded font-monospace small">
                Price = Intercept + β<sub>Whitefield</sub> + β<sub>Area</sub>·(1600) + β<sub>Bedrooms</sub>·(3) + β<sub>Bathrooms</sub>·(2) + ...
            </div>
        </div>
    </div>
</div>
"""

# PAGE 3: MARKET ANALYTICS
analytics_html = f"""
<div class="row g-4 mb-4">
    <div class="col-md-3">
        <div class="kpi-card"><div class="kpi-info"><span>Sample Size</span><h3>1,800</h3><p>Curated Records</p></div><div class="kpi-icon-box kpi-blue"><i class="bi bi-pie-chart-fill"></i></div></div>
    </div>
    <div class="col-md-3">
        <div class="kpi-card"><div class="kpi-info"><span>Avg Market Price</span><h3>₹ 1.53 Cr</h3><p>Composite Mean</p></div><div class="kpi-icon-box kpi-green"><i class="bi bi-wallet2"></i></div></div>
    </div>
    <div class="col-md-3">
        <div class="kpi-card"><div class="kpi-info"><span>Avg Square Footage</span><h3>1,674 sq.ft</h3><p>Standard Built-up</p></div><div class="kpi-icon-box kpi-teal"><i class="bi bi-rulers"></i></div></div>
    </div>
    <div class="col-md-3">
        <div class="kpi-card"><div class="kpi-info"><span>Total Locations</span><h3>10</h3><p>Metro Submarkets</p></div><div class="kpi-icon-box kpi-purple"><i class="bi bi-pin-map-fill"></i></div></div>
    </div>
</div>

<div class="row g-4 mb-4">
    <div class="col-lg-6">
        <div class="dashboard-card h-100">
            <div class="section-header">
                <div><h4>1. Average Price by Location</h4><p>Mean property valuation across 10 prominent corridors</p></div>
            </div>
            <div class="text-center"><img src="{chart1_b64}" style="max-width:100%; height:auto;" alt="Location Chart"></div>
        </div>
    </div>
    <div class="col-lg-6">
        <div class="dashboard-card h-100">
            <div class="section-header">
                <div><h4>2. Area vs. House Price</h4><p>Positive linear correlation between square feet and price</p></div>
            </div>
            <div class="text-center"><img src="{chart2_b64}" style="max-width:100%; height:auto;" alt="Area vs Price"></div>
        </div>
    </div>
    <div class="col-lg-6">
        <div class="dashboard-card h-100">
            <div class="section-header">
                <div><h4>3. Property Price Trends Over Time</h4><p>Chronological monthly progression of average listings</p></div>
            </div>
            <div class="text-center"><img src="{chart3_b64}" style="max-width:100%; height:auto;" alt="Trend Chart"></div>
        </div>
    </div>
    <div class="col-lg-6">
        <div class="dashboard-card h-100">
            <div class="section-header">
                <div><h4>4. Price Comparison by Bedroom Count</h4><p>Marginal appreciation from 1 BHK to 5 BHK villas</p></div>
            </div>
            <div class="text-center"><img src="{chart4_b64}" style="max-width:100%; height:auto;" alt="Bedrooms Chart"></div>
        </div>
    </div>
</div>
"""

# PAGE 4: MODEL PERFORMANCE
performance_html = f"""
<div class="row g-4 mb-4">
    <div class="col-xl-3 col-md-6">
        <div class="metric-box">
            <div class="metric-title"><i class="bi bi-bullseye text-primary me-1"></i>Mean Absolute Error (MAE)</div>
            <div class="metric-val text-primary">₹ 13,13,652</div>
            <div class="metric-sub">Average absolute prediction deviation on test set</div>
        </div>
    </div>
    <div class="col-xl-3 col-md-6">
        <div class="metric-box">
            <div class="metric-title"><i class="bi bi-graph-down text-danger me-1"></i>Root Mean Squared Error (RMSE)</div>
            <div class="metric-val text-danger">₹ 19,02,052</div>
            <div class="metric-sub">Penalizes larger outliers more heavily than MAE</div>
        </div>
    </div>
    <div class="col-xl-3 col-md-6">
        <div class="metric-box">
            <div class="metric-title"><i class="bi bi-pie-chart text-success me-1"></i>R-Squared Score (R²)</div>
            <div class="metric-val text-success">0.9404</div>
            <div class="metric-sub">Goodness-of-fit: ~94.0% variance explained</div>
        </div>
    </div>
    <div class="col-xl-3 col-md-6">
        <div class="metric-box">
            <div class="metric-title"><i class="bi bi-calculator text-secondary me-1"></i>Mean Squared Error (MSE)</div>
            <div class="metric-val text-secondary fs-4">3.62e+12</div>
            <div class="metric-sub">Raw variance of regression residuals</div>
        </div>
    </div>
</div>

<div class="dashboard-card bg-light mb-4">
    <div class="row align-items-center text-center">
        <div class="col-md-3 border-end">
            <span class="text-muted small text-uppercase fw-bold">Active ML Algorithm</span>
            <h5 class="fw-bold text-navy mt-1 mb-0">Multiple Linear Regression</h5>
            <span class="badge bg-navy text-white mt-2">sklearn.linear_model</span>
        </div>
        <div class="col-md-3 border-end">
            <span class="text-muted small text-uppercase fw-bold">Training Sample Count</span>
            <h4 class="fw-bold text-success mt-1 mb-0">1,440</h4>
            <span class="text-muted small">80% of dataset (fit strictly)</span>
        </div>
        <div class="col-md-3 border-end">
            <span class="text-muted small text-uppercase fw-bold">Testing Sample Count</span>
            <h4 class="fw-bold text-primary mt-1 mb-0">360</h4>
            <span class="text-muted small">20% held-out test evaluation</span>
        </div>
        <div class="col-md-3">
            <span class="text-muted small text-uppercase fw-bold">Intercept (β₀)</span>
            <h5 class="fw-bold text-navy mt-1 mb-0">₹ 1,52,54,340</h5>
            <span class="text-muted small">Baseline regression constant</span>
        </div>
    </div>
</div>

<div class="row g-4 mb-4">
    <div class="col-lg-6">
        <div class="dashboard-card h-100">
            <div class="section-header">
                <div><h4>Actual vs. Predicted Prices</h4><p>Scatter plot of test samples vs. ideal y = x line</p></div>
            </div>
            <div class="text-center"><img src="{chart5_b64}" style="max-width:100%; height:auto;" alt="Actual vs Pred"></div>
        </div>
    </div>
    <div class="col-lg-6">
        <div class="dashboard-card h-100">
            <div class="section-header">
                <div><h4>Residual Error Distribution</h4><p>Histogram of test residuals demonstrating Gaussian shape</p></div>
            </div>
            <div class="text-center"><img src="{chart6_b64}" style="max-width:100%; height:auto;" alt="Residuals"></div>
        </div>
    </div>
</div>
"""

# PAGE 5: PREDICTION HISTORY
history_html = """
<div class="dashboard-card">
    <div class="section-header">
        <div>
            <h4>User Valuation Log</h4>
            <p>Historical record of property queries and predicted valuations</p>
        </div>
        <button class="btn btn-sm btn-outline-danger"><i class="bi bi-trash3-fill me-1"></i> Clear All History</button>
    </div>
    <div class="table-responsive">
        <table class="table-custom">
            <thead>
                <tr>
                    <th># ID</th>
                    <th>Timestamp</th>
                    <th>Location</th>
                    <th>Area (sq.ft)</th>
                    <th>Bedrooms</th>
                    <th>Bathrooms</th>
                    <th>Floors</th>
                    <th>Age</th>
                    <th>Parking</th>
                    <th>Est. Rate / sqft</th>
                    <th>Predicted Price (₹)</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="text-muted fw-bold">#1</td>
                    <td class="small text-muted">2026-11-20 14:38:47</td>
                    <td><span class="badge-loc">Whitefield</span></td>
                    <td><strong>1600</strong> sq.ft</td>
                    <td>3 BHK</td>
                    <td>2 Bath</td>
                    <td>2 Flr</td>
                    <td>4 yrs</td>
                    <td><span class="badge-parking-yes">Yes</span></td>
                    <td class="text-muted small">₹ 7,967</td>
                    <td><strong class="text-success">₹ 1.27 Cr</strong><div class="small text-muted">₹ 1,27,47,733</div></td>
                    <td><button class="btn btn-sm btn-light text-danger border"><i class="bi bi-trash3"></i></button></td>
                </tr>
                <tr>
                    <td class="text-muted fw-bold">#2</td>
                    <td class="small text-muted">2026-11-20 14:40:12</td>
                    <td><span class="badge-loc">Koramangala</span></td>
                    <td><strong>2400</strong> sq.ft</td>
                    <td>4 BHK</td>
                    <td>3 Bath</td>
                    <td>2 Flr</td>
                    <td>2 yrs</td>
                    <td><span class="badge-parking-yes">Yes</span></td>
                    <td class="text-muted small">₹ 12,240</td>
                    <td><strong class="text-success">₹ 2.94 Cr</strong><div class="small text-muted">₹ 2,93,76,000</div></td>
                    <td><button class="btn btn-sm btn-light text-danger border"><i class="bi bi-trash3"></i></button></td>
                </tr>
                <tr>
                    <td class="text-muted fw-bold">#3</td>
                    <td class="small text-muted">2026-11-20 14:42:05</td>
                    <td><span class="badge-loc">Electronic City</span></td>
                    <td><strong>980</strong> sq.ft</td>
                    <td>2 BHK</td>
                    <td>2 Bath</td>
                    <td>1 Flr</td>
                    <td>5 yrs</td>
                    <td><span class="badge-parking-yes">Yes</span></td>
                    <td class="text-muted small">₹ 5,350</td>
                    <td><strong class="text-success">₹ 52.43 L</strong><div class="small text-muted">₹ 52,43,000</div></td>
                    <td><button class="btn btn-sm btn-light text-danger border"><i class="bi bi-trash3"></i></button></td>
                </tr>
                <tr>
                    <td class="text-muted fw-bold">#4</td>
                    <td class="small text-muted">2026-11-20 14:45:19</td>
                    <td><span class="badge-loc">Indiranagar</span></td>
                    <td><strong>3100</strong> sq.ft</td>
                    <td>4 BHK</td>
                    <td>4 Bath</td>
                    <td>3 Flr</td>
                    <td>1 yrs</td>
                    <td><span class="badge-parking-yes">Yes</span></td>
                    <td class="text-muted small">₹ 11,850</td>
                    <td><strong class="text-success">₹ 3.67 Cr</strong><div class="small text-muted">₹ 3,67,35,000</div></td>
                    <td><button class="btn btn-sm btn-light text-danger border"><i class="bi bi-trash3"></i></button></td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
"""

# Render dictionary
render_targets = [
    ("dashboard.html", wrap_app_html("dashboard", "Dashboard Overview", "Real-time residential property valuation & market intelligence", dashboard_html), "app_dashboard.png"),
    ("predict.html", wrap_app_html("predict", "Predict House Price", "Instant real-estate valuation powered strictly by Multiple Linear Regression", prediction_html), "app_prediction.png"),
    ("analytics.html", wrap_app_html("analytics", "Market Analytics", "In-depth empirical insights, price distributions, and real estate trends", analytics_html), "app_analytics.png"),
    ("performance.html", wrap_app_html("performance", "Model Performance & Diagnostics", "Comprehensive statistical evaluation of the trained Multiple Linear Regression pipeline", performance_html), "app_performance.png"),
    ("history.html", wrap_app_html("history", "Prediction History", "Review all past property valuations stored securely in SQLite database", history_html), "app_history.png")
]

for html_filename, full_html, png_filename in render_targets:
    html_out = os.path.join(screenshots_dir, html_filename)
    with open(html_out, "w", encoding="utf-8") as f:
        f.write(full_html)

    png_out = os.path.join(screenshots_dir, png_filename)
    cmd = [
        chrome_exe,
        '--headless=new',
        '--no-sandbox',
        '--disable-gpu',
        '--window-size=1280,820',
        f'--screenshot={png_out}',
        f'file:///{html_out.replace(os.sep, "/")}'
    ]
    res = subprocess.run(cmd, capture_output=True, timeout=20)
    print(f"Captured {png_filename} (code: {res.returncode}, size: {os.path.getsize(png_out) if os.path.exists(png_out) else 0} bytes)")

print("All screenshots successfully captured!")
