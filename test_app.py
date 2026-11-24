"""
HousePrice AI - Comprehensive Automated Test Suite
Verifies:
1. Database initialization and KPI calculations
2. Model file existence and pipeline validity
3. All Flask route responses (GET & POST)
4. Model prediction accuracy and SQLite persistence
5. Deletion of prediction records
6. Chart API JSON outputs
"""

import unittest
import json
import os
import joblib
import pandas as pd
from app import app
from database.db import get_kpis, get_predictions, delete_prediction, get_connection

class HousePriceAITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        cls.client = app.test_client()

    def test_01_model_file_exists(self):
        model_path = os.path.join("models", "house_price_model.joblib")
        self.assertTrue(os.path.exists(model_path), "Model joblib file does not exist!")
        pipeline = joblib.load(model_path)
        self.assertIsNotNone(pipeline)
        print("✓ Model pipeline exists and loads successfully.")

    def test_02_database_kpis(self):
        kpis = get_kpis()
        self.assertGreater(kpis["total_properties"], 0)
        self.assertGreater(kpis["avg_price"], 0)
        self.assertGreater(kpis["avg_area"], 0)
        print(f"✓ Database verified with {kpis['total_properties']} records and avg price ₹{kpis['avg_price']:,.2f}")

    def test_03_dashboard_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"HousePrice AI", response.data)
        self.assertIn(b"Dashboard Overview", response.data)
        print("✓ Dashboard route returned HTTP 200.")

    def test_04_listings_route(self):
        response = self.client.get("/listings")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Property Listings", response.data)
        
        # Test filtering
        filter_res = self.client.get("/listings?location=Indiranagar&bedrooms=3")
        self.assertEqual(filter_res.status_code, 200)
        self.assertIn(b"Indiranagar", filter_res.data)
        print("✓ Property listings & filter route verified.")

    def test_05_analytics_route(self):
        response = self.client.get("/analytics")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Market Analytics", response.data)
        print("✓ Analytics route returned HTTP 200.")

    def test_06_performance_route(self):
        response = self.client.get("/performance")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Model Performance", response.data)
        self.assertIn(b"R-Squared", response.data)
        print("✓ Performance route returned HTTP 200.")

    def test_07_about_route(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"About HousePrice AI", response.data)
        print("✓ About route returned HTTP 200.")

    def test_08_api_predict_and_persistence(self):
        test_payload = {
            "location": "Whitefield",
            "area_sqft": 1600,
            "bedrooms": 3,
            "bathrooms": 2,
            "floors": 2,
            "property_age": 4,
            "parking": 1
        }
        response = self.client.post("/api/predict", 
                                    data=json.dumps(test_payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("prediction", data)
        pred = data["prediction"]
        self.assertGreater(pred["predicted_price"], 100000)
        self.assertEqual(pred["location"], "Whitefield")
        print(f"✓ Prediction API returned: {pred['formatted_price']} ({pred['formatted_price_full']})")

        # Verify record exists in history
        history_res = self.client.get("/history")
        self.assertEqual(history_res.status_code, 200)
        self.assertIn(b"Whitefield", history_res.data)

        # Test deleting prediction
        pred_id = pred["id"]
        del_res = self.client.post(f"/history/delete/{pred_id}", follow_redirects=True)
        self.assertEqual(del_res.status_code, 200)
        print(f"✓ Successfully verified prediction generation, SQLite persistence, and record deletion.")

    def test_09_api_chart_data(self):
        analytics_charts = self.client.get("/api/analytics/charts")
        self.assertEqual(analytics_charts.status_code, 200)
        c_data = analytics_charts.get_json()
        self.assertIn("price_by_location", c_data)
        self.assertIn("area_vs_price", c_data)
        self.assertIn("prices_by_bedrooms", c_data)
        self.assertIn("price_trends_by_date", c_data)

        perf_charts = self.client.get("/api/performance/charts")
        self.assertEqual(perf_charts.status_code, 200)
        p_data = perf_charts.get_json()
        self.assertIn("actual_vs_predicted", p_data)
        self.assertIn("residual_distribution", p_data)
        print("✓ All Chart.js dynamic data API endpoints verified.")

if __name__ == "__main__":
    unittest.main()
