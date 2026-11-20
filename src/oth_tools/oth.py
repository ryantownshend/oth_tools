import sys
import json
import click
from pathlib import Path
from rich.console import Console
from loguru import logger

console = Console()


def split_typename(typename: str) -> str:
    return typename.split(",")[0]

def discover() -> Path | None:
    logger.info("Discovering save file")
    """
    Check the following locations:

        ~/Documents/My Games/over the hill/Saves/Player1.json
        ~/AppData/LocalLow/Funselektor/over the hill/My Games/over the hill/Saves/Player1.json

     ~

    :return: the found Player1.json Path
    """

    my_doc = Path("~/Documents/My Games/over the hill/Saves/Player1.json").expanduser()
    if my_doc.exists():
        return my_doc

    app_data = Path("~/AppData/LocalLow/Funselektor/over the hill/My Games/over the hill/Saves/Player1.json").expanduser()
    if app_data.exists():
        return app_data

    return None


def backup_to(save_file: Path, filename: str = "Player1.json.bak001") -> None:
    logger.info(f"Backing up {save_file} to {filename}")
    if save_file.exists():
        dest_path = save_file.parent.joinpath(filename)
        save_file.copy(dest_path)

def restore_from(backup_file: Path, filename: str = "Player1.json") -> None:
    logger.info(f"Restoring from {backup_file}")
    if backup_file.exists():
        save_file = backup_file.parent.joinpath(filename)
        backup_file.copy(save_file)

def load_data(save_file: Path) -> dict:
    logger.info(f"Loading {save_file}")
    with save_file.open(mode="r", encoding="utf-8") as reader:
        data = json.load(reader)
        return data

def save_data(data: dict, save_file: Path) -> None:
    logger.info(f"Saving {save_file}")
    with save_file.open(mode="w", encoding="utf-8") as writer:
        json.dump(data, writer)

def reset_poi(data: dict) -> None:
    """
    PointOfInterestData is Crates and Scenic views
    ObjectiveData is Trails and Recoveries
    """
    logger.info("Resetting Poi: Crates / Scenic / Recoveries / Cabins / Trails")
    count = 0
    for item in data["Profile"]["Inventory"]["VirtualItems"]:
        typename = split_typename(item["Type"])
        if typename == "PointOfInterestData" or typename == "ObjectiveData":
            count += 1
            item["Data"]["State"] = 1
            item["Data"]["Completed"] = False
            # console.print(item)

    print(f"{count} items reset.")



@click.group("main")
def main() -> None:
    logger.info("Main")


@main.command("reset")
def reset() -> None:
    print("reset")

    # logger.remove()
    # logger.add(sys.stderr, level="SUCCESS")

    save_file = discover()
    backup_to(save_file, "Player1.json.bak001")

    data = load_data(save_file)
    console.print(data["Header"])

    reset_poi(data)

    # save_data(data, save_file)






if __name__ == "__main__":
    main()
