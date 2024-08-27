import logging
from logging import Logger
import datetime
from .api import RippleAPI
from typing import Union

logger: Logger = logging.getLogger(__package__)


class GenerationAsset:
    """
    Class representing a Rippler generation asset device

    Methods
    -------
    get_telemetry:
        sets the latest telemetry data
    get_generation:
        sets the latest generation data
    update_properties
        usees the RippleAPI object to call the ripple server and return the current properties of the device.
    """

    def __init__(
        self, api: RippleAPI, data: dict[str : Union[str, int, bool, list]], email: str
    ) -> None:
        """
        Constructs an Ripple generation asset object representing the generation asset

        Parameters
        ----------
        api (RippleAPI):RippleAPI object used to call the Ripple API
        data (dict):Data returned from the Ripple API showing the details of the generation assets
        """
        self._api = api
        self._email = email
        self._name = data["name"]
        self._type = data["type"]
        self._status = data["status"]
        self._member_capacity = data["member_capacity"]
        self._member_capacity_units = data["member_capacity_units"]
        self._member_expected_annual_generation = data[
            "member_expected_annual_generation"
        ]
        self._member_expected_annual_generation_units = data[
            "member_expected_annual_generation_units"
        ]

        self._generation_units = data["generation"]["generation_unit"]
        self._estimated_savings_unit = "£"

        self._latest_telemetry = {}
        self._generation_data = {}

    @property
    def email(self) -> str:
        return self._email

    @property
    def generation_unit(self) -> str:
        return self._generation_units

    @property
    def estimated_savings_unit(self) -> str:
        return self._estimated_savings_unit

    @property
    def api(self) -> RippleAPI:
        return self._api

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def status(self) -> str:
        return self._status

    @property
    def member_capacity(self) -> str:
        return self._member_capacity

    @property
    def member_capacity_units(self) -> str:
        return self._member_capacity_units

    @property
    def member_expected_annual_generation(self) -> str:
        return self._member_expected_annual_generation

    @property
    def member_expected_annual_generation_units(self) -> str:
        return self._member_expected_annual_generation_units

    @property
    def latest_telemetry(self) -> dict:
        return self._latest_telemetry

    @property
    def generation_data(self) -> dict[str:str]:
        return self._generation_data

    async def update_asset_info(self, data) -> None:
        self._status = data["status"]
        self._member_capacity = data["member_capacity"]
        self._member_capacity_units = data["member_capacity_units"]
        self._member_expected_annual_generation = data[
            "member_expected_annual_generation"
        ]
        self._member_expected_annual_generation_units = data[
            "member_expected_annual_generation_units"
        ]

    async def get_telemetry(self, data) -> None:
        self._latest_telemetry = data["latest_telemetry"]
        if "timestamp" in self._latest_telemetry:
            self._latest_telemetry["timestamp"] = datetime.datetime.strptime(
                self._latest_telemetry["timestamp"],
                "%Y-%m-%dT%H:%M:%SZ",
            ).strftime("%Y/%m/%d %H:%M:%S")
        else:
            self._latest_telemetry["timestamp"] = "0001/01/01 00:00:00"

    async def get_generation(self, data) -> None:
        for time_scale in [
            "today",
            "yesterday",
            "this_week",
            "last_week",
            "this_month",
            "last_month",
            "this_year",
            "last_year",
            "total",
        ]:
            self._generation_data[time_scale + "_earned"] = data[time_scale]["earned"]
            self._generation_data[time_scale + "_generated"] = data[time_scale][
                "generated"
            ]
        if data["latest"]:
            self._generation_data["latest_earned"] = data["latest"]["estimated_savings"]
            self._generation_data["latest_generated"] = data["latest"]["generation"]

    async def update_data(
        self,
    ) -> dict:
        """
        Calls the Ripple api to update the properties and then returns the telemetry data and generation data.

        Returns
        -------
        (dict):Dictionary containing two dictionaries, one with the telemetry data from the API and another with the generation_data from the api
        """
        logging.info(f"Updating properties for device {self.name}")
        data = await self._api.request(assets=[self.name])

        data = data["generation_assets"]

        names = [asset["name"] for asset in data]

        if self._name not in names:
            return {{"telemetry": {}}, {"generation_data": {}}}

        generation_data = {}

        for asset in data:
            if asset["name"] == self._name:
                generation_data = asset
                break

        await self.update_asset_info(generation_data)
        await self.get_telemetry(generation_data["generation"])
        await self.get_generation(generation_data["generation"])

        return {
            "telemetry": self._latest_telemetry,
            "generation_data": self._generation_data,
        }
