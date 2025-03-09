class NepseInvalidServerResponse(Exception):
    pass


class NepseInvalidClientRequest(Exception):
    pass


class NepseNetworkError(Exception):
    def __init__(self, response):
        self.response = response


class NepseTokenExpired(Exception):
    pass


class NepseInvalidScrip(Exception):
    pass
