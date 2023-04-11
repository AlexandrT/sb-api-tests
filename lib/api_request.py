import requests
import json
import re
import os

from json import JSONDecodeError
from _pytest.reports import TestReport
from lib.config import settings
from tests.conftest import ValueStorage


class ApiRequest:
    methods = ("get", "put", "post", "patch", "delete")
    payload = {}
    headers = {}
    reqType = ""

    def _clear_attributes(self):
        [ delattr(self, attribute) for attribute in list(vars(self)) ]

    def _dump_request(fn):
        def magic(self, url, reqType):
            req = fn(self, url, reqType)

            output = f"{self.reqType.upper()}-request will be send to {self.url}"
            ValueStorage.request = f'curl -X {reqType.upper()} '

            headers = json.dumps(self.headers)
            if len(self.headers) == 0:
                output += f" without any headers"
            else:
                output += f" with headers {headers}"
                for header in self.headers:
                    ValueStorage.request += f'-H "{header}: {self.headers[header]}" ' 

            try:
                payload = json.dumps(self.payload)
            except:
                pass

            if len(self.payload) != 0:
                output += f" with payload '{payload}'"
                ValueStorage.request += f'-d \'{payload.encode("utf-8", errors="replace").decode("cp1251", "replace")}\' '

            ValueStorage.request += f'"{self.url}"'
            print(output)
            return req
        return magic

    def _dump_response(fn):
        def magic(self):
            response = fn(self)

            if len(response.text) == 0:
                start_string = "Empty response"
            else:
                start_string = f"Response {response.text}"
                ValueStorage.response = response.text

            ValueStorage.status_code = response.status_code

            print(f"{start_string} with headers {response.headers} and status-code {response.status_code}")
            
            return response
        return magic

    def set_data(self, payload):
        self.payload = payload

    @_dump_request
    def prepare_request(self, url, reqType):
        self.reqType = reqType
        self.url = url

        reqType = reqType.lower()

        if reqType not in self.methods:
            print("[ERROR] Unknown request type")
            raise Exception(f"Unknown request type {reqType}")

    @_dump_response
    def send(self):
        attr = self.reqType.lower()
        method = getattr(requests, attr)
        r = method(self.url, headers=self.headers, json=self.payload)

        self._clear_attributes()

        import time
        time.sleep(3)

        return r

    def add_headers(self, headers):
        self.headers = {**self.headers, **headers}

    def build(self, request_type, request_path, **kwargs):
        uri = url(request_path)
        uri += get_query(**kwargs) if kwargs is not None else None
        self.prepare_request(uri, request_type)

        r = self.send()

        return r

    def authenticate(self, token=None):
        if token is not None:
            self.add_headers({'Authorization': token})


def url(request_path):
    return f"{settings.API_URL}{request_path}"


def get_query(**kwargs):
    output = f"?"

    for param in kwargs:
        output += f"{param}={kwargs[param]}&"

    output = re.sub('[&, ?]*$', '', output)

    return output


def request_path(request_path, **kwargs):
    return request_path.format(**kwargs)


def text_to_json(text):
    try:
        payload = json.loads(text)
    except JSONDecodeError:
        payload = text

    return payload