"""
OTH Reset, save file mangler.

The intention here is to take an existing save file and reset the points of interest.

Tested on Python 3.10 using only the standard library.

See `discover()` for the save file locations checked for.

Will create a `.backup` file in the same folder as the target save file.

Will reset crates / scenic views / recoveries / cabins / trails to be discoverable again.

"""

import argparse
import json
from json import JSONDecodeError

from pathlib import Path
import shutil
import logging

logger = logging.getLogger(__name__)


def split_typename(typename: str) -> str:
    return typename.split(",")[0]


def discover() -> Path | None:
    """
    Check the following locations:

        ~/Documents/My Games/over the hill/Saves/Player1.json
        ~/AppData/LocalLow/Funselektor/over the hill/My Games/over the hill/Saves/Player1.json

    :return: the found Player1.json Path
    """

    my_doc = Path("~/Documents/My Games/over the hill/Saves/Player1.json").expanduser()
    if my_doc.exists():
        return my_doc

    app_data = Path(
        "~/AppData/LocalLow/Funselektor/over the hill/My Games/over the hill/Saves/Player1.json"
    ).expanduser()
    if app_data.exists():
        return app_data

    return None


def backup_to(save_file: Path, filename: str | None) -> None:
    if filename is None:
        filename = f"{save_file.name}.backup"
    logger.info(f"Backing up {save_file} to {filename}")

    if save_file.exists():
        dest_path = save_file.parent.joinpath(filename)
        shutil.copy(save_file, dest_path)


def load_data(save_file: Path) -> dict | None:
    logger.info(f"Loading {save_file}")
    try:
        with save_file.open(mode="r", encoding="utf-8") as reader:
            data = json.load(reader)
            return data
    except JSONDecodeError as error:
        logger.error(f"JSON Decode error: {error}")
        return None
    except FileNotFoundError as error:
        logger.error(error)
        return None


def save_data(data: dict, save_file: Path) -> None:
    logger.info(f"Saving {save_file}")
    with save_file.open(mode="w", encoding="utf-8") as writer:
        json.dump(data, writer)


def reset_poi(data: dict) -> None:
    """
    PointOfInterestData is Crates and Scenic views
    ObjectiveData is Trails and Recoveries
    """
    logger.info("Resetting POI: crates / scenic views / recoveries / cabins / trails")
    count = 0
    for item in data["Profile"]["Inventory"]["VirtualItems"]:
        typename = split_typename(item["Type"])
        if typename == "PointOfInterestData" or typename == "ObjectiveData":
            count += 1
            item["Data"]["State"] = 1
            item["Data"]["Completed"] = False

    print(f"{count} items reset.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Process the OTH save file to reset points of interest.")
    parser.add_argument("--filename", help="Path to the save file if not in standard location")
    args = parser.parse_args()

    if args.filename:
        save_file = Path(args.filename)
    else:
        save_file = discover()
    print(save_file)
    data = load_data(save_file)

    reset_poi(data)
    save_data(data, save_file)


if __name__ == "__main__":
    main()
