# map-routing/risk_zones.py

RISK_ZONES_DATABASE = [
    {
        "zone_id": "ZONE-WAYANAD-04",
        "name": "Wayanad Pass High Risk Sector",
        "risk_level": "CRITICAL",
        "risk_score": 0.92,
        "coordinates": [
            [76.070, 11.600],
            [76.095, 11.600],
            [76.095, 11.625],
            [76.070, 11.625],
            [76.070, 11.600]
        ]
    },
    {
        "zone_id": "ZONE-MUNNAR-01",
        "name": "Munnar Slope Sector A",
        "risk_level": "HIGH",
        "risk_score": 0.78,
        "coordinates": [
            [77.050, 10.080],
            [77.070, 10.080],
            [77.070, 10.100],
            [77.050, 10.100],
            [77.050, 10.080]
        ]
    }
]

def get_geojson_risk_zones():
    """Converts internal zone definitions into GeoJSON format for frontend rendering."""
    features = []
    for zone in RISK_ZONES_DATABASE:
        features.append({
            "type": "Feature",
            "properties": {
                "zone_id": zone["zone_id"],
                "name": zone["name"],
                "risk_level": zone["risk_level"],
                "risk_score": zone["risk_score"]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [zone["coordinates"]]
            }
        })
    return {"type": "FeatureCollection", "features": features}