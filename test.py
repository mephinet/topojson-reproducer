import topojson as tp
import requests_cache
import geopandas
from io import BytesIO

print("Downloading...")
url = "https://data.bev.gv.at/geoserver/www/data_bev_gv_at/verwaltungsgrenzen/inspire/AT_BEV_AU_AB_epsg3416_20220401.gpkg"
session = requests_cache.CachedSession("mapcache")
res = session.get(url)
print("Parsing...")
gdf = geopandas.read_file(BytesIO(res.content))

print("Filtering out state Niederösterreich...")
state_noe = gdf.loc[gdf.inspireId.str.contains(".BL.3")].to_crs("EPSG:4326")
state_noe.to_file("niederoesterreich-original.json")

print("Simplifying...")
epsilon = 0.025
topo = tp.Topology(state_noe).toposimplify(epsilon)
simplified_gdf = topo.to_gdf()

print("Saving...")
simplified_gdf.to_file("niederoesterreich-simplified.json")
