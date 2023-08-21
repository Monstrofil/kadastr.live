#!/usr/bin/python
# coding=utf-8
import json
import logging
import os
from copy import deepcopy
from dataclasses import dataclass
from typing import List

import requests


@dataclass
class Layer:
    name: str
    layers: List[str]
    description: str
    preview_bbox: List[float] = None


LAYERS_CONFIG = 'https://kadastr.live/style/vector_style_30_04_2023.json'
RASTER_LAYERS = [
    Layer(name='parcels', layers=['land_polygones'],
          description="Растрові зображення земельних ділянок",
          preview_bbox=[30.497864, 50.439147, 30.518281, 50.445769]),
    Layer(name='dzk__index_map_lines', layers=['dzk__index_map_lines'],
          description="Растрові зображення індексної карти земельного кадастру",
          preview_bbox=[30.497864, 50.439147, 30.518281, 50.445769]),
    Layer(name='dzk__pzf', layers=['dzk__pzf'],
          description="Растрові зображення меж об'єктів природно-заповідного фонду",
          preview_bbox=[29.454345, 47.654288, 37.238159, 49.077465]),
    Layer(name='dzk__atu_oblast', layers=['dzk__atu_oblast'],
          description="Растрові зображення меж областей",
          preview_bbox=[29.454346, 47.654288, 37.238159, 49.077466]),
    Layer(name='dzk__atu_rayon', layers=['dzk__atu_rayon', 'dzk__atu_rayon__text'],
          description="Растрові зображення меж районів",
          preview_bbox=[28.171692, 49.089832, 28.825035, 49.307217]),
    Layer(name='dzk__atu_terhromad__line', layers=['dzk__atu_terhromad__line', 'dzk__atu_terhromad__text'],
          description="Растрові зображення меж територіальних громад",
          preview_bbox=[34.857216, 48.524677, 35.122261, 48.587282]),
    Layer(name='other__water__line',
          layers=['water_lines_large', 'water_lines_middle_rivers', 'water_lines_other', 'water_lines_text'],
          description="Растрові зображення водних басейнів",
          preview_bbox=[27.354455,48.622726,27.395289,48.636468]),
    Layer(name='nsdi__river_basin',
          layers=['river_basin'],
          description="Растрові зображення меж річкових басейнів",
          preview_bbox=[29.454346, 47.654288, 37.238159, 49.077464]),
    Layer(name='nsdi__river_subbasin',
          layers=['river_subbasin'],
          description="Растрові зображення меж річкових суббасейнів",
          preview_bbox=[29.454346, 47.654288, 37.238159, 49.077464]),
    Layer(name='nsdi__manage_parcel',
          layers=['manage_parcel'],
          description="Растрові зображення меж водогосподарств",
          preview_bbox=[29.454346, 47.654288, 37.238159, 49.077464]),
]


def generate_raster_config(original_config, raster_spec):
    new_raster_config = deepcopy(original_config)
    for layer in new_raster_config['layers']:
        if 'layout' not in layer:
            layer['layout'] = {}

        if layer['id'] in raster_spec.layers:
            layer['layout']['visibility'] = 'visible'
        else:
            layer['layout']['visibility'] = 'none'
    return new_raster_config


def main():
    os.makedirs('/configs', exist_ok=True)
    os.makedirs('/styles', exist_ok=True)

    original_config = requests.get(LAYERS_CONFIG).json()

    raster_layers = {}
    for raster_layer in RASTER_LAYERS:
        new_config = generate_raster_config(
            original_config, raster_layer)

        layer_path = '/styles/' + raster_layer.name + '.json'
        with open(layer_path, 'w') as f:
            json.dump(new_config, f)

        raster_layers[raster_layer.name] = {
            'style': layer_path,
            'serve_rendered': True,
            'tilejson': {
                'type': "overlay",
                'description': raster_layer.description,
                'preview': f'/tiles/raster/styles/{raster_layer.name}/static/{raster_layer.preview_bbox[0]},'
                           f'{raster_layer.preview_bbox[1]},'
                           f'{raster_layer.preview_bbox[2]},'
                           f'{raster_layer.preview_bbox[3]}/800x200.png'
                if raster_layer.preview_bbox else None,
                'bounds': [21.203613, 44.134913, 40.209961, 52.442618]
            }
        }

    with open('/configs/config.json', 'w') as f:
        json.dump({
            "options": {
                "paths": {
                    "root": "/data",
                    "mbtiles": "/data"
                },
                "serveStaticMaps": True,
                "formatQuality": {
                    "jpeg": 90,
                    "webp": 90
                },
                "maxSize": 8192,
                "pbfAlias": "pbf"
            },
            "styles": raster_layers
        }, f)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
