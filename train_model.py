"""
HousePrice AI - Model Training Script
Strict ML requirement: ONLY Multiple Linear Regression (sklearn.linear_model.LinearRegression)
Uses ColumnTransformer with OneHotEncoder and StandardScaler inside a unified Pipeline.
Saves the trained pipeline with Joblib and evaluation metrics to JSON.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_and_evaluate_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "dataset", "house_prices.csv")
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    model_output_path = os.path.join(models_dir, "house_price_model.joblib")
    metrics_output_path = os.path.join(models_dir, "model_metrics.json")
    
    print(f"Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    
    # Feature columns and target
    feature_cols = [
        "Location",
        "Area_sqft",
        "Bedrooms",
        "Bathrooms",
        "Floors",
        "Property_Age",
        "Parking"
    ]
    target_col = "Price_INR"
    
    X = df[feature_cols]
    y = df[target_col]
    
    # Train / Test split - strictly reproducible
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    categorical_features = ["Location"]
    numerical_features = [
        "Area_sqft",
        "Bedrooms",
        "Bathrooms",
        "Floors",
        "Property_Age",
        "Parking"
    ]
    
    # Preprocessor using ColumnTransformer
    # handle_unknown='ignore' ensures robustness against unseen locations at inference time
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
            ("num", StandardScaler(), numerical_features)
        ],
        remainder="drop"
    )
    
    # Unified Pipeline: Preprocessing + Multiple Linear Regression ONLY
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression(fit_intercept=True))
    ])
    
    # Fit pipeline strictly on training data to avoid data leakage
    print("Fitting Multiple Linear Regression pipeline on training data...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate strictly on unseen test data
    y_pred_test = pipeline.predict(X_test)
    y_pred_train = pipeline.predict(X_train)
    
    # Metrics computation
    mae_test = float(mean_absolute_error(y_test, y_pred_test))
    mse_test = float(mean_squared_error(y_test, y_pred_test))
    rmse_test = float(np.sqrt(mse_test))
    r2_test = float(r2_score(y_test, y_pred_test))
    
    mae_train = float(mean_absolute_error(y_train, y_pred_train))
    r2_train = float(r2_score(y_train, y_pred_train))
    
    print("\n--- Model Evaluation (Test Set) ---")
    print(f"Mean Absolute Error (MAE): ₹{mae_test:,.2f}")
    print(f"Mean Squared Error (MSE): {mse_test:,.2e}")
    print(f"Root Mean Squared Error (RMSE): ₹{rmse_test:,.2f}")
    print(f"R-squared (R²): {r2_test:.4f}")
    print(f"Training R-squared (R²): {r2_train:.4f}")
    
    # Extract feature names & coefficients for interpretability
    fitted_preprocessor = pipeline.named_steps["preprocessor"]
    fitted_regressor = pipeline.named_steps["regressor"]
    
    cat_feature_names = list(fitted_preprocessor.named_transformers_["cat"].get_feature_names_out(categorical_features))
    all_feature_names = cat_feature_names + numerical_features
    coefficients = fitted_regressor.coef_.tolist()
    intercept = float(fitted_regressor.intercept_)
    
    feature_coefficients = [
        {"feature": name, "coefficient": float(coef)}
        for name, coef in zip(all_feature_names, coefficients)
    ]
    
    # Residual analysis on test set
    residuals = (y_test - y_pred_test).values
    
    # Create histogram distribution of residuals for Chart.js
    res_min, res_max = float(residuals.min()), float(residuals.max())
    hist_counts, bin_edges = np.histogram(residuals, bins=15)
    residual_distribution = [
        {
            "bin_start": float(bin_edges[i]),
            "bin_end": float(bin_edges[i+1]),
            "bin_label": f"₹{bin_edges[i]/1e5:.1f}L to ₹{bin_edges[i+1]/1e5:.1f}L",
            "count": int(hist_counts[i])
        }
        for i in range(len(hist_counts))
    ]
    
    # Select sample points for Actual vs Predicted chart (test set)
    # Sample 100 points for clear visualization without cluttering Chart.js
    sample_indices = np.random.RandomState(42).choice(len(y_test), size=min(120, len(y_test)), replace=False)
    actual_vs_predicted = [
        {
            "actual": float(y_test.iloc[idx]),
            "predicted": float(y_pred_test[idx]),
            "residual": float(y_test.iloc[idx] - y_pred_test[idx]),
            "location": str(X_test.iloc[idx]["Location"]),
            "area_sqft": int(X_test.iloc[idx]["Area_sqft"])
        }
        for idx in sample_indices
    ]
    
    # Save model pipeline
    print(f"\nSaving model pipeline to {model_output_path}...")
    joblib.dump(pipeline, model_output_path)
    
    # Save model metrics & metadata
    metrics_payload = {
        "algorithm": "Multiple Linear Regression",
        "implementation": "sklearn.linear_model.LinearRegression",
        "training_samples": len(X_train),
        "testing_samples": len(X_test),
        "total_samples": len(df),
        "train_test_split_ratio": "80:20",
        "random_state": 42,
        "metrics": {
            "mae": mae_test,
            "mse": mse_test,
            "rmse": rmse_test,
            "r2_score": r2_test,
            "train_r2_score": r2_train,
            "train_mae": mae_train
        },
        "intercept": intercept,
        "coefficients": feature_coefficients,
        "features": {
            "categorical": categorical_features,
            "numerical": numerical_features
        },
        "locations": sorted(df["Location"].unique().tolist()),
        "residual_distribution": residual_distribution,
        "actual_vs_predicted_samples": actual_vs_predicted,
        "target_variable": "Price_INR",
        "evaluation_notes": (
            "R-squared represents the proportion of variance in house prices explained by the linear combination "
            "of input features. It is a goodness-of-fit metric for regression models, distinct from classification accuracy. "
            "Performance depends on dataset linearity, feature relevance, and noise levels."
        )
    }
    
    with open(metrics_output_path, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)
    print(f"Metrics saved successfully to {metrics_output_path}")

if __name__ == "__main__":
    train_and_evaluate_model()
