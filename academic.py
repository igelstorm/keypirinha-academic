import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

class Academic(kp.Plugin):
    ITEMCAT_DOI = kp.ItemCategory.USER_BASE + 1
    ITEMCAT_RESULT = kp.ItemCategory.USER_BASE + 1

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
        if self.should_terminate(0.5):
            return

        opener = kpnet.build_urllib_opener()
        opener.addheaders = [("Accept", "text/x-bibliography")]
        with opener.open("https://doi.org/" + user_input) as response:
            refce = response.read()

        refce = refce.decode(encoding="utf-8", errors="strict")

        self.set_suggestions([
            self.create_item(
                category=self.ITEMCAT_RESULT,
                label="Copy plaintext reference",
                short_desc=refce,
                target="plaintext",
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.NOARGS,
                data_bag=refce
            )
        ], kp.Match.ANY, kp.Sort.NONE)

    def on_execute(self, item, action):
        if item.target() == "plaintext":
            kpu.set_clipboard(item.data_bag())
