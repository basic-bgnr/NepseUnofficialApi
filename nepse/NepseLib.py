from nepse.TokenUtils import TokenManager, AsyncTokenManager
from nepse.DummyIDUtils import DummyIDManager, AsyncDummyIDManager

from datetime import date, datetime, timedelta
from collections import defaultdict

from tqdm import tqdm
import asyncio
import json
import httpx
import pathlib


class _Nepse:
    def __init__(self, token_manager, dummy_id_manager):

        self.token_manager = token_manager(self)

        self.dummy_id_manager = dummy_id_manager(
            market_status_function=self.getMarketStatus,
            date_function=datetime.now,
        )

        # list of all company that were listed in nepse (including delisted but doesn't include promoter shares)
        self.company_symbol_id_keymap = None
        # list of all valid company that are not delisted (includes promoter share)
        self.security_symbol_id_keymap = None

        self.company_list = None
        self.security_list = None

        self.sector_scrips = None

        self.floor_sheet_size = 500

        self.base_url = "https://www.nepalstock.com"

        self.load_json_api_end_points()
        self.load_json_dummy_data()
        self.load_json_header()

    ###############################################PRIVATE METHODS###############################################
    def getDummyID(self):
        return self.dummy_id_manager.getDummyID()

    def load_json_header(self):
        json_file_path = f"{pathlib.Path(__file__).parent}/data/HEADERS.json"
        with open(json_file_path, "r") as json_file:
            self.headers = json.load(json_file)
            self.headers["Host"] = self.base_url.replace("https://", "")
            self.headers["Referer"] = self.base_url.replace("https://", "")

    def load_json_api_end_points(self):
        json_file_path = f"{pathlib.Path(__file__).parent}/data/API_ENDPOINTS.json"
        with open(json_file_path, "r") as json_file:
            self.api_end_points = json.load(json_file)

    def get_full_url(self, api_url):
        return f"{self.base_url}{api_url}"

    def load_json_dummy_data(self):
        json_file_path = f"{pathlib.Path(__file__).parent}/data/DUMMY_DATA.json"
        with open(json_file_path, "r") as json_file:
            self.dummy_data = json.load(json_file)

    def getDummyData(self):
        return self.dummy_data

    def init_client(self, tls_verify):
        pass

    def requestGETAPI(url):
        pass

    def requestPOSTAPI(url, payload_generator):
        pass

    ###############################################PUBLIC METHODS###############################################
    def setTLSVerification(self, flag):
        self._tls_verify = flag
        self.init_client(tls_verify=flag)

    #####api requiring get method
    def getMarketStatus(self):
        return self.requestGETAPI(url=self.api_end_points["nepse_open_url"])

    def getPriceVolume(self):
        return self.requestGETAPI(url=self.api_end_points["price_volume_url"])

    def getSummary(self):
        return self.requestGETAPI(url=self.api_end_points["summary_url"])

    def getTopTenTradeScrips(self):
        return self.requestGETAPI(url=self.api_end_points["top_ten_trade_url"])

    def getTopTenTransactionScrips(self):
        return self.requestGETAPI(url=self.api_end_points["top_ten_transaction_url"])

    def getTopTenTurnoverScrips(self):
        return self.requestGETAPI(url=self.api_end_points["top_ten_turnover_url"])

    def getSupplyDemand(self):
        return self.requestGETAPI(url=self.api_end_points["supply_demand_url"])

    def getTopGainers(self):
        return self.requestGETAPI(url=self.api_end_points["top_gainers_url"])

    def getTopLosers(self):
        return self.requestGETAPI(url=self.api_end_points["top_losers_url"])

    def isNepseOpen(self):
        return self.requestGETAPI(url=self.api_end_points["nepse_open_url"])

    def getNepseIndex(self):
        return self.requestGETAPI(url=self.api_end_points["nepse_index_url"])

    def getNepseSubIndices(self):
        return self.requestGETAPI(url=self.api_end_points["nepse_subindices_url"])

    #####api requiring post method
    def getPriceVolumeHistory(self, business_date=None):
        url = f"{self.api_end_points['todays_price']}?&size=500&businessDate={business_date}"
        return self.requestPOSTAPI(
            url=url, payload_generator=self.getPOSTPayloadIDForFloorSheet
        )

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


class AsyncNepse(_Nepse):
    def __init__(self):
        super().__init__(AsyncTokenManager, AsyncDummyIDManager)
        # internal flag to set tls verification true or false during http request
        self.init_client(tls_verify=True)

    ###############################################PRIVATE METHODS###############################################
    async def getPOSTPayloadIDForScrips(self):
        dummy_id = await self.getDummyID()
        e = self.getDummyData()[dummy_id] + dummy_id + 2 * (date.today().day)
        return e

    async def getPOSTPayloadID(self):
        e = await self.getPOSTPayloadIDForScrips()
        # we need to await before update is completed
        await self.token_manager.update_completed.wait()
        post_payload_id = (
            e
            + self.token_manager.salts[3 if e % 10 < 5 else 1] * date.today().day
            - self.token_manager.salts[(3 if e % 10 < 5 else 1) - 1]
        )
        return post_payload_id

    async def getPOSTPayloadIDForFloorSheet(self):
        e = await self.getPOSTPayloadIDForScrips()

        # we need to await before update is completed
        await self.token_manager.update_completed.wait()

        post_payload_id = (
            e
            + self.token_manager.salts[1 if e % 10 < 4 else 3] * date.today().day
            - self.token_manager.salts[(1 if e % 10 < 4 else 3) - 1]
        )
        return post_payload_id

    async def getAuthorizationHeaders(self):
        headers = self.headers
        access_token = await self.token_manager.getAccessToken()

        headers = {
            "Authorization": f"Salter {access_token}",
            "Content-Type": "application/json",
            **self.headers,
        }

        return headers

    def init_client(self, tls_verify):
        # limits prevent rate limit imposed by nepse
        # (setting connection > 2, raises protocol error, so the following value is used as default)
        limits = httpx.Limits(max_keepalive_connections=2, max_connections=2)
        self.client = httpx.AsyncClient(
            verify=tls_verify, limits=limits, http2=False, timeout=100
        )

    async def requestGETAPI(self, url, include_authorization_headers=True):
        try:
            response = await self.client.get(
                self.get_full_url(api_url=url),
                headers=(
                    await self.getAuthorizationHeaders()
                    if include_authorization_headers
                    else self.headers
                ),
            )
            return response.json() if response.text else {}
        except httpx.RemoteProtocolError:
            return await self.requestGETAPI(url, include_authorization_headers)

    async def requestPOSTAPI(self, url, payload_generator):
        try:
            response = await self.client.post(
                self.get_full_url(api_url=url),
                headers=await self.getAuthorizationHeaders(),
                data=json.dumps({"id": await payload_generator()}),
            )
            return response.json() if response.text else {}
        except httpx.RemoteProtocolError:
            return await self.requestPOSTAPI(url, payload_generator)

    ###############################################PUBLIC METHODS###############################################
    # api requiring get method
    async def getCompanyList(self):
        self.company_list = await self.requestGETAPI(
            url=self.api_end_points["company_list_url"]
        )
        # return a copy of self.company_list so than changes after return are not perisistent
        return list(self.company_list)

    async def getSecurityList(self):
        self.security_list = await self.requestGETAPI(
            url=self.api_end_points["security_list_url"]
        )
        # return a copy of self.company_list so than changes after return are not perisistent
        return list(self.security_list)

    async def getSectorScrips(self):
        if self.sector_scrips is None:
            company_info_dict = {
                company_info["symbol"]: company_info
                for company_info in (await self.getCompanyList())
            }
            sector_scrips = defaultdict(list)

            for security_info in await self.getSecurityList():
                symbol = security_info["symbol"]
                if company_info_dict.get(symbol):
                    company_info = company_info_dict[symbol]
                    sector_name = company_info["sectorName"]
                    sector_scrips[sector_name].append(symbol)
                else:
                    sector_scrips["Promoter Share"].append(symbol)

            self.sector_scrips = dict(sector_scrips)
        # return a copy of self.sector_scrips so than changes after return are not perisistent
        return dict(self.sector_scrips)

    async def getCompanyIDKeyMap(self, force_update=False):
        if self.company_symbol_id_keymap is None or force_update:
            company_list = await self.getCompanyList()
            self.company_symbol_id_keymap = {
                company["symbol"]: company["id"] for company in company_list
            }
        return self.company_symbol_id_keymap

    async def getSecurityIDKeyMap(self, force_update=False):
        if self.security_symbol_id_keymap is None or force_update:
            security_list = await self.getSecurityList()
            self.security_symbol_id_keymap = {
                security["symbol"]: security["id"] for security in security_list
            }
        return self.security_symbol_id_keymap

    async def getCompanyPriceVolumeHistory(
        self, symbol, start_date=None, end_date=None
    ):
        end_date = end_date if end_date else date.today()
        start_date = start_date if start_date else (end_date - timedelta(days=365))
        symbol = symbol.upper()
        company_id = (await self.getSecurityIDKeyMap())[symbol]
        url = f"{self.api_end_points['company_price_volume_history']}{company_id}?&size=500&startDate={start_date}&endDate={end_date}"
        return (await self.requestGETAPI(url=url))["content"]

    # api requiring post method
    async def getDailyScripPriceGraph(self, symbol):
        symbol = symbol.upper()
        company_id = (await self.getSecurityIDKeyMap())[symbol]
        return await self.requestPOSTAPI(
            url=f"{self.api_end_points['company_daily_graph']}{company_id}",
            payload_generator=self.getPOSTPayloadIDForScrips,
        )

    async def getCompanyDetails(self, symbol):
        symbol = symbol.upper()
        company_id = (await self.getSecurityIDKeyMap())[symbol]
        return await self.requestPOSTAPI(
            url=f"{self.api_end_points['company_details']}{company_id}",
            payload_generator=self.getPOSTPayloadIDForScrips,
        )

    async def getFloorSheet(self, show_progress=False):

        url = f"{self.api_end_points['floor_sheet']}?&size={self.floor_sheet_size}&sort=contractId,desc"
        sheet = await self.requestPOSTAPI(
            url=url, payload_generator=self.getPOSTPayloadIDForFloorSheet
        )
        floor_sheets = sheet["floorsheets"]["content"]
        max_page = sheet["floorsheets"]["totalPages"]

        page_range = range(1, max_page)

        if show_progress:
            progress_counter = (_ for _ in tqdm(page_range))
            next(progress_counter)  # first page has already been downloaded
        else:
            progress_counter = None

        awaitables = map(
            lambda page_number: self._getFloorSheetPageNumber(
                url,
                page_number,
                progress_counter,
            ),
            page_range,
        )
        floor_sheets = [floor_sheets] + await asyncio.gather(*awaitables)
        return [row for array in floor_sheets for row in array]

    async def _getFloorSheetPageNumber(self, url, page_number, progress_counter=None):
        current_sheet = await self.requestPOSTAPI(
            url=f"{url}&page={page_number}",
            payload_generator=self.getPOSTPayloadIDForFloorSheet,
        )
        current_sheet_content = current_sheet["floorsheets"]["content"]
        if progress_counter:
            try:
                next(progress_counter)
            except StopIteration:
                pass
        return current_sheet_content

    async def getFloorSheetOf(self, symbol, business_date=None):
        # business date can be YYYY-mm-dd string or date object
        symbol = symbol.upper()
        company_id = (await self.getSecurityIDKeyMap())[symbol]
        business_date = (
            date.fromisoformat(f"{business_date}") if business_date else date.today()
        )
        url = f"{self.api_end_points['company_floorsheet']}{company_id}?&businessDate={business_date}&size={self.floor_sheet_size}&sort=contractid,desc"
        sheet = await self.requestPOSTAPI(
            url=url, payload_generator=self.getPOSTPayloadIDForFloorSheet
        )
        if sheet:  # sheet might be empty
            floor_sheets = sheet["floorsheets"]["content"]
            for page in range(1, sheet["floorsheets"]["totalPages"]):
                next_sheet = await self.requestPOSTAPI(
                    url=f"{url}&page={page}",
                    payload_generator=self.getPOSTPayloadIDForFloorSheet,
                )
                next_floor_sheet = next_sheet["floorsheets"]["content"]
                floor_sheets.extend(next_floor_sheet)
        else:
            floor_sheets = []
        return floor_sheets


class Nepse(_Nepse):
    def __init__(self):
        super().__init__(TokenManager, DummyIDManager)
        # internal flag to set tls verification true or false during http request
        self.init_client(tls_verify=True)

    ###############################################PRIVATE METHODS###############################################
    def getPOSTPayloadIDForScrips(self):
        dummy_id = self.getDummyID()
        e = self.getDummyData()[dummy_id] + dummy_id + 2 * (date.today().day)
        return e

    def getPOSTPayloadID(self):
        e = self.getPOSTPayloadIDForScrips()
        post_payload_id = (
            e
            + self.token_manager.salts[3 if e % 10 < 5 else 1] * date.today().day
            - self.token_manager.salts[(3 if e % 10 < 5 else 1) - 1]
        )
        return post_payload_id

    def getPOSTPayloadIDForFloorSheet(self):
        e = self.getPOSTPayloadIDForScrips()
        post_payload_id = (
            e
            + self.token_manager.salts[1 if e % 10 < 4 else 3] * date.today().day
            - self.token_manager.salts[(1 if e % 10 < 4 else 3) - 1]
        )
        return post_payload_id

    def getAuthorizationHeaders(self):
        headers = self.headers
        access_token = self.token_manager.getAccessToken()

        headers = {
            "Authorization": f"Salter {access_token}",
            "Content-Type": "application/json",
            **self.headers,
        }

        return headers

    def init_client(self, tls_verify):
        # limits prevent rate limit imposed by nepse
        limits = httpx.Limits(max_keepalive_connections=0, max_connections=1)
        self.client = httpx.Client(
            verify=tls_verify, limits=limits, http2=True, timeout=100
        )

    def requestGETAPI(self, url, include_authorization_headers=True):
        try:
            response = self.client.get(
                self.get_full_url(api_url=url),
                headers=(
                    self.getAuthorizationHeaders()
                    if include_authorization_headers
                    else self.headers
                ),
            )
            return response.json() if response.text else {}
        except httpx.RemoteProtocolError:
            return self.requestGETAPI(url, include_authorization_headers)

    def requestPOSTAPI(self, url, payload_generator):
        try:
            response = self.client.post(
                self.get_full_url(api_url=url),
                headers=self.getAuthorizationHeaders(),
                data=json.dumps({"id": payload_generator()}),
            )
            return response.json() if response.text else {}
        except httpx.RemoteProtocolError:
            return self.requestPOSTAPI(url, payload_generator)

    ###############################################PUBLIC METHODS###############################################
    #####api requiring get method
    def getCompanyList(self):
        self.company_list = self.requestGETAPI(
            url=self.api_end_points["company_list_url"]
        )
        # return a copy of self.company_list so than changes after return are not perisistent
        return list(self.company_list)

    def getSecurityList(self):
        self.security_list = self.requestGETAPI(
            url=self.api_end_points["security_list_url"]
        )
        # return a copy of self.company_list so than changes after return are not perisistent
        return list(self.security_list)

    def getSectorScrips(self):
        if self.sector_scrips is None:
            company_info_dict = {
                company_info["symbol"]: company_info
                for company_info in self.getCompanyList()
            }
            sector_scrips = defaultdict(list)

            for security_info in self.getSecurityList():
                symbol = security_info["symbol"]
                if company_info_dict.get(symbol):
                    company_info = company_info_dict[symbol]
                    sector_name = company_info["sectorName"]
                    sector_scrips[sector_name].append(symbol)
                else:
                    sector_scrips["Promoter Share"].append(symbol)

            self.sector_scrips = dict(sector_scrips)
        # return a copy of self.sector_scrips so than changes after return are not perisistent
        return dict(self.sector_scrips)

    def getCompanyIDKeyMap(self, force_update=False):
        if self.company_symbol_id_keymap is None or force_update:
            company_list = self.getCompanyList()
            self.company_symbol_id_keymap = {
                company["symbol"]: company["id"] for company in company_list
            }
        return self.company_symbol_id_keymap

    def getSecurityIDKeyMap(self, force_update=False):
        if self.security_symbol_id_keymap is None or force_update:
            security_list = self.getSecurityList()
            self.security_symbol_id_keymap = {
                security["symbol"]: security["id"] for security in security_list
            }
        return self.security_symbol_id_keymap

    def getCompanyPriceVolumeHistory(self, symbol, start_date=None, end_date=None):
        end_date = end_date if end_date else date.today()
        start_date = start_date if start_date else (end_date - timedelta(days=365))
        symbol = symbol.upper()
        company_id = self.getSecurityIDKeyMap()[symbol]
        url = f"{self.api_end_points['company_price_volume_history']}{company_id}?&size=500&startDate={start_date}&endDate={end_date}"
        return self.requestGETAPI(url=url)

    #####api requiring post method
    def getDailyScripPriceGraph(self, symbol):
        symbol = symbol.upper()
        company_id = self.getSecurityIDKeyMap()[symbol]
        return self.requestPOSTAPI(
            url=f"{self.api_end_points['company_daily_graph']}{company_id}",
            payload_generator=self.getPOSTPayloadIDForScrips,
        )

    def getCompanyDetails(self, symbol):
        symbol = symbol.upper()
        company_id = self.getSecurityIDKeyMap()[symbol]
        return self.requestPOSTAPI(
            url=f"{self.api_end_points['company_details']}{company_id}",
            payload_generator=self.getPOSTPayloadIDForScrips,
        )

    def getFloorSheet(self, show_progress=False):
        url = f"{self.api_end_points['floor_sheet']}?&size={self.floor_sheet_size}&sort=contractId,desc"
        sheet = self.requestPOSTAPI(
            url=url, payload_generator=self.getPOSTPayloadIDForFloorSheet
        )
        floor_sheets = sheet["floorsheets"]["content"]
        max_page = sheet["floorsheets"]["totalPages"]
        page_range = tqdm(range(1, max_page)) if show_progress else range(1, max_page)
        for page_number in page_range:
            current_sheet = self.requestPOSTAPI(
                url=f"{url}&page={page_number}",
                payload_generator=self.getPOSTPayloadIDForFloorSheet,
            )
            current_sheet_content = current_sheet["floorsheets"]["content"]
            floor_sheets.extend(current_sheet_content)
        return floor_sheets

    def getFloorSheetOf(self, symbol, business_date=None):
        # business date can be YYYY-mm-dd string or date object
        symbol = symbol.upper()
        company_id = self.getSecurityIDKeyMap()[symbol]
        business_date = (
            date.fromisoformat(f"{business_date}") if business_date else date.today()
        )
        url = f"{self.api_end_points['company_floorsheet']}{company_id}?&businessDate={business_date}&size={self.floor_sheet_size}&sort=contractid,desc"
        sheet = self.requestPOSTAPI(
            url=url, payload_generator=self.getPOSTPayloadIDForFloorSheet
        )
        if sheet:  # sheet might be empty
            floor_sheets = sheet["floorsheets"]["content"]
            for page in range(1, sheet["floorsheets"]["totalPages"]):
                next_sheet = self.requestPOSTAPI(
                    url=f"{url}&page={page}",
                    payload_generator=self.getPOSTPayloadIDForFloorSheet,
                )
                next_floor_sheet = next_sheet["floorsheets"]["content"]
                floor_sheets.extend(next_floor_sheet)
        else:
            floor_sheets = []
        return floor_sheets
