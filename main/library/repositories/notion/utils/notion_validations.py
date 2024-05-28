import sys, os

sys.path.insert(0, os.path.abspath("."))


def validate_http_response(status_code: int, reason: str, response_data: bytes):
    if 400 <= status_code:
        if reason is not None and reason != "":
            if response_data is not None and response_data != b"":
                raise Exception(
                    f"Request failed with status code {status_code}, reason {reason}, and response data {response_data}"
                )
            else:
                raise Exception(
                    f"Request failed with status code {status_code} and reason {reason}"
                )
        else:
            raise Exception(f"Request failed with status code {status_code}")
