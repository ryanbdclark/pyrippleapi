import aiohttp
import logging
from logging import Logger

from .exceptions import (
    RippleConnectionError
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

    async def request(self) -> dict:
        """
        Method for calling the Ripple API

        Returns
        ------
        dict: Dictionary containing the response
        """

        async with self.session.request(
            "GET", self._api_url + self._auth_token
        ) as response:
            if response.status != 200:
                raise RippleConnectionError("Error sending request")

            return await response.json()
