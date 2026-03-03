
import pandas as pd
import folium
import requests
import os

# Load Mapbox token from environment variable for security
# Set this in your terminal with: export MAPBOX_ACCESS_TOKEN="your_token_here"
MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN", "")

if not MAPBOX_ACCESS_TOKEN:
    raise ValueError("MAPBOX_ACCESS_TOKEN environment variable is not set. "
                     "Run: export MAPBOX_ACCESS_TOKEN='your_token_here'")

MAPBOX_STYLE_ID = "mirandagrein/cmm3mni2f000901qu8ut8fzx2"

MAPBOX_TILE_URL = f"https://api.mapbox.com/styles/v1/{MAPBOX_STYLE_ID}/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={MAPBOX_ACCESS_TOKEN}"

CSV_FILE_PATH = os.path.expanduser("~/Downloads/Hometown.csv")
OUTPUT_HTML_FILE = "hometown_map.html"

# Map center (Houston, TX area - will be adjusted based on data)
DEFAULT_CENTER = [29.7604, -95.3698]
DEFAULT_ZOOM = 10


LOCATION_STYLES = {
    "Historical Landmarks": {"color": "lightgreen", "icon": "university", "prefix": "fa"},
    "Resturant": {"color": "darkpurple", "icon": "utensils", "prefix": "fa"},
    "Restaurant": {"color": "darkpurple", "icon": "utensils", "prefix": "fa"},
    "Park": {"color": "darkgreen", "icon": "tree", "prefix": "fa"},
    "Cultural Sites": {"color": "darkblue", "icon": "masks-theater", "prefix": "fa"},
    "Shopping District": {"color": "blue", "icon": "shopping-bag", "prefix": "fa"},
    "Educational Institutions": {"color": "cadetblue", "icon": "graduation-cap", "prefix": "fa"},
    "Places of Worship": {"color": "lightblue", "icon": "church", "prefix": "fa"},
    "Default": {"color": "gray", "icon": "map-marker", "prefix": "fa"}
}


#AI used to debug and clean CSV file as I had issues with extra quotes and whitespaces in the CSV.
def clean_csv_value(value):
    """Clean CSV values by removing extra quotes and whitespace."""
    if pd.isna(value):
        return ""
    # Convert to string and strip whitespace
    value = str(value).strip()
    # Remove leading/trailing triple quotes
    while value.startswith('"""') and value.endswith('"""'):
        value = value[3:-3]
    # Remove leading/trailing single quotes
    while value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return value.strip()



def read_csv_file(filepath):
    """
    Read and clean the CSV file containing hometown locations.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        pandas DataFrame with cleaned data
    """
    print(f"Reading CSV file: {filepath}")
    
    try:
        # Try different encodings to handle special characters
        encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings_to_try:
            try:
                df = pd.read_csv(filepath, encoding=encoding)
                print(f"  Successfully read with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            # Fallback: read with errors='replace'
            df = pd.read_csv(filepath, encoding='utf-8', errors='replace')
        
        # Clean all string columns
        for col in df.columns:
            df[col] = df[col].apply(clean_csv_value)
        
        # Strip column names
        df.columns = [col.strip() for col in df.columns]
        
        print(f"Successfully loaded {len(df)} locations")
        print(f"Location types found: {df['Type'].unique().tolist()}")
        
        return df
        
    except FileNotFoundError:
        print(f" Error: CSV file not found at {filepath}")
        raise
    except Exception as e:
        print(f" Error reading CSV file: {e}")
        raise


def geocode_address(address, access_token):
    """
    Geocode an address using the Mapbox Geocoding API.
    
    Args:
        address: Street address to geocode
        access_token: Mapbox API access token
        
    Returns:
        Tuple of (latitude, longitude) or None if geocoding fails
    """
    
    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"
    
    encoded_address = requests.utils.quote(address)
    
    url = f"{base_url}/{encoded_address}.json?access_token={access_token}&limit=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("features") and len(data["features"]) > 0:
            # Mapbox returns coordinates as [longitude, latitude]
            coordinates = data["features"][0]["geometry"]["coordinates"]
            longitude, latitude = coordinates[0], coordinates[1]
            return (latitude, longitude)
        else:
            print(f" No geocoding results for: {address}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Geocoding error for '{address}': {e}")
        return None


def geocode_all_locations(df, access_token):
    """
    Geocode all addresses in the DataFrame.
    
    Args:
        df: DataFrame with 'Address' column
        access_token: Mapbox API access token
        
    Returns:
        DataFrame with added 'Latitude' and 'Longitude' columns
    """
    print("\n Geocoding addresses using Mapbox API...")
    
    latitudes = []
    longitudes = []
    
    for idx, row in df.iterrows():
        address = row["Address"]
        print(f"  Geocoding: {row['Name'][:30]}...")
        
        coords = geocode_address(address, access_token)
        
        if coords:
            latitudes.append(coords[0])
            longitudes.append(coords[1])
            print(f"      Found: ({coords[0]:.6f}, {coords[1]:.6f})")
        else:
            latitudes.append(None)
            longitudes.append(None)
            print(f"     Could not geocode")
    
    df["Latitude"] = latitudes
    df["Longitude"] = longitudes
    
    # Report success rate
    success_count = df["Latitude"].notna().sum()
    print(f"\n  Successfully geocoded {success_count}/{len(df)} locations")
    
    return df


def get_marker_style(location_type):
    """
    Get the marker style (color/icon) for a location type.
    
    Args:
        location_type: The type of location
        
    Returns:
        Dictionary with color and icon settings
    """
    return LOCATION_STYLES.get(location_type, LOCATION_STYLES["Default"])


def create_popup_html(name, description, image_url, location_type):
    """
    Create HTML content for a marker popup.
    
    Args:
        name: Location name
        description: Personal description of the location
        image_url: URL to an image of the location
        location_type: Type of location
        
    Returns:
        HTML string for the popup
    """
    # Get style for the location type
    style = get_marker_style(location_type)
    
    # Create HTML with styling
    html = f"""
    <div style="width: 300px; font-family: Arial, sans-serif;">
        <h3 style="margin: 0 0 8px 0; color: #333; font-size: 16px; border-bottom: 2px solid {style['color']}; padding-bottom: 5px;">
            {name}
        </h3>
        <p style="margin: 5px 0; color: #666; font-size: 11px; font-weight: bold;">
            📍 {location_type}
        </p>
        <img src="{image_url}" 
             alt="{name}" 
             style="width: 100%; max-height: 150px; object-fit: cover; border-radius: 5px; margin: 8px 0;"
             onerror="this.style.display='none'">
        <p style="margin: 8px 0; color: #444; font-size: 12px; line-height: 1.4;">
            {description}
        </p>
    </div>
    """
    return html


def create_map(df):
    """
    Create a Folium map with custom Mapbox basemap and markers.
    
    Args:
        df: DataFrame with geocoded locations
        
    Returns:
        Folium Map object
    """
    print("\n  Creating interactive map...")
    
    # Filter out locations without coordinates
    df_valid = df.dropna(subset=["Latitude", "Longitude"])
    
    if df_valid.empty:
        print(" No valid coordinates found. Cannot create map.")
        return None
    
    # Calculate map center based on average of all coordinates
    center_lat = df_valid["Latitude"].mean()
    center_lon = df_valid["Longitude"].mean()
    
    print(f"   Map center: ({center_lat:.4f}, {center_lon:.4f})")
    
    # Create the base map with custom Mapbox tiles
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=DEFAULT_ZOOM,
        tiles=None  # We'll add custom tiles
    )
    
    # Add custom Mapbox tile layer
    folium.TileLayer(
        tiles=MAPBOX_TILE_URL,
        attr="Mapbox",
        name="Custom Mapbox Style",
        overlay=False,
        control=True
    ).add_to(m)
    
    # Create feature groups for each location type (for layer control)
    type_groups = {}
    
    # Add markers for each location
    for idx, row in df_valid.iterrows():
        name = row["Name"]
        description = row["Description"]
        image_url = row["Image_URL"]
        location_type = row["Type"]
        lat = row["Latitude"]
        lon = row["Longitude"]
        
        # Get marker style
        style = get_marker_style(location_type)
        
        # Create or get the feature group for this type
        if location_type not in type_groups:
            type_groups[location_type] = folium.FeatureGroup(name=location_type)
        
        # Create popup HTML
        popup_html = create_popup_html(name, description, image_url, location_type)
        popup = folium.Popup(popup_html, max_width=320)
        
        # Create marker with custom icon
        marker = folium.Marker(
            location=[lat, lon],
            popup=popup,
            tooltip=name,
            icon=folium.Icon(
                color=style["color"],
                icon=style["icon"],
                prefix=style["prefix"]
            )
        )
        
        # Add marker to the appropriate feature group
        marker.add_to(type_groups[location_type])
        
        print(f"   Added marker: {name[:30]}... ({location_type})")
    
    # Add all feature groups to the map
    for group in type_groups.values():
        group.add_to(m)
    
    # Add layer control to toggle location types
    folium.LayerControl(collapsed=False).add_to(m)
    
    print(f"\n Created map with {len(df_valid)} markers")
    
    return m


def create_legend_html():
    """Create a legend HTML for the map."""
    legend_items = ""
    for loc_type, style in LOCATION_STYLES.items():
        if loc_type != "Default":
            legend_items += f"""
            <div style="display: flex; align-items: center; margin: 3px 0;">
                <i class="fa fa-{style['icon']}" style="color: {style['color']}; margin-right: 8px; width: 16px;"></i>
                <span style="font-size: 11px;">{loc_type}</span>
            </div>
            """
    
    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        background-color: white;
        padding: 10px 15px;
        border-radius: 5px;
        border: 2px solid #ccc;
        z-index: 1000;
        font-family: Arial, sans-serif;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    ">
        <h4 style="margin: 0 0 8px 0; font-size: 13px; border-bottom: 1px solid #ddd; padding-bottom: 5px;">
            Location Types
        </h4>
        {legend_items}
    </div>
    """
    return legend_html


def save_map(m, output_path):
    """
    Save the map to an HTML file.
    
    Args:
        m: Folium Map object
        output_path: Path for the output HTML file
    """
    print(f"\n Saving map to: {output_path}")
    
    # Add legend to the map
    legend_html = create_legend_html()
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save to HTML
    m.save(output_path)
    
    print(f" Map saved successfully!")
    print(f"\n Open '{output_path}' in a web browser to view your interactive map!")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main function to create the hometown map."""
    print("=" * 60)
    print("🏠 HOMETOWN MAP GENERATOR")
    print("=" * 60)
    
    # Step 1: Read CSV file
    df = read_csv_file(CSV_FILE_PATH)
    print("\n Data Preview:")
    print(df[["Name", "Type"]].to_string())
    
    # Step 2: Geocode all addresses
    df = geocode_all_locations(df, MAPBOX_ACCESS_TOKEN)
    
    # Step 3: Create the map
    m = create_map(df)
    
    if m is None:
        print(" Failed to create map. Exiting.")
        return
    
    # Step 4: Save the map
    save_map(m, OUTPUT_HTML_FILE)
    
    print("\n" + "=" * 60)
    print(" HOMETOWN MAP CREATION COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
