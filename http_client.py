from . import categories
import keypirinha as kp
import keypirinha_net as kpnet
import urllib

def http_request(url, content_type, label, target):
    try:
        opener = kpnet.build_urllib_opener()
        opener.addheaders = [("Accept", content_type)]
        with opener.open(url) as response:
            content = response.read()

        return {
            "category": categories.RESULT,
            "label": label,
            "short_desc": content,
            "target": target,
            "args_hint": kp.ItemArgsHint.FORBIDDEN,
            "hit_hint": kp.ItemHitHint.NOARGS,
            "data_bag": content
        }
    except urllib.error.URLError as e:
        return {
            "target": "error",
            "label": "Something went wrong...",
            "short_desc": f"{e.code}: {e.reason}"
        }
