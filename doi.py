import keypirinha as kp
import keypirinha_net as kpnet
import urllib
from .http_client import http_request

class Doi:
    ITEMCAT_RESULT = kp.ItemCategory.USER_BASE + 1
    ITEMTEXT_URL = { "label": "Open URL in browser", "target": "url" }

    def __init__(self, doi):
        self._url = "https://doi.org/" + doi

    def url(self):
        return self.__result_item(self._url, self.ITEMTEXT_URL)

    def bibtex(self):
        return http_request(
            url = self._url,
            content_type = "application/x-bibtex",
            label = "Copy BibTeX reference",
            target = "bibtex"
        )

    def plaintext(self):
        return http_request(
            url = self._url,
            content_type = "text/x-bibliography",
            label = "Copy plaintext reference",
            target = "plaintext"
        )

    def __result_item(self, content, item_text):
        return {
            "category": self.ITEMCAT_RESULT,
            "label": item_text["label"],
            "short_desc": content,
            "target": item_text["target"],
            "args_hint": kp.ItemArgsHint.FORBIDDEN,
            "hit_hint": kp.ItemHitHint.NOARGS,
            "data_bag": content
        }
