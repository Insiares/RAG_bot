import requests
import json


def brave_api(msg: str, brave: str) -> json:
    '''request constructor for brave api

    Args:
        msg (str): user message
        brave (str): brave api token

    Returns:
        json: json response from brave api
    '''
    url = "https://api.search.brave.com/res/v1/web/search"

    querystring = {"q": msg}

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": brave,
    }
    response = requests.get(url, headers=headers, params=querystring)
    json.dump(response.json(), open("results.json", "w"))
    return response.json()


def extract_descriptions_and_urls_to_json(json_data: json) -> list[dict]:
    '''extract descriptions and urls from json data

    Args:
        json_data (json): json data from brave api

    Returns:
        list[dict]: list of dictionaries with descriptions and urls
    '''
    results = json_data.get("web", {}).get("results", [])

    output_data = {"results": []}
    for result in results:
        description = result.get("description")
        url = result.get("url")
        output_data["results"].append({"description": description, "url": url})
    return output_data
