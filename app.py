from shiny import App, ui, reactive
from shinywidgets import render_widget, output_widget

from ipyleaflet import (
    Map,
    basemaps,
    basemap_to_tiles,
    LayersControl,
    ScaleControl,
    FullScreenControl,
)

from localtileserver import TileClient, get_leaflet_tile_layer

from pathlib import Path
from io import BytesIO
import rasterio
from rasterio.plot import show


import requests
import tempfile
SAVE_BASE = Path(__file__).parent
DOWNLOAD_URL = "http://206.12.92.143/data/dashboard/" #CAWA/Canada/CAWA_Canada_1990.tif"
DATA_URL = SAVE_BASE / "data"
CACHE_DIR = Path(__file__).parent / "tif_cache"
CACHE_DIR.mkdir(exist_ok=True)

def tif_path_local(code, country, year):
    return CACHE_DIR / f"{code}_{country}_{year}.tif"

def get_data(url, code, country, year):
    path = tif_path_local(code, country, year)

    if path.exists():
        return path

    response = requests.get(f"{url}/{code}/{country}/{code}_{country}_{year}.tif", stream=True)

    if response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        # data = BytesIO(response.content)
        # print("Data retrieved!")
        # return data
        # with tempfile.NamedTemporaryFile(delete=True) as tmp:
        #     tmp.write(response.content)
        #     tmp.flush()
        # return tmp.name
    else:
        print(f"Failed to retrieve data {response.status_code}")
    return path 
# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

app_ui = ui.page_fluid(
    ui.input_select(
        "region",
        "Choose Region",
        choices={
            "Alaska": "Alaska",
            "Canada": "Canada",
            "Lower48": "Lower 48 (US)"
        },
        selected="Canada",
    ),
    ui.input_select(
        "year",
        "Choose Year",
        choices=[1990, 1995, 2000, 2005, 2010, 2015, 2020],
        selected=2020,
    ),
    ui.input_select(
        "species",
        "Choose Species",
        choices=["ALFL", "AMCR", "AMGO", "AMPI", "AMRE"],
        selected="ALFL",
    ),

    output_widget("map_widget", height="800px")
)

def server(input, output, session):

    # @reactive.calc
    # def tif_path():
    #     return get_data(DOWNLOAD_URL, input.species(), input.region(), input.year())
    
    # @reactive.calc
    # def tile_client():
    #     #return TileClient(str(f"{DATA_URL}/{input.species()}_{input.region()}_{input.year()}.tif"))
    #     return TileClient(str(tif_path()))

    # @render_widget
    # def map_widget():

    #     # Create tile client
    #     client = tile_client()

    #     # Raster center
    #     center = client.center()

    #     # -------------------------------------------------------------------
    #     # Basemaps
    #     # -------------------------------------------------------------------

    #     positron = basemap_to_tiles(basemaps.CartoDB.Positron)
    #     positron.base = True
    #     positron.name = "Positron"

    #     osm = basemap_to_tiles(basemaps.OpenStreetMap.Mapnik)
    #     osm.base = True
    #     osm.name = "OpenStreetMap"

    #     esri = basemap_to_tiles(basemaps.Esri.WorldImagery)
    #     esri.base = True
    #     esri.name = "Satellite"

    #     # -------------------------------------------------------------------
    #     # Raster layers
    #     # -------------------------------------------------------------------

    #     mean_density = get_leaflet_tile_layer(
    #         client,
    #         indexes=1,
    #         colormap="ylgn",
    #         name="Mean Density",
    #     )

    #     mean_detection = get_leaflet_tile_layer(
    #         client,
    #         indexes=3,
    #         colormap="ylgn",
    #         name="Mean Detection",
    #     )

    #     # -------------------------------------------------------------------
    #     # Map
    #     # -------------------------------------------------------------------

    #     m = Map(
    #         center=center,
    #         zoom=3,
    #         layers=[esri, mean_density],
    #     )

    #     # Optional overlay
    #     m.add(mean_detection)

    #     # Controls
    #     m.add(LayersControl(position="topright", collapsed=False))
    #     m.add(ScaleControl(position="bottomleft"))
    #     m.add(FullScreenControl())

    #     return m

    @render_widget
    def map_widget():
    #     return show(rasterio.open(tif_path()))
        with rasterio.open("http://206.12.92.143/data/dashboard/ALFL/Alaska/ALFL_Alaska_1990.tif") as dataset:
        # Read the data for the entire raster (or a specific window)
            data = dataset.read(1)
            show(data)

# -------------------------------------------------------------------
# App
# -------------------------------------------------------------------

app = App(app_ui, server)