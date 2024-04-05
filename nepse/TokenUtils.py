import pywasm
import requests
from datetime import datetime
import time
import pathlib


class TokenManager:
    def __init__(self):
        self.MAX_UPDATE_PERIOD = 45

        self.token_parser = TokenParser()

        self.base_url = "https://www.nepalstock.com.np"
        self.token_url = f"{self.base_url}/api/authenticate/prove"
        self.refresh_url = f"{self.base_url}/api/authenticate/refresh-token"

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

        self.access_token = None
        self.refresh_token = None
        self.token_time_stamp = None
        self.salts = None

    def isTokenValid(self):
        return (
            (int(time.time()) - self.token_time_stamp) < self.MAX_UPDATE_PERIOD
            if self.token_time_stamp
            else False
        )

    def getAccessToken(self):
        return (
            self.access_token
            if self.isTokenValid()
            else self.update() or self.access_token
        )

    def getRefreshToken(self):
        return (
            self.refresh_token
            if self.isTokenValid()
            else self.update() or self.refresh_token
        )

    def update(self):
        self._setToken()

    def __repr__(self):
        return (
            f"Access Token: {self.access_token}\nRefresh Token: {self.refresh_token}\nSalts: {self.salts}\nTimeStamp: {datetime.fromtimestamp(self.token_time_stamp).strftime('%Y-%m-%d %H:%M:%S')}"
            if self.access_token is not None
            else "Token Manager Not Initialized"
        )

    def _setToken(self):
        json_response = self._getTokenHttpRequest()

        (
            self.access_token,
            self.refresh_token,
            self.token_time_stamp,
            self.salts,
        ) = self._getValidTokenFromJSON(json_response)

    def _getTokenHttpRequest(self):
        token_response = requests.get(
            self.token_url, headers=self.headers, verify=False
        )

        return token_response.json()

    def _getValidTokenFromJSON(self, token_response):
        salts = []

        for salt_index in range(1, 6):
            val = int(token_response[f"salt{salt_index}"])
            salts.append(val)

        return (
            *self.token_parser.parse_token_response(token_response),
            int(token_response["serverTime"] / 1000),
            salts,
        )


class TokenParser:
    def __init__(self):
        self.runtime = pywasm.load(f"{pathlib.Path(__file__).parent}/css.wasm")

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

        # print(f"refresh token index {a}, {b}, {c}, {d}, {e}", refresh_token)
        # print(f"access token index {n}, {l}, {o}, {p}, {q}", access_token)

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
