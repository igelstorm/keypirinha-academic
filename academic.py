import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet
import urllib

class Academic(kp.Plugin):
    ITEMCAT_DOI = kp.ItemCategory.USER_BASE + 1
    ITEMCAT_RESULT = kp.ItemCategory.USER_BASE + 1

    ITEMTEXT_PLAINTEXT = { "label": "Copy plaintext reference", "target": "plaintext" }
    ITEMTEXT_BIBTEX    = { "label": "Copy BibTeX reference", "target": "bibtex" }
    ITEMTEXT_URL       = { "label": "Open URL in browser", "target": "url" }

    COPYABLE_TARGETS = [
        "plaintext", "bibtex"
    ]

    def __init__(self):
        super().__init__()

    def on_start(self):
        return

    def on_catalog(self):
        catalog = [
            self.create_item(
                category=self.ITEMCAT_DOI,
                label="DOI",
                short_desc="Look up a DOI",
                target="doi",
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.NOARGS
            )
        ]
        self.set_catalog(catalog)

    def on_suggest(self, user_input, items_chain):
        if not items_chain or items_chain[-1].category() != self.ITEMCAT_DOI:
            return
        if self.should_terminate(0.2):
            return

        suggestions = []

        self.__add_suggestion(suggestions, self.__gimme_url(user_input))

        try:
            self.__add_suggestion(suggestions, self.__gimme_bibtex(user_input))
            self.__add_suggestion(suggestions, self.__gimme_plaintext(user_input))

        except urllib.error.URLError as e:
            self.__add_suggestion(suggestions, self.__error_item(e))

    def on_execute(self, item, action):
        if item.target() in self.COPYABLE_TARGETS:
            kpu.set_clipboard(item.data_bag())
        if item.target() == "url":
            kpu.web_browser_command(private_mode=False, url=item.data_bag(), execute=True)

    def __get_doi(self, doi, content_type):
        opener = kpnet.build_urllib_opener()
        opener.addheaders = [("Accept", content_type)]
        with opener.open(self.__doi_url(doi)) as response:
            refce = response.read()

        return refce.decode(encoding="utf-8", errors="strict")

    def __result_item(self, content, item_text):
        return self.create_item(
                category=self.ITEMCAT_RESULT,
                label=item_text["label"],
                short_desc=content,
                target=item_text["target"],
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.NOARGS,
                data_bag=content
            )

    def __error_item(self, error):
        return self.create_error_item(
            label="Something went wrong...",
            short_desc=f"{error.code}: {error.reason}"
        )

    def __doi_url(self, doi):
        return "https://doi.org/" + doi

    def __add_suggestion(self, suggestions, suggestion):
        suggestions.append(suggestion)
        self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.NONE)

    def __gimme_bibtex(self, user_input):
        return self.__result_item(self.__get_doi(user_input, "application/x-bibtex"), self.ITEMTEXT_BIBTEX)

    def __gimme_plaintext(self, user_input):
        return self.__result_item(self.__get_doi(user_input, "text/x-bibliography"), self.ITEMTEXT_PLAINTEXT)

    def __gimme_url(self, user_input):
        return self.__result_item(self.__doi_url(user_input), self.ITEMTEXT_URL)
