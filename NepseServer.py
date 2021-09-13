from flask import Flask 
from NepseLib import Nepse
import json 

app = Flask(__name__)

nepse = Nepse()


routes = {  
            'PriceVolume'    : '/PriceVolume',
            'Summary'        : '/Summary',
            'TopTenScrips'   : '/TopTenScrips',
            'SupplyDemand'   : '/SupplyDemand',
            'TopGainers'     : '/TopGainers',
            'TopLosers'      : '/TopLosers',
            'IsNepseOpen'    : '/IsNepseOpen',
            'NepseIndex'     : '/NepseIndex',
            'NepseSubIndices': '/NepseSubIndices'
         }

@app.route("/")
def getIndex():
    content = '<BR>'.join([f'<a href={value}> {key} </a>' for key, value in routes.items()])
    return f"Serverving hot stock data <BR>{content}"

@app.route(routes['PriceVolume'])
def getPriceVolume():
    response = nepse.getPriceVolume()
    return json.dumps(response)

@app.route(routes["Summary"])
def getSummary():
    return json.dumps(nepse.getSummary())

@app.route(routes["TopTenScrips"])
def getTopTenScrips():
    return json.dumps(nepse.getTopTenScrips())

@app.route(routes["SupplyDemand"])
def getSupplyDemand():
    return json.dumps(nepse.getSupplyDemand())

@app.route(routes["TopGainers"])
def getTopGainers():
    return json.dumps(nepse.getTopGainers())

@app.route(routes["TopLosers"])
def getTopLosers():
   return json.dumps(nepse.getTopLosers())

@app.route(routes["IsNepseOpen"])
def isNepseOpen():
   return json.dumps(nepse.isNepseOpen())

@app.route(routes["NepseIndex"])
def getNepseIndex():
    return json.dumps(nepse.getNepseIndex())

@app.route(routes["NepseSubIndices"])
def getNepseSubIndices():
    return json.dumps(nepse.getNepseSubIndices())