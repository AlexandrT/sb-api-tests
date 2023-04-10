import json
import os

from jsonschema import validate, RefResolver


def get_resolver(schema):
    schema_path = f"file:////{os.path.dirname(__file__)}/schemas/"

    resolver = RefResolver(schema_path, schema)

    return resolver


def assert_valid_schema(data, schema_file):
    schema = _load_json_schema(schema_file)

    return validate(data, schema, resolver=get_resolver(schema_file))


def _load_json_schema(filename):
    relative_path = os.path.join(f"schemas", filename)
    absolute_path = os.path.join(os.path.dirname(__file__), relative_path)

    with open(absolute_path) as schema_file:
        return json.loads(schema_file.read())