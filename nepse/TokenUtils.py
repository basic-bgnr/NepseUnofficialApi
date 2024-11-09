import asyncio
import pathlib
import time
from datetime import datetime

import pywasm


class _TokenManager:
    def __init__(self, nepse):
        self.nepse = nepse

        self.MAX_UPDATE_PERIOD = 45

        self.token_parser = TokenParser()

        self.token_url = "/api/authenticate/prove"
        self.refresh_url = "/api/authenticate/refresh-token"

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

    def __repr__(self):
        return (
            f"Access Token: {self.access_token}\nRefresh Token: {self.refresh_token}\nSalts: {self.salts}\nTimeStamp: {datetime.fromtimestamp(self.token_time_stamp).strftime('%Y-%m-%d %H:%M:%S')}"
            if self.access_token is not None
            else "Token Manager Not Initialized"
        )

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


class AsyncTokenManager(_TokenManager):
    def __init__(self, nepse):
        super().__init__(nepse)

        self.update_started = asyncio.Event()
        self.update_completed = asyncio.Event()

    async def getAccessToken(self):
        if self.isTokenValid():
            return self.access_token
        else:
            await self.update()
            return self.access_token

    async def getRefreshToken(self):
        if self.isTokenValid():
            return self.access_token
        else:
            await self.update()
            return self.refresh_token

    async def update(self):
        await self._setToken()

    async def _setToken(self):
        if not self.update_started.is_set():
            self.update_started.set()
            self.update_completed.clear()
            json_response = await self._getTokenHttpRequest()
            (
                self.access_token,
                self.refresh_token,
                self.token_time_stamp,
                self.salts,
            ) = self._getValidTokenFromJSON(json_response)
            self.update_completed.set()
            self.update_started.clear()
        else:
            await self.update_completed.wait()

    async def _getTokenHttpRequest(self):
        return await self.nepse.requestGETAPI(
            url=self.token_url, include_authorization_headers=False
        )


class TokenManager(_TokenManager):
    def __init__(self, nepse):
        super().__init__(nepse)

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

    def _setToken(self):
        json_response = self._getTokenHttpRequest()

        (
            self.access_token,
            self.refresh_token,
            self.token_time_stamp,
            self.salts,
        ) = self._getValidTokenFromJSON(json_response)

    def _getTokenHttpRequest(self):
        return self.nepse.requestGETAPI(
            url=self.token_url, include_authorization_headers=False
        )

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
        self.runtime = pywasm.core.Runtime()
        self.wasm_module = self.runtime.instance_from_file(
            f"{pathlib.Path(__file__).parent}/data/css.wasm"
        )

    def parse_token_response(self, token_response):
        n = self.runtime.invocate(
            self.wasm_module,
            "cdx",
            [
                token_response["salt1"],
                token_response["salt2"],
                token_response["salt3"],
                token_response["salt4"],
                token_response["salt5"],
            ],
        )[0]
        l = self.runtime.invocate(
            self.wasm_module,
            "rdx",
            [
                token_response["salt1"],
                token_response["salt2"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )[0]
        o = self.runtime.invocate(
            self.wasm_module,
            "bdx",
            [
                token_response["salt1"],
                token_response["salt2"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )[0]
        p = self.runtime.invocate(
            self.wasm_module,
            "ndx",
            [
                token_response["salt1"],
                token_response["salt2"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )[0]
        q = self.runtime.invocate(
            self.wasm_module,
            "mdx",
            [
                token_response["salt1"],
                token_response["salt2"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )[0]

        a = self.runtime.invocate(
            self.wasm_module,
            "cdx",
            [
                token_response["salt2"],
                token_response["salt1"],
                token_response["salt3"],
                token_response["salt5"],
                token_response["salt4"],
            ],
        )[0]
        b = self.runtime.invocate(
            self.wasm_module,
            "rdx",
            [
                token_response["salt2"],
                token_response["salt1"],
                token_response["salt3"],
                token_response["salt4"],
                token_response["salt5"],
            ],
        )[0]
        c = self.runtime.invocate(
            self.wasm_module,
            "bdx",
            [
                token_response["salt2"],
                token_response["salt1"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )[0]
        d = self.runtime.invocate(
            self.wasm_module,
            "ndx",
            [
                token_response["salt2"],
                token_response["salt1"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )[0]
        e = self.runtime.invocate(
            self.wasm_module,
            "mdx",
            [
                token_response["salt2"],
                token_response["salt1"],
                token_response["salt4"],
                token_response["salt3"],
                token_response["salt5"],
            ],
        )[0]

        access_token = token_response["accessToken"]
        refresh_token = token_response["refreshToken"]

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
