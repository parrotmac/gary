from . import models

import inspect, sys
from pprint import pprint

schema = {}


class String:
    pass


class Int:
    pass


class UUID:
    pass


class JSON:
    pass


class DateTime:
    pass


class Boolean:
    pass


for name, obj in inspect.getmembers(sys.modules[models.__name__]):
    if inspect.isclass(obj):
        if hasattr(obj, "_meta") and not obj._meta.abstract:
            if not hasattr(obj, 'GQLMeta'):
                continue

            obj_gql_name = f"{obj.__name__}Type"
            schema[obj_gql_name] = {}
            fields = obj._meta.fields
            for field in fields:

                if not hasattr(field, "__graphql_enabled"):
                    continue

                match field.get_internal_type():
                    case "CharField" | "TextField":
                        schema[obj_gql_name][field.name] = String
                    case "IntegerField":
                        schema[obj_gql_name][field.name] = Int
                    case "UUIDField":
                        schema[obj_gql_name][field.name] = UUID
                    case "JSONField":
                        schema[obj_gql_name][field.name] = JSON
                    case "DateTimeField":
                        schema[obj_gql_name][field.name] = DateTime
                    case "BooleanField":
                        schema[obj_gql_name][field.name] = Boolean
                    case "ForeignKey" | "AutoField":
                        pprint(field)
                    case _:
                        raise Exception(f"Unknown field type: {field.get_internal_type()}")


def foo():
    pprint(schema)
