import requests
# import xmltodict
# import json


def search(query, limit):
    response = requests.get(
        'https://repository.overheid.nl/sru?query=cql.textAndIndexes={query}&maximumRecords={limit}')
    return response


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
