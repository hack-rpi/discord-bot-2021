import base64
import json


# Takes in a json object
def encode(json_object):
    original = json.dumps(json_object)
    message_bytes = original.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")
    return base64_message


# Takes in a string
def decode(code):
    base64_bytes = code.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode("ascii")
    return json.loads(message)
