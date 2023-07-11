from src.pyrippleapi.api import RippleAPI
from src.pyrippleapi.generation_asset import GenerationAsset

import asyncio
import json


async def run():
    with open("login.json") as file:
        data = json.load(file)
    api = RippleAPI(data["auth_token"])

    data = await api.request()
    # print(devices)
    assets = {
        asset["name"]: GenerationAsset(api, asset)
        for asset in data["generation_assets"]
    }
    for asset in assets.values():
        properties = await asset.update_data()
        print(asset.generation_unit)
        print(properties["telemetry"])
        print(properties["generation_data"])

    await api.close()


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run())
