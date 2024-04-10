from nepse.NepseLib import Nepse


__all__ = [
    "Nepse",
]


def main_cli():

    import argparse

    parser = argparse.ArgumentParser(description="cmdline iterface to nepalstock.com")

    parser.add_argument(
        "--start-server",
        action="store_true",
        default=False,
        dest="start_server",
        help="starts local server at 0.0.0.0:8000",
    )
    parser.add_argument(
        "--show-status",
        action="store_true",
        default=False,
        dest="show_status",
        help="dumps Nepse status to the standard output",
    )
    parser.add_argument(
        "--get-floorsheet",
        action="store_true",
        default=False,
        dest="get_floorsheet",
        help="dumps Nepse's floorsheet to the standard output",
    )

    parser.add_argument(
        "--output-file",
        action="store",
        metavar="FILE",
        default=None,
        dest="output_file",
        help="sets the output file for dumping the content",
    )
    parser.add_argument(
        "--hide-progressbar",
        action="store_true",
        default=False,
        dest="hide_progress",
        help="sets the visibility of progress base to False",
    )

    args = parser.parse_args()

    if args.start_server:
        start_server()
    if args.show_status:
        output_content = show_status()
    if args.get_floorsheet:
        output_content = get_floorsheet(not args.hide_progress)

    dump_to_std_file_descriptor(args.output_file, output_content)


def dump_to_std_file_descriptor(output_destination, output_content):

    from pprint import pprint
    import json

    json_dump = json.dumps(output_content)

    if output_destination:
        with open(output_destination, "w") as output_file:
            output_file.write(json_dump)
    else:
        print(json_dump)


def get_floorsheet(show_progress):

    from nepse import Nepse

    share_market = Nepse()
    share_market.setTLSVerification(False)

    floorsheet = share_market.getFloorSheet(show_progress)
    return floorsheet


def show_status():

    from nepse import Nepse

    share_market = Nepse()
    share_market.setTLSVerification(False)

    summary = {item["detail"]: item["value"] for item in share_market.getSummary()}

    return summary


def start_server():

    import flask
    from flask import Flask, request

    from nepse import Nepse

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
        "TradeTurnoverTransactionSubindices": "/TradeTurnoverTransactionSubindices",
    }

    nepse = Nepse()
    nepse.setTLSVerification(False)

    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True

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

    @app.route(routes["PriceVolume"])
    def getPriceVolume():
        response = flask.jsonify(nepse.getPriceVolume())
        response.headers.add("Access-Control-Allow-Origin", "*")
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
                transaction[symbol]["totalTrades"]
                if symbol in transaction.keys()
                else 0
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

    app.run(debug=True, host="0.0.0.0", port=8000)
