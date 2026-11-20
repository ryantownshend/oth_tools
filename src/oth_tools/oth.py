import sys
import json
from json import JSONDecodeError

import click
from pathlib import Path
from rich import box
from rich.console import Console
from rich.table import Table
from loguru import logger


from oth_tools.model import AREA_MAP, VIC_MAP, CABIN_MAP, TOOL_MAP, TOOL_NAMES, COSMETIC_MAP, UNLOCK_MAP, Vehicle

console = Console()


def split_typename(typename: str) -> str:
    return typename.split(",")[0]


def discover() -> Path | None:
    """
    Check the following locations:

        ~/Documents/My Games/over the hill/Saves/Player1.json
        ~/AppData/LocalLow/Funselektor/over the hill/My Games/over the hill/Saves/Player1.json

    :return: the found Player1.json Path
    """

    app_data = Path(
        "~/AppData/LocalLow/Funselektor/over the hill/My Games/over the hill/Saves/Player1.json"
    ).expanduser()
    if app_data.exists():
        return app_data

    app_data_beta = Path("~/AppData/LocalLow/Funselektor/over the hill/Steam/56990439/Saves/Player1.json").expanduser()
    if app_data_beta.exists():
        return app_data_beta

    my_doc = Path("~/Documents/My Games/over the hill/Saves/Player1.json").expanduser()
    if my_doc.exists():
        return my_doc

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


def load_data(save_file: Path) -> dict | None:
    logger.info(f"Loading {save_file}")
    try:
        with save_file.open(mode="r", encoding="utf-8") as reader:
            data = json.load(reader)
            return data
    except JSONDecodeError as error:
        logger.error(error)
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

    console.print(f"{count} items reset.")


@click.group("main")
@click.option("--debug", is_flag=True, default=False)
@click.option(
    "--file",
    "save_file",
    required=False,
    default=None,
    type=click.Path(
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
        path_type=Path,  # type: ignore[type-var]
    ),
)
@click.option(
    "--dry-run",
    "dry_run",
    is_flag=True,
    default=False,
    help="do not save changes",
)
@click.pass_context
def main(ctx: click.Context, debug: bool, save_file: Path | None = None, dry_run: bool = False) -> None:
    if save_file is None:
        save_file = discover()

    ctx.obj = {
        "debug": debug,
        "save_file": save_file,
        "dry_run": dry_run,
    }

    if not debug:
        logger.remove()
        logger.add(sys.stderr, level="SUCCESS")

    if dry_run:
        logger.warning("Dry run, no changes will be made")

    logger.info("Main")


@main.command("discover", help="Look for the OTH save file")
@click.pass_context
def discover_main(ctx: click.Context) -> None:
    logger.info("Discovering save file")
    result = discover()
    console.print(result)


@main.command("reset", help="Reset the crates, scenic views, recoveries, cabins and trails")
@click.pass_context
def reset_main(ctx: click.Context) -> None:
    logger.info("Resetting save file")

    save_file = ctx.obj["save_file"]

    backup_to(save_file, f"{save_file.name}.backup")

    data = load_data(save_file)
    if data is None:
        sys.exit(1)

    reset_poi(data)

    if not ctx.obj["dry_run"]:
        save_data(data, save_file)


@main.group("pebbles")
@click.pass_context
def pebbles(ctx: click.Context) -> None:
    pass


@pebbles.command("show", help="Show pebbles")
@click.pass_context
def show_pebbles(ctx: click.Context) -> None:
    logger.info("Showing pebbles")
    save_file = ctx.obj["save_file"]
    data = load_data(save_file)

    for item in data["Profile"]["Inventory"]["Items"]:
        typename = split_typename(item["Type"])
        item_id = item["Data"]["ItemId"]

        if typename == "InventoryItem" and item_id == 1608550983:
            console.print(item["Data"]["Count"])
            sys.exit(0)


@pebbles.command("set", help="set pebbles")
@click.argument("pebbles_count", type=int)
@click.pass_context
def set_pebbles(ctx: click.Context, pebbles_count: int) -> None:
    logger.info(f"Setting pebbles to {pebbles_count}")

    save_file = ctx.obj["save_file"]
    data = load_data(save_file)

    for item in data["Profile"]["Inventory"]["Items"]:
        typename = split_typename(item["Type"])
        item_id = item["Data"]["ItemId"]

        if typename == "InventoryItem" and item_id == 1608550983:
            console.print(item)
            item["Data"]["Count"] = pebbles_count
            break

    if not ctx.obj["dry_run"]:
        save_data(data, save_file)


@main.group("vic")
@click.pass_context
def vic(ctx: click.Context) -> None:
    pass


@vic.command("list", help="List vehicles")
@click.pass_context
def list_vic(ctx: click.Context) -> None:
    logger.info(f"Listing vehicles")

    save_file = ctx.obj["save_file"]
    data = load_data(save_file)

    vic_list: list[Vehicle] = []

    for item in data["Profile"]["Inventory"]["Items"]:
        _type = item["Type"].split(",")[0]
        if _type == "VehicleItem":
            _vic = Vehicle.from_dict(item)
            vic_list.append(_vic)

    vic_list.sort()

    table = Table(title="Players", title_justify="left", box=box.ROUNDED)
    table.add_column("ID")
    table.add_column("name")
    table.add_column("Meters")
    table.add_column("Class")

    for _vic in vic_list:
        table.add_row(
            str(_vic.id),
            _vic.name,
            str(_vic.meters_travelled),
            str(_vic.vclass.name.capitalize()),
        )

    console.print(table)


@main.group("poi")
@click.pass_context
def poi(ctx: click.Context) -> None:
    pass


@poi.command("list", help="List found poi")
@click.option("--seen", is_flag=True, default=False, help="Show recently seen or changed poi")
@click.pass_context
def list_poi(ctx: click.Context, seen: bool = False) -> None:
    logger.info(f"Listing found poi")
    save_file = ctx.obj["save_file"]
    data = load_data(save_file)

    if seen:
        _list_poi_seen(data)
    else:
        _list_poi_all(data)


def _list_poi_all(data: dict) -> None:
    for item in data["Profile"]["Inventory"]["VirtualItems"]:
        type_name = split_typename(item["Type"])
        data = item["Data"]
        console.print(f"{type_name: >20s}: {data}")


def _list_poi_seen(data: dict) -> None:

    poi_seen: set = set()
    with open("poi_seen.txt", "r") as seen:
        for line in seen:
            poi_seen.add(int(line))
    for item in data["Profile"]["Inventory"]["VirtualItems"]:
        type_name = split_typename(item["Type"])
        item_id = item["Data"]["ItemId"]
        if "State" in item["Data"]:
            state = item["Data"]["State"]
        else:
            state = 0

        if item_id not in poi_seen and state == 2:
            console.print(f"found: {item_id} : {item}")
            poi_seen.add(item_id)

    with open("poi_seen.txt", "w") as seen:
        for line in poi_seen:
            seen.write(f"{line}\n")


@poi.command("detail", help="Detail of a POI by ID")
@click.argument("poi_id", type=int)
@click.pass_context
def detail_poi(ctx: click.Context, poi_id: int) -> None:
    logger.info(f"Detail of {poi_id}")
    _poi = _get_poi(ctx, poi_id)
    console.print(_poi)


@poi.command("reset", help="Reset a POI by ID")
@click.argument("poi_id", type=int)
@click.pass_context
def reset_poi(ctx: click.Context, poi_id: int) -> None:
    logger.info(f"Resetting {poi_id}")
    save_file = ctx.obj["save_file"]
    data = load_data(save_file)

    _poi: dict | None = None
    for item in data["Profile"]["Inventory"]["VirtualItems"]:
        item_id = item["Data"]["ItemId"]
        if item_id == poi_id:
            _poi = item
            break

    _poi["Data"]["State"] = 1
    if "Completed" in _poi["Data"]:
        _poi["Data"].pop("Completed")

    save_data(data, save_file)

    lines: list[int] = []
    with open("poi_seen.txt", "r") as seen_r:
        for line in seen_r:
            item_id = int(line.strip())
            if item_id != poi_id:
                lines.append(item_id)

    with open("poi_seen.txt", "w") as seen_w:
        for line in lines:
            seen_w.write(f"{str(line)}\n")


def _get_poi(ctx: click.Context, poi_id: int) -> dict | None:
    save_file = ctx.obj["save_file"]
    data = load_data(save_file)

    for item in data["Profile"]["Inventory"]["VirtualItems"]:
        item_id = item["Data"]["ItemId"]
        if item_id == poi_id:
            return item

    for item in data["Profile"]["Inventory"]["Items"]:
        item_id = item["Data"]["ItemId"]
        if item_id == poi_id:
            return item

    return None


if __name__ == "__main__":
    main()
