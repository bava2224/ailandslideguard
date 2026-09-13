# map-routing/route_risk.py
from map_routing.map_utils import create_base_map, add_heatmap_layer, format_sensor_popup
from map_routing.risk_zones import get_geojson_risk_zones

def evaluate_route_safety(start_coords, end_coords, hazard_points):
    """
    Evaluates risk score along a route and returns map rendering + path status.
    """
    m = create_base_map(center_lat=start_coords[0], center_lng=start_coords[1])
    
    # Render Risk Heatmap
    add_heatmap_layer(m, hazard_points)
    
    # Render GeoJSON zones
    geojson_data = get_geojson_risk_zones()
    
    return {
        "status": "ANALYZED",
        "map_html": m._repr_html_(),
        "geojson": geojson_data
    }