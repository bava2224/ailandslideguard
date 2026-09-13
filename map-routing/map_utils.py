# map-routing/map_utils.py
import folium
from folium.plugins import HeatMap

def create_base_map(center_lat=10.8505, center_lng=76.2711, zoom=9):
    """Creates a base Folium map instance centered on target terrain."""
    return folium.Map(
        location=[center_lat, center_lng],
        zoom_start=zoom,
        tiles="OpenStreetMap"
    )

def add_heatmap_layer(base_map, risk_points):
    """
    Appends a HeatMap layer to the base map.
    risk_points format: [[lat, lng, risk_weight], ...]
    """
    HeatMap(
        risk_points,
        radius=25,
        blur=15,
        min_opacity=0.4,
        gradient={0.4: 'green', 0.65: 'yellow', 0.85: 'orange', 1.0: 'red'}
    ).add_to(base_map)
    return base_map

def format_sensor_popup(sensor_data):
    """Formats HTML content for map marker popups."""
    color = "red" if sensor_data.get("risk") == "CRITICAL" else "green"
    return f"""
    <div style="font-family: Arial, sans-serif; width: 170px;">
        <h4 style="margin:0 0 5px 0; color:#1A365D;">{sensor_data.get('name', 'Sensor')}</h4>
        <b>ID:</b> {sensor_data.get('id')}<br>
        <b>Moisture:</b> {sensor_data.get('moisture')}%<br>
        <b>Risk Level:</b> <span style="color:{color}; font-weight:bold;">{sensor_data.get('risk')}</span>
    </div>
    """