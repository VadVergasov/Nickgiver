import requests
import json


class WgApiBlitz:
    """
    Class for making requests.
    """

    def __init__(self, WG_ID, server, language):
        """
        Initialize.
        """
        self.wg_id = WG_ID
        self.server = server
        self.language = language

    def check_return_code(self, response):
        """
        Checks if a returned response is OK.

        If not OK Exception will be raised will additional info.
        """
        if response["status"] != "ok":
            raise Exception(
                "Request returned not OK status", response["status"], response["error"],
            )

    def clans_list(self, clan_tag):
        """
        Get clan info.
        """
        url = (
            "https://api.wotblitz."
            + self.server
            + "/wotb/clans/list/?application_id="
            + self.wg_id
            + "&search="
            + clan_tag
            + "&language="
            + self.language
        )
        request = requests.post(url)
        response = request.json()
        self.check_return_code(response)
        return response

    def clans_info(self, clan_id):
        """
        Get clan info.
        """
        url = (
            "https://api.wotblitz."
            + self.server
            + "/wotb/clans/info/?application_id="
            + self.wg_id
            + "&clan_id="
            + clan_id
            + "&language="
            + self.language
        )
        request = requests.post(url)
        response = request.json()
        self.check_return_code(response)
        return response

    def clans_accountinfo(self, account_id):
        """
        Get info about clans members.
        """
        url = (
            "https://api.wotblitz."
            + self.server
            + "/wotb/clans/accountinfo/?application_id="
            + self.wg_id
            + "&account_id="
            + str(account_id)[1:-1]
        )
        request = requests.post(url)
        response = request.json()
        self.check_return_code(response)
        return response
