def get_weather_analysis(weather):
    """
    Advanced weather impact analysis including delay factors,
    road surface risk, and travel advisories for TN roads.
    """
    w = str(weather).strip().capitalize()
    
    profiles = {
        "Clear": {
            "factor": 0.0,
            "visibility": "Excellent (> 10 km)",
            "risk": "Low",
            "advisory": "Normal driving conditions on national/state highways."
        },
        "Fog": {
            "factor": 0.14,
            "visibility": "Reduced (< 500 m)",
            "risk": "Moderate",
            "advisory": "Fog lights recommended. Reduced speed on ghat sections."
        },
        "Rain": {
            "factor": 0.12,
            "visibility": "Moderate (2 - 5 km)",
            "risk": "Moderate",
            "advisory": "Wet roads and reduced traction. Safe braking distance advised."
        },
        "Storm": {
            "factor": 0.28,
            "visibility": "Poor (< 1 km)",
            "risk": "High",
            "advisory": "Heavy crosswinds and waterlogging potential. Slower average speeds expected."
        }
    }

    info = profiles.get(w, {
        "factor": 0.05,
        "visibility": "Good",
        "risk": "Low",
        "advisory": "Standard transit safety guidelines apply."
    })

    return {
        "condition": w,
        "factor": info["factor"],
        "visibility": info["visibility"],
        "risk": info["risk"],
        "advisory": info["advisory"]
    }

def weather_delay_factor(weather):
    """Backward compatibility helper"""
    return get_weather_analysis(weather)["factor"]
