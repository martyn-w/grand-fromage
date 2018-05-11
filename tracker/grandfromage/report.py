# -*- coding: utf-8 -*-

__author__ = 'Martyn Whitwell'
__email__ = 'martyn.whitwell()gmail.com'
__version__ = '0.1.0'

import json

class Report:

    def __init__(self, msg):
        self.msg = json.loads(msg)
        self.report_class = self.get_report_class()
        self.is_tpv_fix = self.get_is_tpv_fix()

    def get_report_class(self):
        if self.msg is not None and 'class' in self.msg:
            return self.msg['class']
        else:
            return None

    def get_is_tpv_fix(self):
        return (self.report_class == 'TPV'
            and 'mode' in self.msg
            and self.msg['mode'] >= 2)

    def lat_lon(self):
        if self.is_tpv_fix:
            return (self.msg['lat'], self.msg['lon'])
        else:
            return None

    def json(self):
        return json.dumps(self.msg)
