import base64
import json
# Useful website: https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/


# Takes in a dictionary/array, converts it to json, and encodes it to base64
def encode(json_object):
    original = json.dumps(json_object)
    message_bytes = original.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")
    return add_blank_spaces(base64_message)


# Takes a string and converts it to a json object
def decode(original_code):
    code = remove_blank_spaces(original_code)
    base64_bytes = code.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode("ascii")
    return json.loads(message)


# Adds blank spaces because Discord is stupid and can't handle footers properly
def add_blank_spaces(footer_string):
    new_footer_string = footer_string
    width = 20
    blank_space = "\u200B"
    new_footer_string = blank_space.join(new_footer_string[i:i+width] for i in range(0, len(new_footer_string), width))
    return new_footer_string


# Removes blank spaces because Discord is stupid and can't handle footers properly
def remove_blank_spaces(footer_string):
    if footer_string.count("\u200B") > 0:
        blank_space = "\u200B"
        lis = footer_string.split(blank_space)
        new_footer_string = ""
        for s in lis:
            new_footer_string += s
        return new_footer_string
    return footer_string
