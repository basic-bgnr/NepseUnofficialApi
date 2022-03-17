import flask
from flask import Flask, request

from NepseLib import Nepse


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True


nepse = Nepse()


routes = {  
            'PriceVolume'    : '/PriceVolume',
            'Summary'        : '/Summary',
            'SupplyDemand'   : '/SupplyDemand',
            'TopGainers'     : '/TopGainers',
            'TopLosers'      : '/TopLosers',
            'TopTenTradeScrips'         : '/TopTenTradeScrips',
            'TopTenTurnoverScrips'      : '/TopTenTurnoverScrips',
            'TopTenTransactionScrips'   : '/TopTenTransactionScrips',
            'IsNepseOpen'    : '/IsNepseOpen',
            'NepseIndex'     : '/NepseIndex',
            'NepseSubIndices': '/NepseSubIndices',
            'DailyNepseIndexGraph': '/DailyNepseIndexGraph',

            'DailyScripPriceGraph': '/DailyScripPriceGraph',
            'CompanyList': '/CompanyList',
         }

@app.route("/")
def getIndex():
    content = '<BR>'.join([f'<a href={value}> {key} </a>' for key, value in routes.items()])
    return f"Serverving hot stock data <BR>{content}"

@app.route(routes['PriceVolume'])
def getPriceVolume():
    import time
    t1 = time.time()
    response = flask.jsonify(nepse.getPriceVolume())
    response.headers.add('Access-Control-Allow-Origin', '*')
    print("time req ", (time.time() - t1))
    return response

@app.route(routes["Summary"])
def getSummary():
    response = flask.jsonify(nepse.getSummary())
    response.headers.add('Access-Control-Allow-Origin', '*')
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

@app.route(routes["NepseIndex"])
def getNepseIndex():
    response = flask.jsonify(nepse.getNepseIndex())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route(routes["NepseSubIndices"])
def getNepseSubIndices():
    response = flask.jsonify(nepse.getNepseSubIndices())
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
        response = flask.jsonify({'company_list': list(nepse.getCompanyIDKeyMap().keys())})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response