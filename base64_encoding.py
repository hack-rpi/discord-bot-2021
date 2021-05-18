import base64


def encode(original):
    message_bytes = original.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")
    return base64_message


def decode(code):
    base64_bytes = code.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode("ascii")
    return message
