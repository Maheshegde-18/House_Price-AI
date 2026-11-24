"""
HousePrice AI - Smart House Price Prediction System
Flask Backend Application
Strict ML Requirement: ONLY Multiple Linear Regression (sklearn.linear_model.LinearRegression)
"""

import os
import json
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash

from database.db import (
    init_db,
    populate_properties_if_empty,
    get_kpis,
    get_unique_locations,
    get_properties,
    get_analytics_data,
    save_prediction,
    get_predictions,
    delete_prediction,
    clear_all_predictions
)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "houseprice-ai-dev-secret-key-change-in-prod")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "house_price_model.joblib")
METRICS_PATH = os.path.join(BASE_DIR, "models", "model_metrics.json")
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "house_prices.csv")

# Global variables for model and metrics
ml_pipeline = None
model_metrics = {}

def load_ml_assets():
    global ml_pipeline, model_metrics
    if os.path.exists(MODEL_PATH):
        try:
            ml_pipeline = joblib.load(MODEL_PATH)
            print("Multiple Linear Regression pipeline loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print("Model file not found. Please run train_model.py first.")
        
    if os.path.exists(METRICS_PATH):
        try:
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                model_metrics = json.load(f)
            print("Model performance metrics loaded successfully.")
        except Exception as e:
            print(f"Error loading metrics: {e}")

# Format currency helper for Jinja
def format_inr(value):
    try:
        val = float(value)
        if val >= 10000000:
            return f"₹ {val / 10000000:.2f} Cr"
        elif val >= 100000:
            return f"₹ {val / 100000:.2f} L"
        else:
            return f"₹ {val:,.0f}"
    except (ValueError, TypeError):
        return f"₹ {value}"

def format_inr_full(value):
    try:
        val = int(round(float(value)))
        # Indian numbering system format (e.g., 12,34,567)
        s = str(val)
        if len(s) <= 3:
            return f"₹ {s}"
        last_three = s[-3:]
        other_digits = s[:-3]
        res = ""
        while len(other_digits) > 2:
            res = "," + other_digits[-2:] + res
            other_digits = other_digits[:-2]
        res = other_digits + res + "," + last_three
        return f"₹ {res}"
    except (ValueError, TypeError):
        return f"₹ {value}"

app.jinja_env.filters["format_inr"] = format_inr
app.jinja_env.filters["format_inr_full"] = format_inr_full

# Initialize Database and load dataset on startup
with app.app_context():
    init_db()
    populate_properties_if_empty(DATASET_PATH)
    load_ml_assets()

# ----------------- ROUTES ----------------- #

@app.route("/")
@app.route("/dashboard")
def dashboard():
    kpis = get_kpis()
    locations = get_unique_locations()
    recent_predictions = get_predictions(limit=5)
    return render_template(
        "dashboard.html",
        kpis=kpis,
        locations=locations,
        recent_predictions=recent_predictions,
        active_page="dashboard"
    )

@app.route("/predict", methods=["GET", "POST"])
def predict():
    locations = get_unique_locations()
    if request.method == "POST":
        try:
            location = request.form.get("location", "").strip()
            area_sqft = float(request.form.get("area_sqft", 0))
            bedrooms = int(request.form.get("bedrooms", 0))
            bathrooms = int(request.form.get("bathrooms", 0))
            floors = int(request.form.get("floors", 0))
            property_age = int(request.form.get("property_age", 0))
            parking = int(request.form.get("parking", 0))

            # Validation
            errors = []
            if not location:
                errors.append("Location is required.")
            if area_sqft < 200 or area_sqft > 15000:
                errors.append("Property area must be between 200 and 15,000 sq ft.")
            if bedrooms < 1 or bedrooms > 10:
                errors.append("Bedrooms must be between 1 and 10.")
            if bathrooms < 1 or bathrooms > 10:
                errors.append("Bathrooms must be between 1 and 10.")
            if floors < 1 or floors > 20:
                errors.append("Floors must be between 1 and 20.")
            if property_age < 0 or property_age > 100:
                errors.append("Property age must be between 0 and 100 years.")
            if parking not in (0, 1):
                errors.append("Parking value must be 0 or 1.")

            if errors:
                for err in errors:
                    flash(err, "danger")
                return render_template("predict.html", locations=locations, active_page="predict", form_data=request.form)

            # Predict using loaded Multiple Linear Regression pipeline
            global ml_pipeline
            if ml_pipeline is None:
                load_ml_assets()

            input_df = pd.DataFrame([{
                "Location": location,
                "Area_sqft": area_sqft,
                "Bedrooms": bedrooms,
                "Bathrooms": bathrooms,
                "Floors": floors,
                "Property_Age": property_age,
                "Parking": parking
            }])

            raw_pred = ml_pipeline.predict(input_df)[0]
            # Ensure price cannot be negative in realistic constraints
            predicted_price = max(100000.0, float(raw_pred))

            # Save prediction to SQLite
            pred_id = save_prediction(
                location=location,
                area_sqft=int(area_sqft),
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                floors=floors,
                property_age=property_age,
                parking=parking,
                predicted_price=predicted_price
            )

            result = {
                "id": pred_id,
                "location": location,
                "area_sqft": int(area_sqft),
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "floors": floors,
                "property_age": property_age,
                "parking": "Yes" if parking == 1 else "No",
                "predicted_price": predicted_price,
                "formatted_price": format_inr(predicted_price),
                "formatted_price_full": format_inr_full(predicted_price),
                "price_per_sqft": round(predicted_price / area_sqft, 2)
            }

            return render_template("predict.html", locations=locations, active_page="predict", result=result, form_data=request.form)

        except Exception as e:
            flash(f"Prediction failed: {str(e)}", "danger")
            return render_template("predict.html", locations=locations, active_page="predict", form_data=request.form)

    return render_template("predict.html", locations=locations, active_page="predict")

@app.route("/api/predict", methods=["POST"])
def api_predict():
    """AJAX API endpoint for real-time predictions."""
    try:
        data = request.get_json() or request.form
        location = str(data.get("location", "")).strip()
        area_sqft = float(data.get("area_sqft", 0))
        bedrooms = int(data.get("bedrooms", 0))
        bathrooms = int(data.get("bathrooms", 0))
        floors = int(data.get("floors", 0))
        property_age = int(data.get("property_age", 0))
        parking = int(data.get("parking", 0))

        # Input validation
        if not location:
            return jsonify({"success": False, "error": "Location is required."}), 400
        if area_sqft < 200 or area_sqft > 15000:
            return jsonify({"success": False, "error": "Area must be between 200 and 15,000 sq ft."}), 400
        if bedrooms < 1 or bedrooms > 10:
            return jsonify({"success": False, "error": "Bedrooms must be between 1 and 10."}), 400
        if bathrooms < 1 or bathrooms > 10:
            return jsonify({"success": False, "error": "Bathrooms must be between 1 and 10."}), 400
        if floors < 1 or floors > 20:
            return jsonify({"success": False, "error": "Floors must be between 1 and 20."}), 400
        if property_age < 0 or property_age > 100:
            return jsonify({"success": False, "error": "Property age must be between 0 and 100."}), 400

        global ml_pipeline
        if ml_pipeline is None:
            load_ml_assets()

        input_df = pd.DataFrame([{
            "Location": location,
            "Area_sqft": area_sqft,
            "Bedrooms": bedrooms,
            "Bathrooms": bathrooms,
            "Floors": floors,
            "Property_Age": property_age,
            "Parking": parking
        }])

        raw_pred = ml_pipeline.predict(input_df)[0]
        predicted_price = max(100000.0, float(raw_pred))

        pred_id = save_prediction(
            location=location,
            area_sqft=int(area_sqft),
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            floors=floors,
            property_age=property_age,
            parking=parking,
            predicted_price=predicted_price
        )

        return jsonify({
            "success": True,
            "prediction": {
                "id": pred_id,
                "location": location,
                "area_sqft": int(area_sqft),
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "floors": floors,
                "property_age": property_age,
                "parking": "Yes" if parking == 1 else "No",
                "predicted_price": predicted_price,
                "formatted_price": format_inr(predicted_price),
                "formatted_price_full": format_inr_full(predicted_price),
                "price_per_sqft": round(predicted_price / area_sqft, 2)
            },
            "disclaimer": "This estimated price is generated using a Multiple Linear Regression statistical model for educational & demonstration purposes. It does not constitute an official appraisal or guaranteed market quotation."
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/listings")
def listings():
    search = request.args.get("search", "").strip()
    location = request.args.get("location", "All")
    min_price = request.args.get("min_price", "")
    max_price = request.args.get("max_price", "")
    bedrooms = request.args.get("bedrooms", "All")
    sort_by = request.args.get("sort_by", "id_asc")
    page = int(request.args.get("page", 1))

    locations = get_unique_locations()
    data = get_properties(
        search=search,
        location=location,
        min_price=min_price,
        max_price=max_price,
        bedrooms=bedrooms,
        sort_by=sort_by,
        page=page,
        per_page=12
    )

    return render_template(
        "listings.html",
        properties=data["properties"],
        total_count=data["total_count"],
        page=data["page"],
        total_pages=data["total_pages"],
        locations=locations,
        selected_location=location,
        selected_bedrooms=bedrooms,
        sort_by=sort_by,
        search=search,
        min_price=min_price,
        max_price=max_price,
        active_page="listings"
    )

@app.route("/analytics")
def analytics():
    kpis = get_kpis()
    locations = get_unique_locations()
    return render_template(
        "analytics.html",
        kpis=kpis,
        locations=locations,
        active_page="analytics"
    )

@app.route("/performance")
def performance():
    global model_metrics
    if not model_metrics:
        load_ml_assets()

    return render_template(
        "performance.html",
        metrics=model_metrics,
        active_page="performance"
    )

@app.route("/history")
def history():
    predictions = get_predictions(limit=100)
    return render_template(
        "history.html",
        predictions=predictions,
        active_page="history"
    )

@app.route("/history/delete/<int:pred_id>", methods=["POST"])
def delete_pred(pred_id):
    success = delete_prediction(pred_id)
    if success:
        flash("Prediction record successfully deleted.", "success")
    else:
        flash("Record not found or could not be deleted.", "warning")
    return redirect(url_for("history"))

@app.route("/history/clear", methods=["POST"])
def clear_history():
    clear_all_predictions()
    flash("Prediction history cleared completely.", "info")
    return redirect(url_for("history"))

@app.route("/about")
def about():
    global model_metrics
    if not model_metrics:
        load_ml_assets()
    return render_template(
        "about.html",
        metrics=model_metrics,
        active_page="about"
    )

# ----------------- JSON DATA APIS FOR CHARTS ----------------- #

@app.route("/api/analytics/charts")
def api_analytics_charts():
    """Returns dynamic dataset analytics data for Chart.js."""
    data = get_analytics_data()
    return jsonify(data)

@app.route("/api/performance/charts")
def api_performance_charts():
    """Returns actual vs predicted and residual distribution data."""
    global model_metrics
    if not model_metrics:
        load_ml_assets()
    return jsonify({
        "actual_vs_predicted": model_metrics.get("actual_vs_predicted_samples", []),
        "residual_distribution": model_metrics.get("residual_distribution", []),
        "metrics": model_metrics.get("metrics", {}),
        "coefficients": model_metrics.get("coefficients", [])
    })

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
