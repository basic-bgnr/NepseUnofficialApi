import requests
from collections import defaultdict
from json import JSONDecodeError
import json

class TokenParser():
    def __init__(self):
        ###############################################MAGIC ARRAY###############################################
        #FOR details check http://newweb.nepalstock.com/assets/prod/css.wasm
        #decompiling the wasm gives access to the following magic array and (rdx, cdx) function
        self.data_segment_data_0 = [
                                      0x09, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 
                                      0x02, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 
                                      0x07, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 
                                      0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
                                      0x02, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
                                      0x09, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x06, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 
                                      0x02, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 
                                      0x09, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 
                                      0x03, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 
                                      0x04, 
                                    ]
        
    def rdx(self, w2c_p0, w2c_p1, w2c_p2, w2c_p3, w2c_p4):

        w2c_i0 = w2c_p1
        w2c_i1 = 100
        w2c_i0 = w2c_i0 // w2c_i1
        w2c_i1 = 10
        w2c_i0 = w2c_i0 % w2c_i1
        w2c_i1 = w2c_p1
        w2c_i2 = 10
        w2c_i1 = w2c_i1 // w2c_i2
        w2c_p0 = w2c_i1
        w2c_i2 = 10
        w2c_i1 = w2c_i1 % w2c_i2
        w2c_i0 += w2c_i1
        w2c_p2 = w2c_i0
        w2c_i1 = w2c_p2
        w2c_i2 = w2c_p1
        w2c_i3 = w2c_p0
        w2c_i4 = 10
        w2c_i3 *= w2c_i4
        w2c_i2 -= w2c_i3
        w2c_i1 += w2c_i2
        w2c_i2 = 2
        w2c_i1 <<= (w2c_i2 & 31)

        w2c_i1 = self.data_segment_data_0[w2c_i1]
        w2c_i0 += w2c_i1
        w2c_i1 = 22
        w2c_i0 += w2c_i1
        return w2c_i0


    def cdx(self, w2c_p0, w2c_p1, w2c_p2, w2c_p3, w2c_p4):
        w2c_i0 = w2c_p1
        w2c_i1 = 10
        w2c_i0 = w2c_i0 // w2c_i1
        w2c_p0 = w2c_i0
        w2c_i1 = 10
        w2c_i0 = w2c_i0 % w2c_i1
        w2c_i1 = w2c_p1
        w2c_i2 = w2c_p0
        w2c_i3 = 10
        w2c_i2 *= w2c_i3
        w2c_i1 -= w2c_i2
        w2c_i0 += w2c_i1
        w2c_i1 = w2c_p1
        w2c_i2 = 100
        w2c_i1 = w2c_i1 // w2c_i2
        w2c_i2 = 10
        w2c_i1 = w2c_i1 % w2c_i2
        w2c_i0 += w2c_i1
        w2c_i1 = 2
        w2c_i0 <<= (w2c_i1 & 31)

        w2c_i0 = self.data_segment_data_0[w2c_i0]
        w2c_i1 = 22
        w2c_i0 += w2c_i1

        return w2c_i0

    def parse_token_response(self, token_response):
        n = self.cdx(token_response['salt1'], token_response['salt2'], token_response['salt3'], token_response['salt4'], token_response['salt5']);
        l = self.rdx(token_response['salt1'], token_response['salt2'], token_response['salt4'], token_response['salt3'], token_response['salt5']);
        
        i = self.cdx(token_response['salt2'], token_response['salt1'], token_response['salt3'], token_response['salt5'], token_response['salt4']);
        r = self.rdx(token_response['salt2'], token_response['salt1'], token_response['salt3'], token_response['salt4'], token_response['salt5']);

        access_token  = token_response['accessToken']
        refresh_token = token_response['refreshToken']
        
        parsed_access_token  = access_token[0:n] + access_token[n + 1: l] + access_token[l + 1:]
        parsed_refresh_token = refresh_token[0:i] + refresh_token[i + 1: r] + refresh_token[r + 1:]
    
        #returns both access_token and refresh_token, i don't know what's the purpose of refresh token.
        #Right now new access_token can be used for every new api request
        return (parsed_access_token, parsed_refresh_token)

class Nepse:
    def __init__(self):
        self.token_request_count = 0 
        self.total_request_count = 0
        
        self.token_parser     = TokenParser()

        self.base_url             = "https://www.nepalstock.com.np"
        
        self.token_url            = f"{self.base_url}/api/authenticate/prove"
        self.refresh_url          = f"{self.base_url}/api/authenticate/refresh-token"
        
        self.api_end_points = {
                                "price_volume_url"     : f"{self.base_url}/api/nots/securityDailyTradeStat/58",
                                "summary_url"          : f"{self.base_url}/api/nots/market-summary/",
                                "top_ten_scrips_url"   : f"{self.base_url}/api/nots/top-ten/trade-qty",
                                "supply_demand_url"    : f"{self.base_url}/api/nots/nepse-data/supplydemand",
                                "turnover_url"         : f"{self.base_url}/api/nots/top-ten/turnover",
                                "top_gainers_url"      : f"{self.base_url}/api/nots/top-ten/top-gainer",
                                "top_losers_url"       : f"{self.base_url}/api/nots/top-ten/top-loser",
                                "nepse_open_url"       : f"{self.base_url}/api/nots/nepse-data/market-open",
                                "nepse_index_url"      : f"{self.base_url}/api/nots/nepse-index",
                                "nepse_subindices_url" : f"{self.base_url}/api/nots",
                              }
        
        self.api_end_point_access_token = defaultdict(lambda : False)
        
        self.headers= {
                            'Host': 'newweb.nepalstock.com',
                            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
                            'Accept': 'application/json, text/plain, */*',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Referer': 'https://newweb.nepalstock.com/',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'TE': 'Trailers',
                        }
    ###############################################PRIVATE METHODS###############################################
    
    def requestAPI(self, url):
        self.incrementTotalRequestCount()
        
        headers = self.headers
        if url in self.api_end_points.values():
            access_token, request_token = self.getTokenForURL(url)
            headers = {'Authorization': f'Salter {access_token}', **self.headers}
        
        
        response = requests.get(url, headers=headers)
        if (response.status_code != 200):
            self.refreshTokenForURL(url)
            return self.requestAPI(url) 
        
        return response.json()
            
    
    #token is unique for each url, when token is requested, the access token received when first used for accessing a url can be 
    #used to send multiple request for the same url without requesting new access token.
    def getTokenForURL(self, url):
        if self.api_end_point_access_token[url] is False:
            token_response = self.getValidToken()
            self.api_end_point_access_token[url] = token_response
        
        return self.api_end_point_access_token[url]
    
    def refreshTokenForURL(self, url):
        print(f'token refresh: {url}')
        
        access_token, refresh_token = self.api_end_point_access_token[url]

        data=json.dumps({'refreshToken':refresh_token})

        headers= {**self.headers, 
                    "Content-Type": "application/json",
                    "Content-Length": str(len(data)),
                    "Authorization": f"Salter {access_token}"
                 }
        
        refresh_key = requests.post(self.refresh_url, 
                                    headers=headers, 
                                    data=data)
        
        if refresh_key.status_code != 200:
            self.resetTokenForURL(url)
        else:
            self.api_end_point_access_token[url] = self.getValidTokenFromJSON( refresh_key.json() )
        
    def resetTokenForURL(self, url):
        self.api_end_point_access_token[url] = False
        
#         self.api_end_point_access_token[url] = False
    def getValidTokenFromJSON(self, token_response):
        for salt_index in range(1, 6):
            token_response[f'salt{salt_index}'] = int(token_response[f'salt{salt_index}'])
        
        #returns access_token only, refresh token is not used right now
        return self.token_parser.parse_token_response(token_response)
        
    def getValidToken(self):
        self.incrementTokenRequestCount()
        
        token_response = self.requestAPI(url=self.token_url)        
        return self.getValidTokenFromJSON(token_response)
    
    def incrementTokenRequestCount(self):
        self.token_request_count += 1
        
    def incrementTotalRequestCount(self):
        self.total_request_count += 1
    
    ###############################################PUBLIC METHODS###############################################
    def getTotalRequestCount(self):
        return self.total_request_count
    
    def getTokenRequestCount(self):
        return self.token_request_count
        
    def getPriceVolume(self):
        return self.requestAPI(url=self.api_end_points['price_volume_url'])
    
    def getSummary(self):
        return self.requestAPI(url=self.api_end_points['summary_url'])
    
    def getTopTenScrips(self):
        return self.requestAPI(url=self.api_end_points['top_ten_scrips_url'])
    
    def getSupplyDemand(self):
        return self.requestAPI(url=self.api_end_points['supply_demand_url'])
    
    def getTopGainers(self):
        return self.requestAPI(url=self.api_end_points['top_gainers_url'])
    
    def getTopLosers(self):
        return self.requestAPI(url=self.api_end_points['top_losers_url'])
    
    def isNepseOpen(self):
        return self.requestAPI(url=self.api_end_points['nepse_open_url'])
    
    def getNepseIndex(self):
        return self.requestAPI(url=self.api_end_points['nepse_index_url'])
    
    def getNepseSubIndices(self):
        return self.requestAPI(url=self.api_end_points['nepse_subindices_url'])