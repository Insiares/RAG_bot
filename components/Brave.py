import requests
import json
from bs4 import BeautifulSoup
import re
# from .Selenium import selenium_scraping


def brave_api(msg: str, brave: str) -> json:
    """request constructor for brave api

    Args:
        msg (str): user message
        brave (str): brave api token

    Returns:
        json: json response from brave api
    """
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
    """extract descriptions and urls from json data

    Args:
        json_data (json): json data from brave api

    Returns:
        list[dict]: list of dictionaries with descriptions and urls
    """
    results = json_data.get("web", {}).get("results", [])

    output_data = {"results": []}
    for result in results[:3]:
        description = result.get("description")
        url = result.get("url")

        body = extract_body(url)
        output_data["results"].append(
            {"description": description, "url": url, "body": body[:2500]}
        )
    return output_data


def extract_body(url: str) -> str:
    """extract body from url
    Args:
        url (str): url

    Returns:
        str: body
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        body = soup.body.text
        body = body.replace(r'\n', r'').replace(r'\t', '')
        normalized_text = re.sub(r'\s+', ' ', body).strip()
        normalized_text = re.sub(r'\${.*?}', '', normalized_text).strip()
    except AttributeError as e:
        print(e)
        normalized_text = ""

    return normalized_text
