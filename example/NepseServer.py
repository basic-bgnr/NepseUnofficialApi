import flask
from flask import Flask, request
from json import JSONDecodeError

try:
    from nepse import Nepse
except ImportError:
    import sys

    sys.path.append("../")
    from nepse import Nepse

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True


nepse = Nepse()
nepse.setTLSVerification(False)

routes = {
    "PriceVolume": "/PriceVolume",
    "Summary": "/Summary",
    "SupplyDemand": "/SupplyDemand",
    "TopGainers": "/TopGainers",
    "TopLosers": "/TopLosers",
    "TopTenTradeScrips": "/TopTenTradeScrips",
    "TopTenTurnoverScrips": "/TopTenTurnoverScrips",
    "TopTenTransactionScrips": "/TopTenTransactionScrips",
    "IsNepseOpen": "/IsNepseOpen",
    "NepseIndex": "/NepseIndex",
    "NepseSubIndices": "/NepseSubIndices",
    "DailyNepseIndexGraph": "/DailyNepseIndexGraph",
    "DailyScripPriceGraph": "/DailyScripPriceGraph",
    "CompanyList": "/CompanyList",
    "SecurityList": "/SecurityList",
    "TradeTurnoverTransactionSubindices": "/TradeTurnoverTransactionSubindices",
    "LiveMarket": "/LiveMarket",
    "MarketDepth": "/MarketDepth",
}


@app.route("/")
def getIndex():
    content = "<BR>".join(
        [f"<a href={value}> {key} </a>" for key, value in routes.items()]
    )
    return f"Serverving hot stock data <BR>{content}"


@app.route(routes["Summary"])
def getSummary():
    response = flask.jsonify(_getSummary())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def _getSummary():
    response = dict()
    for obj in nepse.getSummary():
        response[obj["detail"]] = obj["value"]
    return response


@app.route(routes["NepseIndex"])
def getNepseIndex():
    response = flask.jsonify(_getNepseIndex())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def _getNepseIndex():
    response = dict()
    for obj in nepse.getNepseIndex():
        response[obj["index"]] = obj
    return response


@app.route(routes["NepseSubIndices"])
def getNepseSubIndices():
    response = flask.jsonify(_getNepseSubIndices())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def _getNepseSubIndices():
    response = dict()
    for obj in nepse.getNepseSubIndices():
        response[obj["index"]] = obj
    return response


@app.route(routes["TopTenTradeScrips"])
def getTopTenTradeScrips():
    response = flask.jsonify(nepse.getTopTenTradeScrips())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(routes["TopTenTransactionScrips"])
def getTopTenTransactionScrips():
    response = flask.jsonify(nepse.getTopTenTransactionScrips())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(routes["TopTenTurnoverScrips"])
def getTopTenTurnoverScrips():
    response = flask.jsonify(nepse.getTopTenTurnoverScrips())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(routes["SupplyDemand"])
def getSupplyDemand():
    response = flask.jsonify(nepse.getSupplyDemand())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(routes["TopGainers"])
def getTopGainers():
    response = flask.jsonify(nepse.getTopGainers())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(routes["TopLosers"])
def getTopLosers():
    response = flask.jsonify(nepse.getTopLosers())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(routes["IsNepseOpen"])
def isNepseOpen():
    response = flask.jsonify(nepse.isNepseOpen())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(routes["DailyNepseIndexGraph"])
def getDailyNepseIndexGraph():
    response = flask.jsonify(nepse.getDailyNepseIndexGraph())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(routes["DailyScripPriceGraph"])
def getDailyScripPriceGraph():
    args = request.args
    param_scrip_name = args.get("symbol")
    print(param_scrip_name)
    response = flask.jsonify(nepse.getDailyScripPriceGraph(param_scrip_name))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(routes["CompanyList"])
def getCompanyList():
    response = flask.jsonify(nepse.getCompanyList())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(routes["CompanyList"])
def getSecurityList():
    response = flask.jsonify(nepse.getSecurityList())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(routes["PriceVolume"])
def getPriceVolume():
    response = flask.jsonify(nepse.getPriceVolume())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(routes["LiveMarket"])
def getLiveMarket():
    response = flask.jsonify(nepse.getLiveMarket())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route(f"{routes['MarketDepth']}", defaults={"symbol": None})
@app.route(f"{routes['MarketDepth']}/<string:symbol>")
def getMarketDepth(symbol):
    if symbol:
        try:
            response = flask.jsonify(nepse.getSymbolMarketDepth(symbol))
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        except JSONDecodeError:
            return None
    else:
        symbols = nepse.getSecurityList()
        response = "<BR>".join(
            [
                f"<a href={routes['MarketDepth']}/{symbol['symbol']}> {symbol['symbol']} </a>"
                for symbol in symbols
            ]
        )
        return response


@app.route(routes["TradeTurnoverTransactionSubindices"])
def getTradeTurnoverTransactionSubindices():
    companies = {company["symbol"]: company for company in nepse.getCompanyList()}
    turnover = {obj["symbol"]: obj for obj in nepse.getTopTenTurnoverScrips()}
    transaction = {obj["symbol"]: obj for obj in nepse.getTopTenTransactionScrips()}
    trade = {obj["symbol"]: obj for obj in nepse.getTopTenTradeScrips()}

    gainers = {obj["symbol"]: obj for obj in nepse.getTopGainers()}
    losers = {obj["symbol"]: obj for obj in nepse.getTopLosers()}

    price_vol_info = {obj["symbol"]: obj for obj in nepse.getPriceVolume()}

    sector_sub_indices = _getNepseSubIndices()
    # this is done since nepse sub indices and sector name are different
    sector_mapper = {
        "Commercial Banks": "Banking SubIndex",
        "Development Banks": "Development Bank Index",
        "Finance": "Finance Index",
        "Hotels And Tourism": "Hotels And Tourism Index",
        "Hydro Power": "HydroPower Index",
        "Investment": "Investment Index",
        "Life Insurance": "Life Insurance",
        "Manufacturing And Processing": "Manufacturing And Processing",
        "Microfinance": "Microfinance Index",
        "Mutual Fund": "Mutual Fund",
        "Non Life Insurance": "Non Life Insurance",
        "Others": "Others Index",
        "Tradings": "Trading Index",
    }

    scrips_details = dict()
    for symbol, company in companies.items():
        company_details = {}

        company_details["symbol"] = symbol
        company_details["sectorName"] = company["sectorName"]
        company_details["totalTurnover"] = (
            turnover[symbol]["turnover"] if symbol in turnover.keys() else 0
        )
        company_details["totalTrades"] = (
            transaction[symbol]["totalTrades"] if symbol in transaction.keys() else 0
        )
        company_details["totalTradeQuantity"] = (
            trade[symbol]["shareTraded"] if symbol in transaction.keys() else 0
        )

        if symbol in gainers.keys():
            (
                company_details["pointChange"],
                company_details["percentageChange"],
                company_details["ltp"],
            ) = (
                gainers[symbol]["pointChange"],
                gainers[symbol]["percentageChange"],
                gainers[symbol]["ltp"],
            )
        elif symbol in losers.keys():
            (
                company_details["pointChange"],
                company_details["percentageChange"],
                company_details["ltp"],
            ) = (
                losers[symbol]["pointChange"],
                losers[symbol]["percentageChange"],
                losers[symbol]["ltp"],
            )
        else:
            (
                company_details["pointChange"],
                company_details["percentageChange"],
                company_details["ltp"],
            ) = (0, 0, 0)

        scrips_details[symbol] = company_details

    sector_details = dict()
    sectors = {company["sectorName"] for company in companies.values()}
    for sector in sectors:
        total_trades, total_trade_quantity, total_turnover = 0, 0, 0
        for scrip_details in scrips_details.values():
            if scrip_details["sectorName"] == sector:
                total_trades += scrip_details["totalTrades"]
                total_trade_quantity += scrip_details["totalTradeQuantity"]
                total_turnover += scrip_details["totalTurnover"]

        sector_details[sector] = {
            "totalTrades": total_trades,
            "totalTradeQuantity": total_trade_quantity,
            "totalTurnover": total_turnover,
            "index": sector_sub_indices[sector_mapper[sector]],
            "sectorName": sector,
        }

    response = flask.jsonify(
        {"scripsDetails": scrips_details, "sectorsDetails": sector_details}
    )

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
