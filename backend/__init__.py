import socketserver
from http import HTTPStatus, server
from os import path
from urllib.request import urlopen
import json
from typing import Dict, List,  Union

from sklearn.linear_model import LinearRegression, SGDRegressor

PORT = 9487


class Handler(server.SimpleHTTPRequestHandler):
    _data_url = 'https://data.coa.gov.tw/Service/OpenData/FromM/{}.aspx'

    _data_sources = {
        'PoultryTransBoiledChickenData': {
            '白肉雞(2.0Kg以上)': '白肉雞（2.0kg以上）',
            '白肉雞(1.75-1.95Kg)': '白肉雞（1.75~1.95kg）',
            '白肉雞(門市價高屏)': '白肉雞（門市價，高屏）',
            '雞蛋(產地)': '雞蛋（產地）',
        },
        'PoultryTransLocalChickenData': {
            '黑羽土雞公舍飼': '黑羽土雞（南區，公，舍飼）',
            '黑羽土雞母舍飼': '黑羽土雞（南區，母，舍飼）',
        },
        'PoultryTransGooseDuckData': {
            '肉鵝(白羅曼)': '肉鵝（白羅曼）',
            '正番鴨(公)': '正番鴨（公）',
            '土番鴨(75天)': '土番鴨（75天）',
            '鴨蛋(新蛋)(台南)': '鴨蛋（新蛋，台南）',
        },
        'PoultryTransLocalRedChickenData': {
            '紅羽土雞北區': '紅羽土雞（北區）',
            '紅羽土雞中區': '紅羽土雞（中區）',
            '紅羽土雞南區': '紅羽土雞（南區）',
        },
        'PoultryTransLocalBlackChickenData': {
            '黑羽土雞舍飼(南區)公': '黑羽土雞（南區，公，舍飼）',
            '黑羽土雞舍飼(南區)母': '黑羽土雞（南區，母，舍飼）',
        },
    }

    @staticmethod
    def _process_raw_data(
        raw_data: List[Dict[str, str]],
        fields: Dict[str, str],
    ) -> Dict[str, List[Dict[str, Union[str, float]]]]:
        result = dict()
        for node in raw_data:
            date = node['日期']
            for field, name in fields.items():
                if name not in result:
                    result[name] = list()
                rawValue: str = node[field]
                if rawValue != '休市' and rawValue != '-' and rawValue != '':
                    if '..' in rawValue:
                        rawValue = rawValue.replace('..', '.')
                    if '-' in rawValue:
                        rawValues = rawValue.split('-')
                        rawValue = (
                            float(rawValues[0]) + float(rawValues[1])) / 2
                    value = float(rawValue)
                    if value > 0:
                        result[name].append({'date': date, 'value': value})
        return result

    def __init__(self, *args, directory=None, **kwargs):
        self._data = None
        directory = path.join(path.dirname(__file__), '../dist')
        super().__init__(*args, directory=directory, **kwargs)

    def _get_data(self):
        self._data = dict()
        for src, fields in Handler._data_sources.items():
            with urlopen(Handler._data_url.format(src)) as f:
                raw_data = json.load(f)
            for k, v in Handler._process_raw_data(raw_data, fields).items():
                if k in self._data:
                    v.extend(self._data[k])
                self._data[k] = v

    def do_GET(self):
        def send_json_head():
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        if self.path == '/api/data':
            if self._data is None:
                self._get_data()
            send_json_head()
            self.wfile.write(json.dumps(
                self._data, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/api/pred':
            send_json_head()
            self.wfile.write(b'{"a":1,"b":2}')
        else:
            super().do_GET()


def run_server():
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        httpd.serve_forever()
