from nepse.NepseLib import Nepse


__all__ = [
    "Nepse",
]
def show_status():

    from nepse import Nepse
    import json
    from pprint import pprint

    share_market = Nepse()
    share_market.setTLSVerification(False)

    summary = {item["detail"]: item["value"] for item in share_market.getSummary()}

    pprint(summary)
