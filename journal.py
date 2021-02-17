from .http_client import http_request
import urllib

class Journal:
    def __init__(self, name):
        self._name = name

    def abbreviation(self):
        return http_request(
            url = "https://abbreviso.toolforge.org/a/" + urllib.parse.quote(self._name),
            label = "Copy ISO-4 abbreviation",
            target = "plaintext"
        )
