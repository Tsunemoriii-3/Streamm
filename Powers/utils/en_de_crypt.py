import base64
import re

def is_base64(string):
    """Check if a string is Base64 encoded."""
    if len(string) % 4 == 0:
        try:
            base64_bytes = base64.b64decode(string, validate=True)
            try:
                base64_bytes.decode('ascii')
            except UnicodeDecodeError:
                return False
            return True
        except Exception:
            return False
    return False

async def encode_decode(string, to_do="encode"):
    """
    Function to encode or decode strings.
    string: string to be decoded or encoded.
    to_do: 'encode' to encode the string, 'decode' to decode the string.
    """
    string = str(string)
    if to_do.lower() == "encode":
        encodee = string.encode("ascii")
        base64_ = base64.b64encode(encodee)
        B64 = base64_.decode("ascii")

    elif to_do.lower() == "decode":
        if is_base64(string):
            try:
                decodee = string.encode("ascii")
                base64_ = base64.b64decode(decodee)
                B64 = base64_.decode("ascii")
            except Exception as e:
                B64 = string
        else:
            B64 = string

    else:
        B64 = string

    return B64