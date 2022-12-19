from http.server import BaseHTTPRequestHandler
import requests
# import xmltodict
import json


def query_api(params):
    query = params["query"]
    limit = params["limit"]
    response = requests.get(
        'https://repository.overheid.nl/sru?query=cql.textAndIndexes=\"{query}\"&maximumRecords={limit}')
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response


class handler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/xml')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        # origin = self.headers["origin"]
        # if(origin != 'https://findspaces.net'):
        # if(origin != 'http://localhost:3000'):
        #     self.wfile.write(json.dumps(
        #         {"error": str(origin + " " + "not allowed")}).encode())
        #     return
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        # headers = create_headers(bearer_token)
        xml_response = query_api(json.loads(post_body.decode()))
        self.wfile.write(xml_response.text.encode('utf-8'))
        return


# json_obj = xmltodict.parse(response.text)

# total_records = json_obj['sru:searchRetrieveResponse']['sru:numberOfRecords']

# records = json_obj['sru:searchRetrieveResponse']['sru:records']

# print(total_records)

# count = 0

# for record in records['sru:record']:
#     manifestations = record['sru:recordData']['gzd:gzd']['gzd:enrichedData']['gzd:itemUrl']
#     for man in manifestations:
#         if man['@manifestation'] == 'xml' or man['@manifestation'] == 'xml-en' or man['@manifestation'] == 'xml-nl':
#             print(man['#text'])
#             count += 1


# print(count)
