import logging
from logging import Logger

import aiohttp

from .exceptions import (
    RippleAuthenticationError,
    RippleConnectionError,
    RippleDevicesError,
)

logger: Logger = logging.getLogger(__package__)


class RippleAPI:
    """
    A class that creates an API object, to be used to call against the Ripple Energy API

    Attributes
    ----------
    auth_token : str
        once autherntiacted the auth token will be stored in the object to be used for future api calls
    session : aiohttp.ClientSession
        The aiohttp session is stored to be called against

    Methods
    -------
    close:
        Closes the aiohttp ClientSession that is stored in the session variable
    request:
        get the current data from the api and returns the json response given
    """

    def __init__(
        self,
        auth_token: str = None,
        session: aiohttp.ClientSession = None,
    ) -> None:
        """
        Sets all the necessary variables for the API caller based on the passed in information, if a session is not passed in then one is created

        Parameters
        ---------
        auth_token (str):Once authentiacted the auth token will be stored in the object to be used for future api calls
        session (aiohttp.ClientSession), optional:The aiohttp session is stored to be called against
        """
        self._auth_token: str = auth_token
        self.session = session
        self._api_url = "https://rippleenergy.com/rest/member_data/"

        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close(self) -> None:
        """
        Closes the aiohttp ClientSession

        Returns
        -------
        None
        """
        if self.session:
            await self.session.close()

    async def request(self, assets: list[str] = []) -> dict:
        """
        Method for calling the Ripple API

        Returns
        ------
        dict: Dictionary containing the response
        """

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        }

        async with self.session.request(
            "GET", self._api_url + self._auth_token, headers=headers
        ) as response:
            if response.status != 200:
                raise RippleConnectionError("Error sending request")

            response = await response.json()

            if "error" in response:
                raise RippleAuthenticationError("Invalid API Key")

            if len(response["generation_assets"]) < 1:
                raise RippleDevicesError("No generation assets found")

            for asset in enumerate(response["generation_assets"]):
                if asset[1]["name"] not in assets:
                    del response["generation_assets"][asset[0]]

            return response
