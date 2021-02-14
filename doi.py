import keypirinha as kp
import keypirinha_net as kpnet
import urllib

class Doi:
    ITEMCAT_RESULT = kp.ItemCategory.USER_BASE + 1
    ITEMTEXT_URL = { "label": "Open URL in browser", "target": "url" }
    PARAMS_BIBTEX = {
        "label": "Copy BibTeX reference",
        "target": "bibtex",
        "content_type": "application/x-bibtex"
    }
    PARAMS_PLAINTEXT = {
        "label": "Copy plaintext reference",
        "target": "plaintext",
        "content_type": "text/x-bibliography"
    }

    def __init__(self, doi, plugin):
        self._url = "https://doi.org/" + doi
        self._plugin = plugin

    def url(self):
        return self.__result_item(self._url, self.ITEMTEXT_URL)

    def bibtex(self):
        return self.__get_doi(self._url, self.PARAMS_BIBTEX)

    def plaintext(self):
        return self.__get_doi(self._url, self.PARAMS_PLAINTEXT)

    def __result_item(self, content, item_text):
        return self._plugin.create_item(
            category=self.ITEMCAT_RESULT,
            label=item_text["label"],
            short_desc=content,
            target=item_text["target"],
            args_hint=kp.ItemArgsHint.FORBIDDEN,
            hit_hint=kp.ItemHitHint.NOARGS,
            data_bag=content
        )

    def __error_item(self, error):
        return self._plugin.create_error_item(
            label="Something went wrong...",
            short_desc=f"{error.code}: {error.reason}"
        )

    def __get_doi(self, doi, params):
        try:
            opener = kpnet.build_urllib_opener()
            opener.addheaders = [("Accept", params["content_type"])]
            with opener.open(self._url) as response:
                refce = response.read()

            return self.__result_item(
                refce.decode(encoding="utf-8", errors="strict"),
                params
            )
        except urllib.error.URLError as e:
            return self.__error_item(e)
