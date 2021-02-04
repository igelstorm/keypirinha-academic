import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

class Academic(kp.Plugin):
    ITEMCAT_DOG = kp.ItemCategory.USER_BASE + 1

    def __init__(self):
        super().__init__()

    def on_start(self):
        actions = [
            self.create_action(
                name="bark",
                label="Bark!",
                short_desc="This barks into the clipboard"),
            self.create_action(
                name="browse",
                label="Browse!",
                short_desc="This browses google")
        ]
        self.set_actions(self.ITEMCAT_DOG, actions)

    def on_catalog(self):
        catalog = [
            self.create_item(
                category=self.ITEMCAT_DOG,
                label="Hello!",
                short_desc="This is dog",
                target="target?",
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.NOARGS
            )
        ]
        self.set_catalog(catalog)

    def on_suggest(self, user_input, items_chain):
        if not items_chain or items_chain[-1].category() != self.ITEMCAT_DOG:
            return
        if self.should_terminate(0.5):
            return

        self.set_suggestions([
            self.create_item(
                category=self.ITEMCAT_DOG,
                label="Woof!",
                short_desc="This is dog barking",
                target="target?",
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.NOARGS
            )
        ], kp.Match.ANY, kp.Sort.NONE)

    def on_execute(self, item, action):
        if action and action.name() == "browse":
            kpu.web_browser_command(private_mode=False, url="https://www.google.com",
                                    execute=True)

        if action and action.name() == "bark":
            kpu.set_clipboard("woof")
