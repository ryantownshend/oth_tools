"""
data["Profile"]["Inventory"]["Items"]:
{'InventoryItem', 'VehicleSpecificItem', 'VehicleItem'}

data["Profile"]["Inventory"]["VirtualItems"]:
{'VehicleSpecificItem', 'InventoryItem', 'VehicleItem'}
{'AreaItem', 'PointOfInterestData', 'ObjectiveData', 'AnimalItem'}

PointOfInterestData is Crates and Scenic views
ObjectiveData is Trails and Recoveries

"""

from __future__ import annotations
import json
import click
from pathlib import Path
from rich.console import Console
from dataclasses import dataclass

from oth_tools.model import AREA_MAP, VIC_MAP, CABIN_MAP, TOOL_MAP, TOOL_NAMES, COSMETIC_MAP, UNLOCK_MAP, Vehicle

console = Console()


def split_typename(typename: str) -> str:
    return typename.split(",")[0]


def process_keysets(data: dict) -> None:
    i_set: set = set()
    for item in data["Profile"]["Inventory"]["Items"]:
        name = split_typename(item["Type"])
        i_set.add(name)

    console.print(i_set)
    # {'InventoryItem', 'VehicleSpecificItem', 'VehicleItem'}

    v_set: set = set()
    for item in data["Profile"]["Inventory"]["VirtualItems"]:
        name = split_typename(item["Type"])
        v_set.add(name)

    console.print(v_set)
    # {'VehicleSpecificItem', 'InventoryItem', 'VehicleItem'}
    # {'AreaItem', 'PointOfInterestData', 'ObjectiveData', 'AnimalItem'}


def process_meta(data: dict) -> None:
    console.print(data["Header"])
    for key, value in data["Profile"].items():
        if key != "Inventory":
            console.print(key, value)


def process_vehicles(data: dict) -> None:
    for item in data["Profile"]["Inventory"]["Items"]:
        _type = item["Type"].split(",")[0]
        if _type == "VehicleItem":
            console.print(item)
            # if "MetersTravelled" in item["Data"]:
            #     item_id = item["Data"]["ItemId"]
            #     if item_id in VIC_MAP:
            #         name = VIC_MAP[item_id]
            #     else:
            #         name = item_id
            # console.print(f'{name}: {item["Data"]["MetersTravelled"]}')


def process_blast_wagon(data: dict) -> None:
    blast_wagon_id = 1808898351

    for item in data["Profile"]["Inventory"]["Items"]:
        # console.print(item)
        if item["Data"]["ItemId"] == blast_wagon_id:
            console.print(item)

            # vic = _process_vehicle_item(item)
            vic = Vehicle.from_dict(item)
            console.print(vic)
            console.print("---")
            console.print(vic.to_dict())


def process_toolsets(data: dict) -> None:
    for item in data["Profile"]["Inventory"]["Items"]:
        console.print(item["Type"])


def search_for_new_points(data: dict) -> None:
    poi_seen: set = set()
    with open("poi_seen.txt", "r") as seen:
        for line in seen:
            poi_seen.add(int(line))

    for item in data["Profile"]["Inventory"]["VirtualItems"]:
        typename = split_typename(item["Type"])
        if typename == "PointOfInterestData":
            item_id = item["Data"]["ItemId"]
            state = item["Data"]["State"]
            if state == 2:
                if item_id not in poi_seen:
                    print("found: ", item_id)
                    poi_seen.add(item_id)

    with open("poi_seen.txt", "w") as seen:
        for line in poi_seen:
            seen.write(f"{line}\n")


def process_obj(data: dict) -> None:
    for item in data["Profile"]["Inventory"]["VirtualItems"]:
        typename = split_typename(item["Type"])
        if typename == "ObjectiveData":
            console.print(item)


def process_areas(data: dict) -> None:
    for item in data["Profile"]["Inventory"]["VirtualItems"]:
        typename = split_typename(item["Type"])
        if typename == "AreaItem":
            console.print(item)


def process_pebbles(data: dict) -> None:
    """
    {
        "Type": "InventoryItem, Assembly-CSharp",
        "Data":
        {
            "ItemId": 1608550983,
            "IsNew": true,
            "Count": 684
        }
    },
    """
    for item in data["Profile"]["Inventory"]["Items"]:
        typename = split_typename(item["Type"])
        item_id = item["Data"]["ItemId"]

        if typename == "InventoryItem" and item_id == 1608550983:
            console.print(item)


blast_wagon_string = """
{
    'Type': 'VehicleItem, Assembly-CSharp',
    'Data': {'ItemId': 1808898351, 'Count': 1, 'InUse': True, 'MetersTravelled': 164050, 'ToolsetIDs': [2317836723, 2317836723, 1440544897, 2436578994]}
}
"""


@click.command()
@click.argument(
    "filename",
    type=click.Path(
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
        path_type=Path,  # type: ignore[type-var]
    ),
)
def main(filename):
    print(filename)
    data = json.load(open(filename))
    # process_keysets(data)
    # process_meta(data)
    # process_vehicles(data)
    # process_blast_wagon(data)
    # process_toolsets(data)
    # search_for_new_points(data)
    # process_obj(data)
    # process_areas(data)
    # process_pebbles(data)


if __name__ == "__main__":
    main()
