from nepse import Nepse
import json

share_market = Nepse()
share_market.setTLSVerification(False)

summary = {item["detail"]: item["value"] for item in share_market.getSummary()}
print(json.dumps(summary))
