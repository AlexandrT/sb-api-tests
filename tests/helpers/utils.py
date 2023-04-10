import json

from json import JSONDecodeError


def text_to_json(text):
    try:
        payload = json.loads(text)
    except JSONDecodeError:
        payload = text

    return payload