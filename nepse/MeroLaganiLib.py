from bs4 import BeautifulSoup
import requests


class MeroLaganiAPI:
    def __init__(self):
        self.base_url = "https://merolagani.com"
        self.end_point_scrip_details = "/CompanyDetail.aspx?symbol="

    def _get_full_url(self, end_point):
        return f"{self.base_url}{end_point}"

    def _get_html_content(self, url):
        html_response = requests.get(url)
        return html_response.content

    def _parse_table_scrip_details(self, content):
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", id="accordion")
        if table == None:
            return None, None
        table_bodies = table.find_all("tbody")
        headers = []
        values = []
        final_value = {}

        for body in table_bodies:
            if len(body.find_all("td")) != 0:
                header = body.find_all("th")[0].text.lstrip().rstrip()
                value = (
                    body.find_all("td")[0]
                    .text.replace("\r\n", "")
                    .replace(" ", "")
                    .lstrip()
                    .rstrip()
                )

                if header != "#":
                    final_value[header] = value

                    headers.append(header)
                    values.append(value)

        return headers, values

    def _filter_dict(self, unfiltered_dict):
        float_or_zero = lambda string: float(string) if len(string) else 0
        to_filter = {
            "Shares Outstanding": (
                "shares_outstanding",
                lambda string: string.replace(",", "") if string else 0,
                float,
            ),
            #'Market Price': ('market_price', lambda string: string.replace(',', ''), float_or_zero),
            "Sector": ("sector", lambda string: string.lower()),
            "1 Year Yield": (
                "one_year_yield",
                lambda string: string[:-1] if string else 0,
                float,
            ),
            "EPS": (
                "eps",
                lambda string: string[: string.index("(")] if string else 0,
                float,
            ),
            #'P/E Ratio': ('p_e_ratio', float_or_zero),
            "Book Value": (
                "book_value",
                lambda string: string.replace(",", "")
                if string and string.count(",")
                else string
                if string
                else 0,
                float,
            ),
            #'PBV':('pbv', float_or_zero),
            "% Dividend": (
                "dividend",
                lambda string: 0
                if not string
                else string[: string.index("(")].replace(",", "")
                if string[: string.index("(")].count(",")
                else string[: string.index("(")],
                float,
            ),
            "% Bonus": (
                "bonus",
                lambda string: string[: string.index("(")] if string else 0,
                float,
            ),
            "Right Share": (
                "right_share",
                lambda string: (
                    string[string.index(":") + 1 : string.index("(")]
                    if string[string.index(":") + 1 : string.index("(")]
                    else 0
                )
                if string and string.count("(FY")
                else 0,
                float,
            ),
            "symbol": ("symbol", lambda string: string.lower()),
        }
        output_dict = {}
        for old_key, values in to_filter.items():
            new_key = to_filter[old_key][0]
            output_dict[new_key] = unfiltered_dict[old_key]
            for func in values[1:]:
                try:
                    output_dict[new_key] = func(output_dict[new_key])
                except:
                    print(old_key, unfiltered_dict)
                    pass
        return output_dict

    def get_scrip_details(self, scrip_id):
        scrip_details_url = (
            f"{self._get_full_url(self.end_point_scrip_details)}{scrip_id}"
        )
        page_content = self._get_html_content(scrip_details_url)
        headers, values = self._parse_table_scrip_details(page_content)
        if headers != None and values != None:
            headers.append("symbol")
            values.append(scrip_id)

        unfiltered_dict = dict(zip(headers, values))
        return self._filter_dict(unfiltered_dict)
        return unfiltered_dict

    def get_scrips_details(self, scrips):
        return map(self.get_scrip_details, scrips)


def test():
    import NepseLib

    nepse = NepseLib.Nepse()
    company_scrips = map(lambda dict: dict["symbol"].lower(), nepse.getCompanyList())

    merolagani = MeroLaganiAPI()
    print(list(merolagani.get_scrips_details(company_scrips)))
    # print(merolagani.get_scrip_details('JBBL'))
