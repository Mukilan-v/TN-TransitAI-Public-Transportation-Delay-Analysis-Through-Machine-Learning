import math
import pandas as pd
from pathlib import Path
from heapq import heappush, heappop

BASE_DIR = Path(__file__).resolve().parent

# -----------------------------
# LOAD DISTRICT DATA & ALIASES
# -----------------------------
districts_df = pd.read_csv(BASE_DIR / "data" / "tn_districts.csv")
districts_df["district"] = districts_df["district"].astype(str).str.strip().str.lower()

district_dict = {
    row["district"]: (float(row["latitude"]), float(row["longitude"]))
    for _, row in districts_df.iterrows()
}

district_metadata = {
    row["district"]: {
        "zone": row.get("zone", "General"),
        "is_ghat": bool(row.get("is_ghat", 0))
    }
    for _, row in districts_df.iterrows()
}

# Common name aliases for seamless user experience
ALIASES = {
    "trichy": "tiruchirappalli",
    "tiruchi": "tiruchirappalli",
    "villupuram": "viluppuram",
    "nilgiris": "ooty",
    "the nilgiris": "ooty",
    "trivandrum": "kanyakumari",
    "bangalore": "hosur"
}

def resolve_district_name(name):
    if not name:
        return ""
    clean = str(name).strip().lower()
    return ALIASES.get(clean, clean)

def get_coordinates(district_name):
    district_name = resolve_district_name(district_name)
    coords = district_dict.get(district_name)
    if coords is None:
        # Fallback to closest matching key
        for k, v in district_dict.items():
            if district_name in k or k in district_name:
                return v
        return 11.1271, 78.6569 # Center of Tamil Nadu default
    return coords

def calculate_distance(from_d, to_d):
    lat1, lon1 = get_coordinates(from_d)
    lat2, lon2 = get_coordinates(to_d)

    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Road curvature factor (typical Indian national/state highways are ~1.18x aerial distance)
    road_factor = 1.18
    from_meta = district_metadata.get(resolve_district_name(from_d), {})
    to_meta = district_metadata.get(resolve_district_name(to_d), {})
    if from_meta.get("is_ghat") or to_meta.get("is_ghat"):
        road_factor = 1.35  # Ghat hairpin bends
        
    return round(R * c * road_factor, 1)

# -------------------------------------------------------------
# TAMIL NADU HIGHWAY ROAD GRAPH (Connecting all 38 districts)
# -------------------------------------------------------------
# Realistic network of major NH / SH corridors
HIGHWAY_GRAPH = {
    "chennai": ["tiruvallur", "kanchipuram", "chengalpattu"],
    "tiruvallur": ["chennai", "kanchipuram", "ranipet"],
    "kanchipuram": ["chennai", "chengalpattu", "ranipet", "vellore", "tiruvannamalai"],
    "chengalpattu": ["chennai", "kanchipuram", "viluppuram"],
    "viluppuram": ["chengalpattu", "cuddalore", "tiruvannamalai", "kallakurichi", "perambalur"],
    "cuddalore": ["viluppuram", "kallakurichi", "mayiladuthurai", "perambalur"],
    "ranipet": ["tiruvallur", "kanchipuram", "vellore"],
    "vellore": ["ranipet", "kanchipuram", "tirupathur", "tiruvannamalai", "krishnagiri"],
    "tirupathur": ["vellore", "krishnagiri", "dharmapuri", "tiruvannamalai"],
    "tiruvannamalai": ["kanchipuram", "vellore", "tirupathur", "viluppuram", "kallakurichi"],
    "kallakurichi": ["viluppuram", "cuddalore", "tiruvannamalai", "perambalur", "salem"],
    "perambalur": ["viluppuram", "cuddalore", "kallakurichi", "ariyalur", "tiruchirappalli", "salem"],
    "ariyalur": ["perambalur", "cuddalore", "thanjavur", "tiruchirappalli"],
    "krishnagiri": ["vellore", "tirupathur", "dharmapuri", "hosur"],
    "hosur": ["krishnagiri", "dharmapuri"],
    "dharmapuri": ["hosur", "krishnagiri", "tirupathur", "salem"],
    "salem": ["dharmapuri", "kallakurichi", "perambalur", "namakkal", "erode"],
    "namakkal": ["salem", "erode", "karur", "tiruchirappalli"],
    "erode": ["salem", "namakkal", "karur", "tiruppur", "coimbatore"],
    "tiruppur": ["erode", "coimbatore", "karur", "dindigul"],
    "coimbatore": ["tiruppur", "erode", "pollachi", "mettupalayam"],
    "mettupalayam": ["coimbatore", "ooty"],
    "ooty": ["mettupalayam", "coimbatore"],
    "pollachi": ["coimbatore", "tiruppur", "dindigul"],
    "karur": ["namakkal", "erode", "tiruppur", "dindigul", "tiruchirappalli"],
    "tiruchirappalli": ["perambalur", "ariyalur", "karur", "namakkal", "pudukkottai", "thanjavur", "dindigul"],
    "thanjavur": ["ariyalur", "tiruchirappalli", "pudukkottai", "kumbakonam", "tiruvarur"],
    "kumbakonam": ["thanjavur", "mayiladuthurai", "tiruvarur", "ariyalur"],
    "mayiladuthurai": ["cuddalore", "kumbakonam", "tiruvarur", "nagapattinam"],
    "tiruvarur": ["thanjavur", "kumbakonam", "mayiladuthurai", "nagapattinam"],
    "nagapattinam": ["mayiladuthurai", "tiruvarur", "thanjavur", "ramanathapuram"],
    "pudukkottai": ["tiruchirappalli", "thanjavur", "sivaganga", "madurai"],
    "dindigul": ["tiruppur", "karur", "tiruchirappalli", "madurai", "theni", "kodaikanal", "pollachi"],
    "kodaikanal": ["dindigul", "theni"],
    "theni": ["dindigul", "kodaikanal", "madurai", "virudhunagar"],
    "madurai": ["dindigul", "theni", "tiruchirappalli", "pudukkottai", "sivaganga", "virudhunagar"],
    "sivaganga": ["madurai", "pudukkottai", "karaikudi", "ramanathapuram"],
    "karaikudi": ["sivaganga", "pudukkottai", "ramanathapuram"],
    "virudhunagar": ["madurai", "theni", "sivaganga", "tenkasi", "tirunelveli", "thoothukudi"],
    "ramanathapuram": ["sivaganga", "karaikudi", "nagapattinam", "rameswaram", "thoothukudi"],
    "rameswaram": ["ramanathapuram"],
    "tenkasi": ["virudhunagar", "tirunelveli"],
    "tirunelveli": ["virudhunagar", "tenkasi", "thoothukudi", "nagercoil", "kanyakumari"],
    "thoothukudi": ["virudhunagar", "ramanathapuram", "tirunelveli", "kanyakumari"],
    "nagercoil": ["tirunelveli", "kanyakumari"],
    "kanyakumari": ["tirunelveli", "thoothukudi", "nagercoil"]
}

# Ensure bidirectional graph links
for node, neighbors in list(HIGHWAY_GRAPH.items()):
    for neighbor in neighbors:
        if neighbor in HIGHWAY_GRAPH:
            if node not in HIGHWAY_GRAPH[neighbor]:
                HIGHWAY_GRAPH[neighbor].append(node)
        else:
            HIGHWAY_GRAPH[neighbor] = [node]

# -------------------------------------------------------------
# GRAPH ROUTE DISCOVERY (Dijkstra Shortest Road Path)
# -------------------------------------------------------------
def find_optimal_route(origin, destination):
    """
    Finds the shortest road route connecting any two districts in Tamil Nadu.
    Returns: {
        'path': [list of capitalized district names],
        'total_distance_km': float,
        'stops': [list with per-segment distance & cumulative distance],
        'is_ghat': bool,
        'terrain': str
    }
    """
    start = resolve_district_name(origin)
    goal = resolve_district_name(destination)

    if start not in HIGHWAY_GRAPH or goal not in HIGHWAY_GRAPH:
        # Fallback direct path
        dist = calculate_distance(start, goal)
        return {
            "path": [origin.title(), destination.title()],
            "total_distance_km": dist,
            "stops": [{"district": origin.title(), "segment_km": 0, "cumulative_km": 0},
                      {"district": destination.title(), "segment_km": dist, "cumulative_km": dist}],
            "is_ghat": False,
            "terrain": "Plains"
        }

    if start == goal:
        return {
            "path": [start.title()],
            "total_distance_km": 0,
            "stops": [{"district": start.title(), "segment_km": 0, "cumulative_km": 0}],
            "is_ghat": False,
            "terrain": "Local"
        }

    # Dijkstra priority queue: (cumulative_distance, current_node, path)
    queue = [(0, start, [start])]
    visited = {}

    best_path = None
    best_dist = float("inf")

    while queue:
        dist, current, path = heappop(queue)

        if current in visited and visited[current] <= dist:
            continue
        visited[current] = dist

        if current == goal:
            best_path = path
            best_dist = dist
            break

        for neighbor in HIGHWAY_GRAPH.get(current, []):
            edge_dist = calculate_distance(current, neighbor)
            new_dist = dist + edge_dist
            if neighbor not in visited or new_dist < visited[neighbor]:
                heappush(queue, (new_dist, neighbor, path + [neighbor]))

    if not best_path:
        best_path = [start, goal]
        best_dist = calculate_distance(start, goal)

    # Build detailed stop breakdown
    stops = []
    cumulative = 0.0
    has_ghat = False

    for i, district in enumerate(best_path):
        seg = 0.0
        if i > 0:
            seg = calculate_distance(best_path[i-1], district)
            cumulative += seg
        
        meta = district_metadata.get(district, {})
        if meta.get("is_ghat"):
            has_ghat = True

        stops.append({
            "district": district.title(),
            "segment_km": round(seg, 1),
            "cumulative_km": round(cumulative, 1),
            "zone": meta.get("zone", "General")
        })

    terrain = "Ghats / Mountain Corridor" if has_ghat else "State Highway / Expressway Corridor"

    return {
        "path": [d.title() for d in best_path],
        "total_distance_km": round(cumulative if cumulative > 0 else best_dist, 1),
        "stops": stops,
        "is_ghat": has_ghat,
        "terrain": terrain
    }

# -----------------------------
# NEAREST DISTRICT DETECTOR
# -----------------------------
def find_nearest_district(lat, lon):
    """
    Finds the closest TN district to given GPS coordinates using Haversine formula.
    """
    min_dist = float("inf")
    nearest = "Chennai"

    for dist_name, (dlat, dlon) in district_dict.items():
        R = 6371
        dlat_rad = math.radians(dlat - lat)
        dlon_rad = math.radians(dlon - lon)
        a = (math.sin(dlat_rad / 2) ** 2
             + math.cos(math.radians(lat))
             * math.cos(math.radians(dlat))
             * math.sin(dlon_rad / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        dist = R * c

        if dist < min_dist:
            min_dist = dist
            nearest = dist_name

    return nearest.title()
