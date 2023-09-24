import requests
from collections import defaultdict
from json import JSONDecodeError
import json
import time
from datetime import date
import pywasm
import tqdm


class TokenParser:
    def __init__(self):
        self.runtime = pywasm.load("css.wasm")

    def parse_token_response(self, token_response):
        n = self.runtime.exec(
            "cdx",
            [
                token_response["salt1"],
                token_response["salt2"],
                token_response["salt3"],
                token_response["salt4"],
                token_response["salt5"],
            ],
        )
        l = self.runtime.exec(
            "rdx",
            [
                token_response["salt1"],
                token_response["salt2"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )
        o = self.runtime.exec(
            "bdx",
            [
                token_response["salt1"],
                token_response["salt2"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )
        p = self.runtime.exec(
            "ndx",
            [
                token_response["salt1"],
                token_response["salt2"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )
        q = self.runtime.exec(
            "mdx",
            [
                token_response["salt1"],
                token_response["salt2"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )

        a = self.runtime.exec(
            "cdx",
            [
                token_response["salt2"],
                token_response["salt1"],
                token_response["salt3"],
                token_response["salt5"],
                token_response["salt4"],
            ],
        )
        b = self.runtime.exec(
            "rdx",
            [
                token_response["salt2"],
                token_response["salt1"],
                token_response["salt3"],
                token_response["salt4"],
                token_response["salt5"],
            ],
        )
        c = self.runtime.exec(
            "bdx",
            [
                token_response["salt2"],
                token_response["salt1"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )
        d = self.runtime.exec(
            "ndx",
            [
                token_response["salt2"],
                token_response["salt1"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )
        e = self.runtime.exec(
            "mdx",
            [
                token_response["salt2"],
                token_response["salt1"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )

        access_token = token_response["accessToken"]
        refresh_token = token_response["refreshToken"]

        print(f"refresh token index {a}, {b}, {c}, {d}, {e}", refresh_token)
        print(f"access token index {n}, {l}, {o}, {p}, {q}", access_token)

        parsed_access_token = (
            access_token[0:n]
            + access_token[n + 1 : l]
            + access_token[l + 1 : o]
            + access_token[o + 1 : p]
            + access_token[p + 1 : q]
            + access_token[q + 1 :]
        )
        parsed_refresh_token = (
            refresh_token[0:a]
            + refresh_token[a + 1 : b]
            + refresh_token[b + 1 : c]
            + refresh_token[c + 1 : d]
            + refresh_token[d + 1 : e]
            + refresh_token[e + 1 :]
        )

        # returns both access_token and refresh_token, i don't know what's the purpose of refresh token.
        # Right now new access_token can be used for every new api request
        return (parsed_access_token, parsed_refresh_token)


class Nepse:
    def __init__(self):
        self.token_request_count = 0
        self.total_request_count = 0

        self.token_parser = TokenParser()

        self.base_url = "https://www.nepalstock.com.np"

        self.token_url = f"{self.base_url}/api/authenticate/prove"
        self.refresh_url = f"{self.base_url}/api/authenticate/refresh-token"

        self.post_payload_id = None
        self.company_symbol_id_keymap = None
        self.company_list = None

        self.floor_sheet_size = 500

        self.api_end_points = {
            "price_volume_url": f"{self.base_url}/api/nots/securityDailyTradeStat/58",
            "summary_url": f"{self.base_url}/api/nots/market-summary/",
            "supply_demand_url": f"{self.base_url}/api/nots/nepse-data/supplydemand",
            "turnover_url": f"{self.base_url}/api/nots/top-ten/turnover",
            "top_gainers_url": f"{self.base_url}/api/nots/top-ten/top-gainer",
            "top_losers_url": f"{self.base_url}/api/nots/top-ten/top-loser",
            "top_ten_trade_url": f"{self.base_url}/api/nots/top-ten/trade",
            "top_ten_transaction_url": f"{self.base_url}/api/nots/top-ten/transaction",
            "top_ten_turnover_url": f"{self.base_url}/api/nots/top-ten/turnover",
            "nepse_open_url": f"{self.base_url}/api/nots/nepse-data/market-open",
            "nepse_index_url": f"{self.base_url}/api/nots/nepse-index",
            "nepse_subindices_url": f"{self.base_url}/api/nots",
            "nepse_isopen": f"{self.base_url}/api/nots/nepse-data/market-open",
            "company_list_url": f"{self.base_url}/api/nots/company/list",
            ###graph data api (these requires post request) ####
            "nepse_index_daily_graph": f"{self.base_url}/api/nots/graph/index/58",
            "sensitive_index_daily_graph": f"{self.base_url}/api/nots/graph/index/57",
            "float_index_daily_graph": f"{self.base_url}/api/nots/graph/index/62",
            "sensitive_float_index_daily_graph": f"{self.base_url}/api/nots/graph/index/63",
            ##sub index graph##
            "banking_sub_index_graph": f"{self.base_url}/api/nots/graph/index/51",
            "development_bank_sub_index_graph": f"{self.base_url}/api/nots/graph/index/55",
            "finance_sub_index_graph": f"{self.base_url}/api/nots/graph/index/60",
            "hotel_tourism_sub_index_graph": f"{self.base_url}/api/nots/graph/index/52",
            "hydro_sub_index_graph": f"{self.base_url}/api/nots/graph/index/54",
            "investment_sub_index_graph": f"{self.base_url}/api/nots/graph/index/67",
            "life_insurance_sub_index_graph": f"{self.base_url}/api/nots/graph/index/65",
            "manufacturing_sub_index_graph": f"{self.base_url}/api/nots/graph/index/56",
            "microfinance_sub_index_graph": f"{self.base_url}/api/nots/graph/index/64",
            "mutual_fund_sub_index_graph": f"{self.base_url}/api/nots/graph/index/66",
            "non_life_insurance_sub_index_graph": f"{self.base_url}/api/nots/graph/index/59",
            "others_sub_index_graph": f"{self.base_url}/api/nots/graph/index/53",
            "trading_sub_index_graph": f"{self.base_url}/api/nots/graph/index/61",
            ##company_graph_data (add company id after the frontslash)##
            "company_daily_graph": f"{self.base_url}/api/nots/market/graphdata/daily/",
            "company_details": f"{self.base_url}/api/nots/security/",
            "company_price_volume_history": f"{self.base_url}/api/nots/market/security/price/",
            "company_floorsheet": f"{self.base_url}/api/nots/security/floorsheet/",
            "floor_sheet": f"{self.base_url}/api/nots/nepse-data/floorsheet",
            "todays_price": f"{self.base_url}/api/nots/nepse-data/today-price?&size=20&securityId=2742&businessDate=2022-01-06",
        }

        self.api_end_point_access_token = (False, False)

        self.headers = {
            # host doesn't work with https prefix so removing it
            "Host": self.base_url.replace("https://", ""),
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": f"{self.base_url}",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "Trailers",
        }

    ###############################################PRIVATE METHODS###############################################

    def requestAPI(self, url):
        self.incrementTotalRequestCount()

        headers = self.headers
        if (
            url in self.api_end_points.values()
        ):  # this is done so that get request to api/authenticate doesnt fail, since it doesnt require authorization headers
            access_token, request_token = self.getToken()
            headers = {"Authorization": f"Salter {access_token}", **self.headers}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            self.refreshToken()
            return self.requestAPI(url)

        return response.json()

    def requestPOSTAPI(self, url):
        print("url ######: ", url)
        self.incrementTotalRequestCount()

        access_token, request_token = self.getToken()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Salter {access_token}",
            **self.headers,
        }
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(
                {
                    "id": self.getPOSTPayloadIDForNepseIndex()
                    if url == self.api_end_points["nepse_index_daily_graph"]
                    else self.getPOSTPayloadID()
                }
            ),
        )

        print("post response: ", response.text)
        if response.status_code != 200:
            # self.refreshToken()
            self.resetToken()
            return self.requestPOSTAPI(url)

        return response.json()

    # token is not unique for each url, when token is requested,
    def getToken(self):
        if self.api_end_point_access_token == (False, False):
            token_response = self.getValidToken()
            self.api_end_point_access_token = token_response

        return self.api_end_point_access_token

    def refreshToken(self):
        print("refresh token")
        access_token, refresh_token = self.api_end_point_access_token
        if (
            access_token != False
        ):  # this is done to make first request to api/authenticate pass
            data = json.dumps({"refreshToken": refresh_token})

            headers = {
                **self.headers,
                "Content-Type": "application/json",
                "Content-Length": str(len(data)),
                "Authorization": f"Salter {access_token}",
            }

            refresh_key = requests.post(self.refresh_url, headers=headers, data=data)

            if refresh_key.status_code != 200:
                self.resetToken()
            else:
                self.api_end_point_access_token = self.getValidTokenFromJSON(
                    refresh_key.json()
                )
        else:
            self.getToken()

    def resetToken(self):
        self.api_end_point_access_token = (False, False)
        self.salts = []

    #         self.api_end_point_access_token[url] = False
    def getValidTokenFromJSON(self, token_response):
        self.salts = []
        for salt_index in range(1, 6):
            val = int(token_response[f"salt{salt_index}"])
            token_response[f"salt{salt_index}"] = val
            self.salts.append(val)

        # returns access_token only, refresh token is not used right now
        return self.token_parser.parse_token_response(token_response)

    def getValidToken(self):
        self.incrementTokenRequestCount()
        token_response = self.requestAPI(url=self.token_url)
        return self.getValidTokenFromJSON(token_response)

    def incrementTokenRequestCount(self):
        self.token_request_count += 1

    def incrementTotalRequestCount(self):
        self.total_request_count += 1

    ##################method to get post payload id#################################33
    def getDummyID(self):
        return self.getMarketStatus()["id"]

    def getDummyData(self):
        return [
            147,
            117,
            239,
            143,
            157,
            312,
            161,
            612,
            512,
            804,
            411,
            527,
            170,
            511,
            421,
            667,
            764,
            621,
            301,
            106,
            133,
            793,
            411,
            511,
            312,
            423,
            344,
            346,
            653,
            758,
            342,
            222,
            236,
            811,
            711,
            611,
            122,
            447,
            128,
            199,
            183,
            135,
            489,
            703,
            800,
            745,
            152,
            863,
            134,
            211,
            142,
            564,
            375,
            793,
            212,
            153,
            138,
            153,
            648,
            611,
            151,
            649,
            318,
            143,
            117,
            756,
            119,
            141,
            717,
            113,
            112,
            146,
            162,
            660,
            693,
            261,
            362,
            354,
            251,
            641,
            157,
            178,
            631,
            192,
            734,
            445,
            192,
            883,
            187,
            122,
            591,
            731,
            852,
            384,
            565,
            596,
            451,
            772,
            624,
            691,
        ]

    def getPOSTPayloadIDForNepseIndex(self):
        print("post paylod nepse index called")
        dummy_id = self.getDummyID()
        e = self.getDummyData()[dummy_id] + dummy_id + 2 * (date.today().day)
        n = (
            e
            + self.salts[3 if e % 10 < 5 else 1] * date.today().day
            - self.salts[(3 if e % 10 < 5 else 1) - 1]
        )
        self.post_payload_id = n

        print("post payload id ", self.post_payload_id)

        return self.post_payload_id

    def getPOSTPayloadID(self):
        print("post payload for other called")
        dummy_id = self.getDummyID()
        self.post_payload_id = (
            self.getDummyData()[dummy_id] + dummy_id + 2 * (date.today().day)
        )

        return self.post_payload_id

    ###############################################PUBLIC METHODS###############################################
    def getMarketStatus(self):
        return self.requestAPI(url=self.api_end_points["nepse_isopen"])

    def getTotalRequestCount(self):
        return self.total_request_count

    def getTokenRequestCount(self):
        return self.token_request_count

    def getPriceVolume(self):
        return self.requestAPI(url=self.api_end_points["price_volume_url"])

    def getSummary(self):
        return self.requestAPI(url=self.api_end_points["summary_url"])

    def getTopTenTradeScrips(self):
        return self.requestAPI(url=self.api_end_points["top_ten_trade_url"])

    def getTopTenTransactionScrips(self):
        return self.requestAPI(url=self.api_end_points["top_ten_transaction_url"])

    def getTopTenTurnoverScrips(self):
        return self.requestAPI(url=self.api_end_points["top_ten_turnover_url"])

    def getSupplyDemand(self):
        return self.requestAPI(url=self.api_end_points["supply_demand_url"])

    def getTopGainers(self):
        return self.requestAPI(url=self.api_end_points["top_gainers_url"])

    def getTopLosers(self):
        return self.requestAPI(url=self.api_end_points["top_losers_url"])

    def isNepseOpen(self):
        return self.requestAPI(url=self.api_end_points["nepse_open_url"])

    def getNepseIndex(self):
        return self.requestAPI(url=self.api_end_points["nepse_index_url"])

    def getNepseSubIndices(self):
        return self.requestAPI(url=self.api_end_points["nepse_subindices_url"])

    def getCompanyList(self, force=False):
        if self.company_list is None or force == True:
            self.company_list = self.requestAPI(
                url=self.api_end_points["company_list_url"]
            )
        return self.company_list

    def getCompanyIDKeyMap(self):
        if self.company_symbol_id_keymap is None:
            company_list = self.getCompanyList()
            self.company_symbol_id_keymap = {
                company["symbol"]: company["id"] for company in company_list
            }
        return self.company_symbol_id_keymap

    #####api requiring post method
    def getDailyNepseIndexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points["nepse_index_daily_graph"])

    def getDailySensitiveIndexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["sensitive_index_daily_graph"]
        )

    def getDailyFloatIndexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points["float_index_daily_graph"])

    def getDailySensitiveFloatIndexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["sensitive_float_index_daily_graph"]
        )

    def getDailyBankSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points["banking_sub_index_graph"])

    def getDailyDevelopmentBankSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["development_bank_sub_index_graph"]
        )

    def getDailyFinanceSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points["finance_sub_index_graph"])

    def getDailyHotelTourismSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["hotel_tourism_sub_index_graph"]
        )

    def getDailyHydroSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points["hydro_sub_index_graph"])

    def getDailyInvestmentSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["investment_sub_index_graph"]
        )

    def getDailyLifeInsuranceSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["life_insurance_sub_index_graph"]
        )

    def getDailyManufacturingSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["manufacturing_sub_index_graph"]
        )

    def getDailyMicrofinanceSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["microfinance_sub_index_graph"]
        )

    def getDailyMutualfundSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["mutual_fund_sub_index_graph"]
        )

    def getDailyNonLifeInsuranceSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["non_life_insurance_sub_index_graph"]
        )

    def getDailyOthersSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points["others_sub_index_graph"])

    def getDailyTradingSubindexGraph(self):
        return self.requestPOSTAPI(url=self.api_end_points["trading_sub_index_graph"])

    def getDailyScripPriceGraph(self, symbol):
        # return self.getCompanyIDKeyMap()
        company_id = self.getCompanyIDKeyMap()[symbol]
        return self.requestPOSTAPI(
            url=f"{self.api_end_points['company_daily_graph']}{company_id}"
        )

    def getCompanyDetails(self, symbol):
        company_id = self.getCompanyIDKeyMap()[symbol]
        return self.requestPOSTAPI(
            url=f"{self.api_end_points['company_details']}{company_id}"
        )

    ##unfinished
    def getCompanyPriceVolumeHistory(self, symbol):
        company_id = self.getCompanyIDKeyMap()[symbol]
        return self.requestPOSTAPI(
            url=f"{self.api_end_points['company_price_volume_history']}{company_id}"
        )

    def getFloorSheet(self, show_progress=False):
        url = f"{self.api_end_points['floor_sheet']}?=&size={self.floor_sheet_size}&sort=contractId,asc"
        sheet = self.requestPOSTAPI(url=url)
        floor_sheets = sheet["floorsheets"]["content"]
        page_range = range(1, sheet["floorsheets"]["totalPages"] + 1)
        pages = tqdm.tqdm(page_range) if show_progress else page_range
        for page in pages:
            next_sheet = self.requestPOSTAPI(url=f"{url}&page={page}")
            next_floor_sheet = next_sheet["floorsheets"]["content"]
            floor_sheets.extend(next_floor_sheet)
        return floor_sheets

    def getFloorSheetOf(self, symbol):
        company_id = self.getCompanyIDKeyMap()[symbol]
        url = f"{self.api_end_points['company_floorsheet']}{company_id}?=&size={self.floor_sheet_size}&sort=contractId,asc&businessDate={date.isoformat(date.today())}"
        sheet = self.requestPOSTAPI(url=url)
        floor_sheets = sheet["floorsheets"]["content"]
        for page in range(1, sheet["floorsheets"]["totalPages"] + 1):
            next_sheet = self.requestPOSTAPI(url=f"{url}&page={page}")
            next_floor_sheet = next_sheet["floorsheets"]["content"]
            floor_sheets.extend(next_floor_sheet)
        return floor_sheets


def test():
    a = Nepse()
    # a.getFloorSheet(show_progress=True)
    # print(a.getFloorSheetOf(symbol="MLBBL"))
    # print(a.getValidToken())
    # print(a.getDailyNepseIndexGraph())
    # print(a.getPriceVolume())
    print(a.getMarketStatus())


if __name__ == "__main__":
    test()
