def get_traffic_analysis(day, hour, origin="", destination=""):
    """
    Advanced multi-factor corridor traffic score (1.0 to 10.0 scale)
    incorporating time of day, day of week, weekend surge, and major metro bottleneck zones.
    """
    day = str(day).title()
    hour = int(hour)
    
    # Base diurnal traffic curve
    if 0 <= hour < 5:
        base_score = 1.8  # Midnight / early dawn free cruising
    elif 5 <= hour < 7:
        base_score = 3.2  # Early morning departures
    elif 7 <= hour <= 10:
        base_score = 8.5  # Morning office & bus terminal rush peak
    elif 11 <= hour <= 15:
        base_score = 4.8  # Midday steady flow
    elif 16 <= hour <= 20:
        base_score = 9.2  # Evening peak commute & inter-city departures
    elif 21 <= hour <= 23:
        base_score = 5.5  # Night express departures
    else:
        base_score = 4.0

    # Day of week modifiers
    is_weekend = day in ["Saturday", "Sunday"]
    is_friday = day == "Friday"
    
    if is_friday and hour >= 16:
        base_score += 1.2  # Friday weekend exit rush
    elif is_weekend:
        if 8 <= hour <= 12 or 17 <= hour <= 21:
            base_score += 0.8  # Weekend tourist & family transit
        else:
            base_score -= 0.5

    # Check if origin or destination is a high-density transit hub
    metro_hubs = {"chennai", "coimbatore", "madurai", "tiruchirappalli", "salem"}
    o_clean = str(origin).strip().lower()
    d_clean = str(destination).strip().lower()
    if o_clean in metro_hubs or d_clean in metro_hubs:
        if (7 <= hour <= 10) or (17 <= hour <= 20):
            base_score += 0.8

    traffic_score = min(10.0, max(1.0, round(base_score, 1)))

    if traffic_score >= 8.0:
        status = "Heavy Traffic / Peak Bottleneck"
        color = "#ef4444" # red
        speed_impact_pct = 25
    elif traffic_score >= 5.0:
        status = "Moderate Highway Flow"
        color = "#f59e0b" # amber
        speed_impact_pct = 12
    else:
        status = "Clear / Fast Moving Road"
        color = "#10b981" # green
        speed_impact_pct = 0

    return {
        "score": traffic_score,
        "status": status,
        "color": color,
        "speed_impact_pct": speed_impact_pct
    }

def get_traffic_score(day, hour):
    """Backward compatibility helper"""
    return get_traffic_analysis(day, hour)["score"]
