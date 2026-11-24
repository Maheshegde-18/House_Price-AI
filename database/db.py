"""
HousePrice AI - SQLite Database Handler
Manages property listings and user prediction history.
"""

import os
import sqlite3
import pandas as pd
from datetime import datetime

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "house_price.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table 1: Properties dataset
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        area_sqft INTEGER NOT NULL,
        bedrooms INTEGER NOT NULL,
        bathrooms INTEGER NOT NULL,
        floors INTEGER NOT NULL,
        property_age INTEGER NOT NULL,
        parking INTEGER NOT NULL,
        price_inr INTEGER NOT NULL,
        date_listed TEXT NOT NULL
    )
    """)
    
    # Table 2: User Prediction History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        location TEXT NOT NULL,
        area_sqft INTEGER NOT NULL,
        bedrooms INTEGER NOT NULL,
        bathrooms INTEGER NOT NULL,
        floors INTEGER NOT NULL,
        property_age INTEGER NOT NULL,
        parking INTEGER NOT NULL,
        predicted_price_inr REAL NOT NULL,
        price_per_sqft REAL NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

def populate_properties_if_empty(csv_path):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM properties")
    count = cursor.fetchone()["cnt"]
    
    if count == 0 and os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        records = df.to_dict(orient="records")
        cursor.executemany("""
        INSERT INTO properties (location, area_sqft, bedrooms, bathrooms, floors, property_age, parking, price_inr, date_listed)
        VALUES (:Location, :Area_sqft, :Bedrooms, :Bathrooms, :Floors, :Property_Age, :Parking, :Price_INR, :Date_Listed)
        """, records)
        conn.commit()
        print(f"Database populated with {len(records)} property records.")
    
    conn.close()

def get_kpis():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        COUNT(*) as total_properties,
        AVG(price_inr) as avg_price,
        MAX(price_inr) as max_price,
        MIN(price_inr) as min_price,
        AVG(area_sqft) as avg_area
    FROM properties
    """)
    row = cursor.fetchone()
    conn.close()
    
    if row and row["total_properties"] > 0:
        return {
            "total_properties": int(row["total_properties"]),
            "avg_price": float(row["avg_price"]),
            "max_price": int(row["max_price"]),
            "min_price": int(row["min_price"]),
            "avg_area": float(row["avg_area"])
        }
    return {
        "total_properties": 0,
        "avg_price": 0,
        "max_price": 0,
        "min_price": 0,
        "avg_area": 0
    }

def get_unique_locations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT location FROM properties ORDER BY location ASC")
    rows = cursor.fetchall()
    conn.close()
    return [r["location"] for r in rows]

def get_properties(search=None, location=None, min_price=None, max_price=None, bedrooms=None, sort_by="id_asc", page=1, per_page=15):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM properties WHERE 1=1"
    params = []
    
    if search:
        query += " AND (location LIKE ? OR CAST(area_sqft AS TEXT) LIKE ?)"
        search_term = f"%{search.strip()}%"
        params.extend([search_term, search_term])
        
    if location and location != "All":
        query += " AND location = ?"
        params.append(location)
        
    if min_price:
        try:
            query += " AND price_inr >= ?"
            params.append(float(min_price))
        except ValueError:
            pass
            
    if max_price:
        try:
            query += " AND price_inr <= ?"
            params.append(float(max_price))
        except ValueError:
            pass
            
    if bedrooms and bedrooms != "All":
        try:
            query += " AND bedrooms = ?"
            params.append(int(bedrooms))
        except ValueError:
            pass
            
    # Sorting
    sort_mapping = {
        "price_asc": "price_inr ASC",
        "price_desc": "price_inr DESC",
        "area_asc": "area_sqft ASC",
        "area_desc": "area_sqft DESC",
        "age_asc": "property_age ASC",
        "date_desc": "date_listed DESC",
        "id_asc": "id ASC"
    }
    order_clause = sort_mapping.get(sort_by, "id ASC")
    
    # Count total matching rows
    count_query = f"SELECT COUNT(*) as total FROM ({query})"
    cursor.execute(count_query, params)
    total_count = cursor.fetchone()["total"]
    
    # Pagination
    offset = (page - 1) * per_page
    query += f" ORDER BY {order_clause} LIMIT ? OFFSET ?"
    params.extend([per_page, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    properties = [dict(r) for r in rows]
    conn.close()
    
    total_pages = max(1, (total_count + per_page - 1) // per_page)
    
    return {
        "properties": properties,
        "total_count": total_count,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages
    }

def get_analytics_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Average price and count by location
    cursor.execute("""
    SELECT location, 
           ROUND(AVG(price_inr), 2) as avg_price,
           ROUND(AVG(price_inr / area_sqft), 2) as avg_rate_sqft,
           COUNT(*) as property_count
    FROM properties
    GROUP BY location
    ORDER BY avg_price DESC
    """)
    price_by_location = [dict(r) for r in cursor.fetchall()]
    
    # 2. Scatter plot: Area vs House Price (sample up to 250 points for chart smoothness)
    cursor.execute("""
    SELECT area_sqft, price_inr, location, bedrooms
    FROM properties
    ORDER BY RANDOM()
    LIMIT 250
    """)
    area_vs_price = [dict(r) for r in cursor.fetchall()]
    
    # 3. Bedroom-wise comparisons
    cursor.execute("""
    SELECT bedrooms,
           ROUND(AVG(price_inr), 2) as avg_price,
           MIN(price_inr) as min_price,
           MAX(price_inr) as max_price,
           COUNT(*) as count
    FROM properties
    GROUP BY bedrooms
    ORDER BY bedrooms ASC
    """)
    prices_by_bedrooms = [dict(r) for r in cursor.fetchall()]
    
    # 4. Property price trend by Date Listed (Monthly aggregation)
    cursor.execute("""
    SELECT strftime('%Y-%m', date_listed) as month,
           ROUND(AVG(price_inr), 2) as avg_price,
           COUNT(*) as listings_count
    FROM properties
    GROUP BY month
    ORDER BY month ASC
    """)
    price_trends_by_date = [dict(r) for r in cursor.fetchall()]
    
    conn.close()
    
    return {
        "price_by_location": price_by_location,
        "area_vs_price": area_vs_price,
        "prices_by_bedrooms": prices_by_bedrooms,
        "price_trends_by_date": price_trends_by_date
    }

def save_prediction(location, area_sqft, bedrooms, bathrooms, floors, property_age, parking, predicted_price):
    conn = get_connection()
    cursor = conn.cursor()
    
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    price_per_sqft = round(predicted_price / max(1, area_sqft), 2)
    
    cursor.execute("""
    INSERT INTO predictions (created_at, location, area_sqft, bedrooms, bathrooms, floors, property_age, parking, predicted_price_inr, price_per_sqft)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (created_at, location, area_sqft, bedrooms, bathrooms, floors, property_age, parking, predicted_price, price_per_sqft))
    
    pred_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return pred_id

def get_predictions(limit=100):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    predictions = [dict(r) for r in rows]
    conn.close()
    return predictions

def delete_prediction(pred_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions WHERE id = ?", (pred_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def clear_all_predictions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()
    return True
