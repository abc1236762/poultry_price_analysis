'''
$ conda create -n ppa --strict-channel-priority -y \
        python=3 numpy scikit-learn pylint autopep8 rope
$ conda activate ppa
$ conda config --env --set channel_priority strict
$ conda list
# packages in environment at /home/user/miniconda3/envs/ppa:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main
astroid                   2.4.1                    py38_0
autopep8                  1.4.4                      py_0
blas                      1.0                         mkl
ca-certificates           2020.1.1                      0
certifi                   2020.4.5.1               py38_0
intel-openmp              2020.1                      217
isort                     4.3.21                   py38_0
joblib                    0.15.1                     py_0
lazy-object-proxy         1.4.3            py38h7b6447c_0
ld_impl_linux-64          2.33.1               h53a641e_7
libedit                   3.1.20181209         hc058e9b_0
libffi                    3.3                  he6710b0_1
libgcc-ng                 9.1.0                hdf63c60_0
libgfortran-ng            7.3.0                hdf63c60_0
libstdcxx-ng              9.1.0                hdf63c60_0
mccabe                    0.6.1                    py38_1
mkl                       2020.1                      217
mkl-service               2.3.0            py38he904b0f_0
mkl_fft                   1.0.15           py38ha843d7b_0
mkl_random                1.1.1            py38h0573a6f_0
ncurses                   6.2                  he6710b0_1
numpy                     1.18.1           py38h4f9e942_0
numpy-base                1.18.1           py38hde5b4d6_1
openssl                   1.1.1g               h7b6447c_0
pip                       20.0.2                   py38_3
pycodestyle               2.6.0                      py_0
pylint                    2.5.2                    py38_0
python                    3.8.3                hcff3b4d_0
readline                  8.0                  h7b6447c_0
rope                      0.17.0                     py_0
scikit-learn              0.22.1           py38hd81dba3_0
scipy                     1.4.1            py38h0b6359f_0
setuptools                47.1.1                   py38_0
six                       1.15.0                     py_0
sqlite                    3.31.1               h62c20be_1
tk                        8.6.8                hbc83047_0
toml                      0.10.0             pyh91ea838_0
wheel                     0.34.2                   py38_0
wrapt                     1.11.2           py38h7b6447c_0
xz                        5.2.5                h7b6447c_0
zlib                      1.2.11               h7b6447c_3
$ conda deactivate
'''

import json
import socketserver
from datetime import datetime, timedelta
from http import HTTPStatus, server
from os import path
from typing import Dict, List, Union
from urllib.parse import parse_qs, unquote, urlparse
from urllib.request import urlopen

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

__all__ = ['PORT', 'run_server']

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

    @staticmethod
    def _gen_date_range(start_str: str, end_str: str) -> List[str]:
        date_range = list()
        time = datetime.strptime(start_str, '%Y/%m/%d')
        end = datetime.strptime(end_str, '%Y/%m/%d')
        step = timedelta(days=1)
        while time <= end:
            date_range.append(time.strftime('%Y/%m/%d'))
            time += step
        return date_range

    @staticmethod
    def _get_data() -> (Dict[str, List[Dict[str, Union[str, float]]]],
                        Dict[str, np.ndarray]):
        data, datasets = dict(), dict()
        for src, fields in Handler._data_sources.items():
            with urlopen(Handler._data_url.format(src)) as f:
                raw_data = json.load(f)
            for k, v in Handler._process_raw_data(raw_data, fields).items():
                if k in data:
                    v.extend(data[k])
                data[k] = v
        for k, v in data.items():
            date_range = Handler._gen_date_range(
                v[-1]['date'], datetime.now().strftime('%Y/%m/%d'))
            dataset = np.empty(len(date_range))
            nodes = v[::-1]
            for i, node in enumerate(nodes):
                start = date_range.index(node['date'])
                if i < len(nodes) - 1:
                    end = date_range.index(nodes[i+1]['date'])
                else:
                    end = len(date_range)
                dataset[start:end] = node['value']
            datasets[k] = dataset
        return data, datasets

    @staticmethod
    def _train_and_predict(
            dataset: np.ndarray, past: int, future: int) -> np.ndarray:
        l = len(dataset)
        x = np.arange(l - past, l).reshape(-1, 1)
        x_pred = np.arange(l, l + future).reshape(-1, 1)
        y = dataset[-past:].reshape(-1, 1)
        lr = make_pipeline(PolynomialFeatures(6), Ridge()).fit(x, y)
        return lr.predict(x_pred).flatten()

    def __init__(self, *args, directory=None, **kwargs):
        self._data: Dict[str, List[Dict[str, Union[str, float]]]] = None
        self._datasets: Dict[np.ndarray] = None
        directory = path.join(path.dirname(__file__), '../../dist')
        super().__init__(*args, directory=directory, **kwargs)

    def _set_send_json_response(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/data':
            data, _ = Handler._get_data()
            self._set_send_json_response()
            self.wfile.write(
                json.dumps(data, ensure_ascii=False).encode('utf-8'))
        elif self.path.startswith('/api/pred'):
            try:
                query = parse_qs(urlparse(self.path).query)
                key = query['key'][0]
                past = int(query['past'][0])
                future = int(query['future'][0])
                _, datasets = Handler._get_data()
                dataset = datasets[key]
                assert 0 < past <= len(dataset) and future > 0
            except:
                super().do_GET()
                return
            pred = Handler._train_and_predict(dataset, past, future)
            self._set_send_json_response()
            self.wfile.write(json.dumps(
                pred.tolist(), ensure_ascii=False).encode('utf-8'))
        else:
            super().do_GET()


def run_server():
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        httpd.serve_forever()
