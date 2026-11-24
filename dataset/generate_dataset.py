"""
HousePrice AI - Dataset Generator
Generates a realistic residential property dataset based on Indian metropolitan real estate metrics.
Clearly labeled as a curated demonstration dataset for training Multiple Linear Regression.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_house_price_dataset(n_samples=1800, random_state=42):
    np.random.seed(random_state)
    
    locations = [
        "Indiranagar",
        "Koramangala",
        "HSR Layout",
        "Jayanagar",
        "Whitefield",
        "Bellandur",
        "Hebbal",
        "Marathahalli",
        "Bannerghatta Road",
        "Electronic City"
    ]
    
    # Base rate per sqft by location (INR)
    base_sqft_rates = {
        "Indiranagar": 11500,
        "Koramangala": 12000,
        "HSR Layout": 9600,
        "Jayanagar": 10200,
        "Whitefield": 7200,
        "Bellandur": 8100,
        "Hebbal": 8600,
        "Marathahalli": 6700,
        "Bannerghatta Road": 6100,
        "Electronic City": 4900
    }
    
    # Assign locations randomly with realistic distribution
    chosen_locations = np.random.choice(locations, size=n_samples, p=[
        0.08, 0.08, 0.12, 0.09, 0.15, 0.11, 0.09, 0.10, 0.08, 0.10
    ])
    
    records = []
    
    start_date = datetime(2025, 1, 1)
    
    for i in range(n_samples):
        loc = chosen_locations[i]
        
        # Bedrooms: 1 to 5
        bedrooms = np.random.choice([1, 2, 3, 4, 5], p=[0.10, 0.35, 0.35, 0.15, 0.05])
        
        # Area sqft typically correlates with bedrooms
        if bedrooms == 1:
            area = int(np.random.uniform(550, 850))
            bathrooms = 1
            floors = 1
        elif bedrooms == 2:
            area = int(np.random.uniform(900, 1400))
            bathrooms = np.random.choice([1, 2], p=[0.2, 0.8])
            floors = np.random.choice([1, 2], p=[0.7, 0.3])
        elif bedrooms == 3:
            area = int(np.random.uniform(1450, 2200))
            bathrooms = np.random.choice([2, 3], p=[0.3, 0.7])
            floors = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
        elif bedrooms == 4:
            area = int(np.random.uniform(2200, 3200))
            bathrooms = np.random.choice([3, 4], p=[0.4, 0.6])
            floors = np.random.choice([2, 3, 4], p=[0.3, 0.5, 0.2])
        else: # 5 bedrooms
            area = int(np.random.uniform(3100, 4500))
            bathrooms = np.random.choice([4, 5], p=[0.4, 0.6])
            floors = np.random.choice([2, 3, 4], p=[0.2, 0.5, 0.3])
            
        # Property age: 0 to 25 years
        age = int(np.random.exponential(scale=5.0))
        age = min(age, 25)
        
        # Parking: 1 or 0 (larger houses more likely to have parking)
        parking_prob = 0.65 if bedrooms == 1 else (0.85 if bedrooms <= 3 else 0.98)
        parking = 1 if np.random.rand() < parking_prob else 0
        
        # Date listed within past 500 days
        date_offset = int(np.random.uniform(0, 500))
        date_listed = (start_date + timedelta(days=date_offset)).strftime("%Y-%m-%d")
        
        # Calculate realistic price
        base_rate = base_sqft_rates[loc]
        base_price = area * base_rate
        
        # Premium and adjustments
        bedroom_val = bedrooms * 250000
        bathroom_val = bathrooms * 150000
        floors_val = (floors - 1) * 200000
        parking_val = parking * 300000
        depreciation = age * 35000
        
        # Market noise (approx +/- 3% to 5%)
        noise = np.random.normal(0, base_price * 0.04)
        
        total_price = base_price + bedroom_val + bathroom_val + floors_val + parking_val - depreciation + noise
        # Round to nearest 10,000 INR
        total_price = int(round(total_price / 10000.0) * 10000)
        
        records.append({
            "Location": loc,
            "Area_sqft": area,
            "Bedrooms": bedrooms,
            "Bathrooms": bathrooms,
            "Floors": floors,
            "Property_Age": age,
            "Parking": parking,
            "Date_Listed": date_listed,
            "Price_INR": total_price
        })
        
    df = pd.DataFrame(records)
    
    # Sort by date listed
    df = df.sort_values(by="Date_Listed").reset_index(drop=True)
    
    output_path = os.path.join(os.path.dirname(__file__), "house_prices.csv")
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully generated at {output_path} with {len(df)} records.")
    print("Sample records:\n", df.head())
    print("\nSummary Statistics:\n", df.describe())
    return df

if __name__ == "__main__":
    generate_house_price_dataset()
