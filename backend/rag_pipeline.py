import os
import traceback
try:
    import geopandas as gpd
except ImportError:
    gpd = None

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "pune_datasets")

PUNE_PLANNING_KB = {
    "Population": "7.4 million (2026), projected 10 million by 2041",
    "Area": "516 sq km (PMC jurisdiction)",
    "Major zones": "Hinjewadi (IT), Pimpri-Chinchwad (Industrial), Kalyani Nagar (Residential/Commercial)",
    "Current initiatives": "Pune Metro Phase 1 expansion, Mula-Mutha Riverfront Development"
}

PUNE_STATS = {
    "building_count": 0,
    "total_building_area": 0.0,
    "mean_building_area": 0.0,
    "landuse_distribution": {},
    "road_length_by_type": {},
    "waterway_count": 0,
    "waterway_total_length": 0.0,
    "natural_area_count": 0,
    "natural_total_area": 0.0
}

def load_stats():
    if gpd is None:
        print("Geopandas not installed. Skipping shapefile loading.")
        return

    # 1. Buildings
    try:
        buildings_path = os.path.join(DATA_DIR, "gis_osm_buildings_a_free_1.shp")
        if os.path.exists(buildings_path):
            gdf = gpd.read_file(buildings_path)
            # Area calculation might require projection to CRS like 3857 (meters), 
            # assuming degrees if unprojected. Let's do a basic area calc.
            gdf = gdf.to_crs(epsg=3857)
            PUNE_STATS["building_count"] = len(gdf)
            areas = gdf.geometry.area
            PUNE_STATS["total_building_area"] = float(areas.sum())
            PUNE_STATS["mean_building_area"] = float(areas.mean()) if len(areas) > 0 else 0.0
            print("Loaded buildings.")
    except Exception as e:
        print("Error loading buildings shapefile:", str(e))
        traceback.print_exc()

    # 2. Landuse
    try:
        landuse_path = os.path.join(DATA_DIR, "gis_osm_landuse_a_free_1.shp")
        if os.path.exists(landuse_path):
            gdf = gpd.read_file(landuse_path)
            # count occurrences of each fclass
            if 'fclass' in gdf.columns:
                counts = gdf['fclass'].value_counts().to_dict()
                PUNE_STATS["landuse_distribution"] = {k: int(v) for k, v in counts.items()}
            print("Loaded landuse.")
    except Exception as e:
        print("Error loading landuse shapefile:", str(e))

    # 3. Roads
    try:
        roads_path = os.path.join(DATA_DIR, "gis_osm_roads_free_1.shp")
        if os.path.exists(roads_path):
            gdf = gpd.read_file(roads_path)
            gdf = gdf.to_crs(epsg=3857)
            if 'fclass' in gdf.columns:
                gdf['length_km'] = gdf.geometry.length / 1000.0
                grouped = gdf.groupby('fclass')['length_km'].sum().to_dict()
                PUNE_STATS["road_length_by_type"] = {k: float(v) for k, v in grouped.items()}
            print("Loaded roads.")
    except Exception as e:
        print("Error loading roads shapefile:", str(e))

    # 4. Waterways
    try:
        waterways_path = os.path.join(DATA_DIR, "gis_osm_waterways_free_1.shp")
        if os.path.exists(waterways_path):
            gdf = gpd.read_file(waterways_path)
            gdf = gdf.to_crs(epsg=3857)
            PUNE_STATS["waterway_count"] = len(gdf)
            PUNE_STATS["waterway_total_length"] = float((gdf.geometry.length / 1000.0).sum())
            print("Loaded waterways.")
    except Exception as e:
        print("Error loading waterways shapefile:", str(e))

    # 5. Natural
    try:
        natural_path = os.path.join(DATA_DIR, "gis_osm_natural_a_free_1.shp")
        if os.path.exists(natural_path):
            gdf = gpd.read_file(natural_path)
            gdf = gdf.to_crs(epsg=3857)
            PUNE_STATS["natural_area_count"] = len(gdf)
            PUNE_STATS["natural_total_area"] = float((gdf.geometry.area / 1e6).sum()) # in sq km
            print("Loaded natural areas.")
    except Exception as e:
        print("Error loading natural shapefile:", str(e))

# Run once on import
load_stats()

def query_rag(query_text: str) -> str:
    """
    Very basic RAG logic: check if keywords from the knowledge base or stats
    exist in the query, and return relevant information.
    """
    query_text = query_text.lower()
    responses = []
    
    if "population" in query_text:
        responses.append(f"Population: {PUNE_PLANNING_KB['Population']}")
    if "area" in query_text:
        responses.append(f"Area: {PUNE_PLANNING_KB['Area']}")
    if "zone" in query_text or "hinjewadi" in query_text:
        responses.append(f"Major zones: {PUNE_PLANNING_KB['Major zones']}")
    if "initiative" in query_text or "metro" in query_text or "river" in query_text:
        responses.append(f"Current initiatives: {PUNE_PLANNING_KB['Current initiatives']}")
        
    if "building" in query_text:
        responses.append(f"Pune has {PUNE_STATS['building_count']} buildings recorded, with a total area of {PUNE_STATS['total_building_area']:,.2f} sq meters.")
    if "road" in query_text:
        total_road = sum(PUNE_STATS['road_length_by_type'].values())
        responses.append(f"There is a total of {total_road:,.2f} km of roads recorded.")
    if "landuse" in query_text or "residential" in query_text or "commercial" in query_text:
        responses.append(f"Landuse distribution includes {len(PUNE_STATS['landuse_distribution'])} different classes.")
    if "water" in query_text:
        responses.append(f"There are {PUNE_STATS['waterway_count']} waterways totaling {PUNE_STATS['waterway_total_length']:,.2f} km in length.")
    if "natural" in query_text:
        responses.append(f"There are {PUNE_STATS['natural_area_count']} natural areas covering {PUNE_STATS['natural_total_area']:,.2f} sq km.")
        
    if not responses:
        return "I am a simple RAG assistant for Pune. You can ask me about Pune's population, area, zones, initiatives, buildings, roads, landuse, waterways, or natural areas."
        
    return " ".join(responses)
