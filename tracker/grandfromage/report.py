# -*- coding: utf-8 -*-

__author__ = 'Martyn Whitwell'
__email__ = 'martyn.whitwell()gmail.com'
__version__ = '0.1.0'

import json

class Report:

    def __init__(self, json_data):
        self.json_data = json_data
        obj_data = json.loads(json_data)

        if obj_data is not None \
                and 'class' in obj_data \
                and obj_data['class'] == 'TPV' \
                and 'mode' in obj_data \
                and obj_data['mode'] >= 2 \
                and 'lat' in obj_data \
                and 'lon' in obj_data:
            self.is_tpv_fix = True
            self.lat_lon = (obj_data['lat'], obj_data['lon'])
        else:
            self.is_tpv_fix = False
            self.lat_lon = None