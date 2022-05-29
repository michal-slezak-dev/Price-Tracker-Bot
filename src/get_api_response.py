import requests

def make_a_request(url, headers):
    response = requests.get(url, headers)

def get_json_response(request):
    try:
        res = request.json()
    except Exception as e:
        print(e)
    else:
        return res


def extract_relevant_data(response):
    pass