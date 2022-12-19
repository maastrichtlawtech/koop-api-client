from http.server import BaseHTTPRequestHandler
import requests
import json
from urllib import parse
import re


def query_api(xml_url, depth):
    response = requests.get(xml_url)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    citations = re.findall("<extref.*?<\/extref>", response.text)
    return citations


class handler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        citations = query_api(dic["xml_url"], dic["depth"])
        self.wfile.write(json.dumps(citations).encode('utf-8'))
        return
