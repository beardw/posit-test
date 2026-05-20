from shiny import App, Inputs, reactive, ui, render
from shinywidgets import render_widget, output_widget
from ipywidgets import HTML
from ipyleaflet import (
    Map, basemaps,
    basemap_to_tiles, LayersControl, ScaleControl,
    FullScreenControl, WidgetControl
)
from localtileserver import TileClient, get_leaflet_tile_layer

from pathlib import Path

BASE = Path(__file__).parent

file = BASE / "ALFL_Alaska_2020.tif"

app_ui = ui.page_fluid(output_widget("map_widget"))  

def server(input, output, session):
    @render_widget  
    def map():
        return Map(center=(50.6252978589571, 0.34580993652344), zoom=3)  
    

    @render_widget
    def map_widget():

        client = TileClient(file)

        center = client.center()

        positron = basemap_to_tiles(basemaps.CartoDB.Positron)
        positron.base = True
        positron.name = "Positron (minimal)"
        
        osm = basemap_to_tiles(basemaps.OpenStreetMap.Mapnik)
        osm.base = True
        osm.name = "Open Street Map (default)"
        
        esri = basemap_to_tiles(basemap=basemaps.Esri.WorldImagery)
        esri.base = True
        esri.name = "World Imagery (satellite)"

        mean_density = get_leaflet_tile_layer(client, colormap="ylgn", indexes=1, name="Mean Density")
        mean_detection = get_leaflet_tile_layer(client, colormap="ylgn", indexes=3, name="Mean Detection")

        m = Map(layers=[esri, positron, osm],
                center=center,
        )

        # band = client.dataset.read(1).astype(float)
        # rmin = float(np.nanmin(band))
        # rmax = float(np.nanmax(band))

        # legend = WidgetControl(
        #     widget=HTML(f"""
        #     <div class="map-legend">
        #         <div class="map-legend-title">
        #             <b>{rmin:.4f} → {rmax:.4f}</b>
        #         </div>
        #         <div class="map-legend-gradient"></div>
        #     </div>
        #     """),
        #     position="bottomright"
        # )

        m.add(mean_density)
        m.add(mean_detection)

        #m.add(legend)

        m.add(FullScreenControl())
        m.add(LayersControl(collapsed=False, position='topright'))
        m.add(ScaleControl(position='bottomleft'))

        return m

app = App(app_ui, server)