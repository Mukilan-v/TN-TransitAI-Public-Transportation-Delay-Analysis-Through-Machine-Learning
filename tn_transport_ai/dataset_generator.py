import random
import pandas as pd
import numpy as np
from pathlib import Path
from route_engine import calculate_distance, find_optimal_route
from traffic_engine import get_traffic_analysis
from weather_engine import get_weather_analysis

BASE_DIR = Path(__file__).resolve().parent

districts_df = pd.read_csv(BASE_DIR / "data" / "tn_districts.csv")
districts = districts_df["district"].tolist()

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weathers = ["Clear", "Fog", "Rain", "Storm"]

rows = []
np.random.seed(42)
random.seed(42)

print("Generating 5,000 realistic Tamil Nadu transit records...")

for _ in range(5000):
    from_d = random.choice(districts)
    to_d = random.choice(districts)

    if from_d == to_d:
        continue

    # Use graph engine for realistic route discovery
    route_info = find_optimal_route(from_d, to_d)
    distance = route_info["total_distance_km"]
    is_ghat = 1 if route_info.get("is_ghat") else 0

    hour = random.randint(0, 23)
    day = random.choice(days)
    is_weekend = 1 if day in ["Saturday", "Sunday"] else 0
    weather = random.choices(weathers, weights=[0.60, 0.12, 0.22, 0.06])[0]

    traffic_info = get_traffic_analysis(day, hour, from_d, to_d)
    traffic_score = traffic_info["score"]

    weather_info = get_weather_analysis(weather)
    weather_factor = weather_info["factor"]

    # Base travel time (average highway cruise: 52 km/h; ghats: 32 km/h)
    speed = 32.0 if is_ghat else 52.0
    base_time = (distance / speed) * 60.0

    # Realistic delay formula components:
    # 1. Congestion toll & terminal delay
    traffic_delay = (traffic_score * 2.8) * (1.0 + (distance / 500.0))
    
    # 2. Weather road condition delay
    weather_delay = base_time * weather_factor
    
    # 3. Ghat section delay
    ghat_delay = random.uniform(15.0, 30.0) if is_ghat else 0.0

    # 4. Long haul fatigue/toll queue delay
    toll_delay = (distance / 70.0) * random.uniform(2.0, 4.5)

    # 5. Peak urban terminus delay
    peak_urban_delay = 0.0
    if (7 <= hour <= 10) or (17 <= hour <= 20):
        peak_urban_delay = random.uniform(8.0, 18.0)

    # Total predicted delay with natural variance
    noise = random.gauss(0, 3.5)
    total_delay = max(0.0, traffic_delay + weather_delay + ghat_delay + toll_delay + peak_urban_delay + noise)

    rows.append([
        from_d, to_d, distance, hour, day, is_weekend,
        weather, traffic_score, is_ghat, round(base_time, 1), round(total_delay, 1)
    ])

df = pd.DataFrame(rows, columns=[
    "from_district", "to_district", "distance_km", "hour", "day",
    "is_weekend", "weather", "traffic_score", "is_ghat", "base_time", "delay_minutes"
])

output_path = BASE_DIR / "data" / "transport_dataset.csv"
df.to_csv(output_path, index=False)
print(f"Dataset Created successfully with {len(df)} records at {output_path}")
