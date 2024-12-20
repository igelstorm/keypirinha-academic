from . import categories
from .doi import Doi
from .journal import Journal
import keypirinha as kp
import keypirinha_util as kpu

class Academic(kp.Plugin):
    def __init__(self):
        super().__init__()

    def on_start(self):
        return

    def on_catalog(self):
        catalog = [
            self.create_item(
                category=categories.DOI,
                label="DOI",
                short_desc="Look up a DOI",
                target="doi",
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.NOARGS
            ),
            self.create_item(
                category=categories.JOURNAL,
                label="Journal abbreviation",
                short_desc="Abbreviate a journal name",
                target="journal",
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.NOARGS
            )
        ]
        self.set_catalog(catalog)

    def on_suggest(self, user_input, items_chain):
        if not items_chain:
            return
        if self.should_terminate(0.2):
            return
        if user_input == "":
            return

        suggestions = []
        if items_chain[-1].category() == categories.DOI:
            doi = Doi(doi = user_input)
            self.__add_suggestion(suggestions, doi.url())
            self.__add_suggestion(suggestions, doi.bibtex())
            self.__add_suggestion(suggestions, doi.plaintext())
        if items_chain[-1].category() == categories.JOURNAL:
            journal = Journal(user_input)
            self.__add_suggestion(suggestions, journal.abbreviation())

    def on_execute(self, item, action):
        if item.target() in ["plaintext", "bibtext"]:
            kpu.set_clipboard(item.data_bag())
        if item.target() == "url":
            kpu.web_browser_command(private_mode=False, url=item.data_bag(), execute=True)

    def __add_suggestion(self, suggestions, item_params):
        if item_params["target"] == "error":
            item = self.create_error_item(**item_params)
        else:
            item = self.create_item(**item_params)

        suggestions.append(item)
        self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.NONE)
