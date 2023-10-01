from TokenUtils import TokenManager
from datetime import date
import json
import requests


class Nepse:
    def __init__(self):
        # internal flag to set tls verification true or false during http request
        self._tls_verify = True

        self.token_manager = TokenManager()

        self.company_symbol_id_keymap = None
        self.company_list = None

        self.floor_sheet_size = 500

        self.base_url = "https://www.nepalstock.com.np"
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
        headers = self.headers
        access_token = self.token_manager.getAccessToken()

        headers = {
            "Authorization": f"Salter {access_token}",
            "Content-Type": "application/json",
            **self.headers,
        }
        response = requests.get(url, headers=headers, verify=self._tls_verify)

        return response.json()

    def requestPOSTAPI(self, url, payload_generator):
        # print("url ", url)
        access_token = self.token_manager.getAccessToken()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Salter {access_token}",
            **self.headers,
        }
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps({"id": payload_generator()}),
            verify=self._tls_verify,
        )
        return response.json()

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

    def getPOSTPayloadID(self):
        dummy_id = self.getDummyID()
        e = self.getDummyData()[dummy_id] + dummy_id + 2 * (date.today().day)
        post_payload_id = (
            e
            + self.token_manager.salts[3 if e % 10 < 5 else 1] * date.today().day
            - self.token_manager.salts[(3 if e % 10 < 5 else 1) - 1]
        )
        return post_payload_id

    def getPOSTPayloadIDForFloorSheet(self):
        dummy_id = self.getDummyID()
        e = self.getDummyData()[dummy_id] + dummy_id + 2 * (date.today().day)
        post_payload_id = (
            e
            + self.token_manager.salts[1 if e % 10 < 4 else 3] * date.today().day
            - self.token_manager.salts[(1 if e % 10 < 4 else 3) - 1]
        )
        return post_payload_id

    ###############################################PUBLIC METHODS###############################################
    def setTLSVerification(self, flag):
        self._tls_verify = flag

    def getMarketStatus(self):
        return self.requestAPI(url=self.api_end_points["nepse_isopen"])

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

    def getCompanyList(self):
        self.company_list = self.requestAPI(url=self.api_end_points["company_list_url"])
        return self.company_list

    def getCompanyIDKeyMap(self, force_update=False):
        if self.company_symbol_id_keymap is None or force_update:
            company_list = self.getCompanyList()
            self.company_symbol_id_keymap = {
                company["symbol"]: company["id"] for company in company_list
            }
        return self.company_symbol_id_keymap

    #####api requiring post method
    def getDailyNepseIndexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["nepse_index_daily_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailySensitiveIndexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["sensitive_index_daily_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyFloatIndexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["float_index_daily_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailySensitiveFloatIndexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["sensitive_float_index_daily_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyBankSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["banking_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyDevelopmentBankSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["development_bank_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyFinanceSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["finance_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyHotelTourismSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["hotel_tourism_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyHydroSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["hydro_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyInvestmentSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["investment_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyLifeInsuranceSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["life_insurance_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyManufacturingSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["manufacturing_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyMicrofinanceSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["microfinance_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyMutualfundSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["mutual_fund_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyNonLifeInsuranceSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["non_life_insurance_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyOthersSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["others_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyTradingSubindexGraph(self):
        return self.requestPOSTAPI(
            url=self.api_end_points["trading_sub_index_graph"],
            payload_generator=self.getPOSTPayloadID,
        )

    def getDailyScripPriceGraph(self, symbol):
        # return self.getCompanyIDKeyMap()
        company_id = self.getCompanyIDKeyMap()[symbol]
        return self.requestPOSTAPI(
            url=f"{self.api_end_points['company_daily_graph']}{company_id}",
            payload_generator=self.getPOSTPayloadID,
        )

    def getCompanyDetails(self, symbol):
        company_id = self.getCompanyIDKeyMap()[symbol]
        return self.requestPOSTAPI(
            url=f"{self.api_end_points['company_details']}{company_id}",
            payload_generator=self.getPOSTPayloadID,
        )

    ##unfinished
    def getCompanyPriceVolumeHistory(self, symbol):
        company_id = self.getCompanyIDKeyMap()[symbol]
        return self.requestPOSTAPI(
            url=f"{self.api_end_points['company_price_volume_history']}{company_id}",
            payload_generator=self.getPOSTPayloadID,
        )

    def getFloorSheet(self):
        url = f"{self.api_end_points['floor_sheet']}?&size={self.floor_sheet_size}&sort=contractId,desc"
        sheet = self.requestPOSTAPI(
            url=url, payload_generator=self.getPOSTPayloadIDForFloorSheet
        )
        floor_sheets = sheet["floorsheets"]["content"]
        page_range = range(1, sheet["floorsheets"]["totalPages"] + 1)
        for page in page_range:
            next_sheet = self.requestPOSTAPI(
                url=f"{url}&page={page}",
                payload_generator=self.getPOSTPayloadIDForFloorSheet,
            )
            next_floor_sheet = next_sheet["floorsheets"]["content"]
            floor_sheets.extend(next_floor_sheet)
        return floor_sheets

    def getFloorSheetOf(self, symbol):
        company_id = self.getCompanyIDKeyMap()[symbol]
        url = f"{self.api_end_points['company_floorsheet']}{company_id}?&businessDate=2023-09-27&size={self.floor_sheet_size}&sort=contractid,desc"
        sheet = self.requestPOSTAPI(
            url=url, payload_generator=self.getPOSTPayloadIDForFloorSheet
        )
        floor_sheets = sheet["floorsheets"]["content"]
        for page in range(1, sheet["floorsheets"]["totalPages"] + 1):
            next_sheet = self.requestPOSTAPI(
                url=f"{url}&page={page}",
                payload_generator=self.getPOSTPayloadIDForFloorSheet,
            )
            next_floor_sheet = next_sheet["floorsheets"]["content"]
            floor_sheets.extend(next_floor_sheet)
        return floor_sheets
