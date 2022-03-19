import flask
from flask import Flask, request

from NepseLib import Nepse


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


nepse = Nepse()


routes = {
    'PriceVolume': '/PriceVolume',
    'Summary': '/Summary',
    'SupplyDemand': '/SupplyDemand',
    'TopGainers': '/TopGainers',
    'TopLosers': '/TopLosers',
    'TopTenTradeScrips': '/TopTenTradeScrips',
    'TopTenTurnoverScrips': '/TopTenTurnoverScrips',
    'TopTenTransactionScrips': '/TopTenTransactionScrips',
    'IsNepseOpen': '/IsNepseOpen',
    'NepseIndex': '/NepseIndex',
    'NepseSubIndices': '/NepseSubIndices',
    'DailyNepseIndexGraph': '/DailyNepseIndexGraph',

    'DailyScripPriceGraph': '/DailyScripPriceGraph',
    'CompanyList': '/CompanyList',
}


@app.route("/")
def getIndex():
    content = '<BR>'.join(
        [f'<a href={value}> {key} </a>' for key, value in routes.items()])
    return f"Serverving hot stock data <BR>{content}"


@app.route(routes["Summary"])
def getSummary():
    response = flask.jsonify(_getSummary())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
def _getSummary():
    response = dict()
    for obj in nepse.getSummary():
        response[obj['detail']] = obj['value']
    return response

@app.route(routes["NepseIndex"])
def getNepseIndex():
    response = flask.jsonify(_getNepseIndex)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
def _getNepseIndex():
    response = dict()
    for obj in nepse.getNepseIndex():
        response[obj['index']] = obj
    return response
    
@app.route(routes["NepseSubIndices"])
def getNepseSubIndices():
    response = flask.jsonify(_getNepseSubIndices())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
def _getNepseSubIndices():
    response = dict()
    for obj in nepse.getNepseSubIndices():
        response[obj['index']] = obj
    return response

@app.route(routes["TopTenTradeScrips"])
def getTopTenTradeScrips():
    response = flask.jsonify(nepse.getTopTenTradeScrips())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route(routes["TopTenTransactionScrips"])
def getTopTenTransactionScrips():
    response = flask.jsonify(nepse.getTopTenTransactionScrips())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route(routes["TopTenTurnoverScrips"])
def getTopTenTurnoverScrips():
    response = flask.jsonify(nepse.getTopTenTurnoverScrips())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route(routes["SupplyDemand"])
def getSupplyDemand():
    response = flask.jsonify(nepse.getSupplyDemand())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route(routes["TopGainers"])
def getTopGainers():
    response = flask.jsonify(nepse.getTopGainers())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route(routes["TopLosers"])
def getTopLosers():
    response = flask.jsonify(nepse.getTopLosers())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route(routes["IsNepseOpen"])
def isNepseOpen():
    response = flask.jsonify(nepse.isNepseOpen())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response




@app.route(routes["DailyNepseIndexGraph"])
def getDailyNepseIndexGraph():
    response = flask.jsonify(nepse.getDailyNepseIndexGraph())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route(routes["DailyScripPriceGraph"])
def getDailyScripPriceGraph():
    args = request.args
    param_scrip_name = args.get('symbol')
    print(param_scrip_name)
    response = flask.jsonify(nepse.getDailyScripPriceGraph(param_scrip_name))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route(routes["CompanyList"])
def getCompanyList():
    response = flask.jsonify(nepse.getCompanyList())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route(routes["PriceVolume"])
def getPriceVolume():
    companies = {company['symbol']: company['sectorName']
                 for company in nepse.getCompanyList()}
    turnover = {obj['symbol']: obj['turnover']
                for obj in nepse.getTopTenTurnoverScrips()}
    transaction = {obj['symbol']: obj['totalTrades']
                   for obj in nepse.getTopTenTransactionScrips()}
    price_vol_info = nepse.getPriceVolume()

    sector_sub_indices = _getNepseSubIndices()
    #this is done since nepse sub indices and sector name are different 
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
        "Tradings": "Trading Index"
    }



    scrips_details = dict()
    for obj in price_vol_info:
        obj['sectorName'] = companies[obj['symbol']]
        obj['totalTurnover'] = turnover[obj['symbol']]
        obj['totalTrades'] = transaction[obj['symbol']]
        obj['pointsChange'] = obj['percentageChange']/100 * obj['previousClose'] 
        scrips_details[obj['symbol']] = obj
    
    sector_details = dict()
    for sector in set(companies.values()):

        total_trades, total_trade_quantity, total_turnover = 0, 0, 0
        for scrip_details in scrips_details.values():

            if scrip_details['sectorName'] == sector:
                total_trades += scrip_details['totalTrades']
                total_trade_quantity += scrip_details['totalTradeQuantity']
                total_turnover += scrip_details['totalTurnover']

        sector_details[sector] = {'totalTrades': total_trades, 
                                  'totalTradeQuantity':total_trade_quantity, 
                                  'totalTurnover': total_turnover,
                                  'index': sector_sub_indices[sector_mapper[sector]],
                                  'sectorName': sector}


    response = flask.jsonify({'scripsDetails': scrips_details,
                              'sectorsDetails': sector_details})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
