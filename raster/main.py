#!/usr/bin/python
# coding=utf-8
import json
import logging
import os
from copy import deepcopy

import requests

LAYERS_CONFIG = 'https://kadastr.live/style/vector_style_24_03_2023.json'
RASTER_LAYERS = [
    {'name': 'parcels', 'layers': ['land_polygones']},
    {'name': 'dzk__index_map_lines', 'layers': ['dzk__index_map_lines']},
    {'name': 'dzk__pzf', 'layers': ['dzk__pzf']},
    {'name': 'dzk__atu_oblast', 'layers': ['dzk__atu_oblast']},
    {'name': 'dzk__atu_rayon', 'layers': ['dzk__atu_rayon', 'dzk__atu_rayon__text']},
    {'name': 'dzk__atu_terhromad__line', 'layers': ['dzk__atu_terhromad__line', 'dzk__atu_terhromad__text']},
]


def generate_raster_config(original_config, raster_spec):
    new_raster_config = deepcopy(original_config)
    for layer in new_raster_config['layers']:
        if 'layout' not in layer:
            layer['layout'] = {}

        if layer['id'] in raster_spec['layers']:
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

        layer_path = '/styles/' + raster_layer["name"] + '.json'
        with open(layer_path, 'w') as f:
            json.dump(new_config, f)

        raster_layers[raster_layer['name']] = {
            'style': layer_path,
            'serve_rendered': True
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
