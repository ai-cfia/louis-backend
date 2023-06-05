# https://stackoverflow.com/questions/6456304/scrapy-unit-testing

import os

from scrapy.http import HtmlResponse, Request
from scrapy.http.response import Response

def fake_response_from_file(file_name, url):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    request = Request(url=url)
    if not file_name[0] == '/':
        responses_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(responses_dir, file_name)
    else:
        file_path = file_name

    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
    except FileNotFoundError:
        return Response(url=url, status=404)

    response = HtmlResponse(url=url,
        request=request,
        body=file_content,
        encoding='utf-8')
    return response

def fake_response_from_row(row, url):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    request = Request(url=url)
    if not row['html_content']:
        return Response(url=url, status=404, request=request)

    response = HtmlResponse(url=url,
        request=request,
        body=row['html_content'],
        encoding='utf-8')
    return response