from shiny import App, ui
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


# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

BASE = Path(__file__).parent
www_dir = BASE / "www"

tif_file = www_dir / "ALFL_Alaska_2020.tif"


# -------------------------------------------------------------------
# UI
# -------------------------------------------------------------------

app_ui = ui.page_fluid(
    output_widget("map_widget", height="800px")
)


# -------------------------------------------------------------------
# Server
# -------------------------------------------------------------------

def server(input, output, session):

    @render_widget
    def map_widget():

        # Create tile client
        client = TileClient(str(tif_file))

        # Raster center
        center = client.center()

        # -------------------------------------------------------------------
        # Basemaps
        # -------------------------------------------------------------------

        positron = basemap_to_tiles(basemaps.CartoDB.Positron)
        positron.base = True
        positron.name = "Positron"

        osm = basemap_to_tiles(basemaps.OpenStreetMap.Mapnik)
        osm.base = True
        osm.name = "OpenStreetMap"

        esri = basemap_to_tiles(basemaps.Esri.WorldImagery)
        esri.base = True
        esri.name = "Satellite"

        # -------------------------------------------------------------------
        # Raster layers
        # -------------------------------------------------------------------

        mean_density = get_leaflet_tile_layer(
            client,
            indexes=1,
            colormap="ylgn",
            name="Mean Density",
        )

        mean_detection = get_leaflet_tile_layer(
            client,
            indexes=3,
            colormap="ylgn",
            name="Mean Detection",
        )

        # -------------------------------------------------------------------
        # Map
        # -------------------------------------------------------------------

        m = Map(
            center=center,
            zoom=5,
            layers=[esri, mean_density],
        )

        # Optional overlay
        m.add(mean_detection)

        # Controls
        m.add(LayersControl(position="topright", collapsed=False))
        m.add(ScaleControl(position="bottomleft"))
        m.add(FullScreenControl())

        return m


# -------------------------------------------------------------------
# App
# -------------------------------------------------------------------

app = App(app_ui, server, static_assets=www_dir)