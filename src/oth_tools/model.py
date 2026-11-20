from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum

AREA_MAP: dict = {
    1404582921: "C?",
    2016554849: "C?",
    2245356061: "C?",
    1547044322: "A1",
    2777299617: "A2",
}


VIC_MAP: dict = {
    1691061460: "The Brick",
    1236419262: "The Bull V1",
    1461055881: "The Ding",
    3404874685: "Das Lynx",
    3098383629: "The Polyana",
    1046421331: "The Protector",
    2047734690: "The Tinny",
    1043242486: "The Trailrat",
    3658652804: "Das Wombat",
    3847423181: "The Cumbre",
    2033237166: "The Grand Woodman",
    3262308567: "The Roamer",
    2035762699: "The Trail Burner",
    1779250133: "The Woodman",
    1808898351: "The Blast Wagon",
    2998940911: "The Boar",
    1260490138: "The Burro",
    1018520739: "Das Rust Ox",
    2098325991: "The Timberbox",
    1932033467: "Das Mammoth",
    2266109950: "The Marshal",
}

# Cabins, Portals, Mechanics
CABIN_MAP: dict = {
    1101794939: {"name": "Pavilion Lake Cabin", "map": "C1", "grid": "B5"},
    3483716394: {"name": "Crazy Gunther", "map": "C1", "grid": "B5"},
    1226452874: {"name": "Elizabeth Lake Cabin", "map": "C1", "grid": "B4"},
    1156766673: {"name": "Brew Hut", "map": "C1", "grid": "C4"},
    1111806668: {"name": "Black Bear's Den", "map": "C1", "grid": "E4"},
    2349692358: {"name": "Ferry to the Ridge", "map": "C1", "grid": "F5"},
    1011907904: {"name": "Birch Grove Hut", "map": "C1", "grid": "E5"},
    1815311426: {"name": "Malachite Lodge", "map": "C1", "grid": "G6"},
    2281158188: {"name": "Ferry To The Mountain", "map": "C2", "grid": "D6"},
    1750341430: {"name": "Sunset Landing Cabin", "map": "C2", "grid": "D6"},
    1688272994: {"name": "Secluded Marsh Bunkie", "map": "C2", "grid": "E7"},
    1689746922: {"name": "Nerthus Cabin", "map": "C2", "grid": "C7"},
    4053512632: {"name": "Crazy Gunther", "map": "C2", "grid": "F6"},
    2196576037: {"name": "Valkyr Lodge", "map": "C2", "grid": "F5"},
    2786927816: {"name": "Lake View Cabin", "map": "C2", "grid": "D5"},
    1746949483: {"name": "Mount Gibson Lodge", "map": "C2", "grid": "B4"},
    2813951711: {"name": "Seer Lodge", "map": "C2", "grid": "D3"},
    1247617841: {"name": "Powder Creek Lodge", "map": "C2", "grid": "E4"},
    1923376065: {"name": "Whitecap Alpine Lodge", "map": "C2", "grid": "F2"},
    2454176252: {"name": "Tunnel to Asgard Mountain", "map": "C2", "grid": "G1"},
    2776394955: {"name": "Tunnel to Gimli Ridge", "map": "C3", "grid": "C8"},
    2024271429: {"name": "Shaughnessey Cabin", "map": "C3", "grid": "C8"},
    4118214863: {"name": "Crazy Gunther", "map": "C3", "grid": "C7"},
    2176336079: {"name": "Ridgeline Rest", "map": "C3", "grid": "C6"},
    2889717940: {"name": "Eagle Perch Cabin", "map": "C3", "grid": "B5"},
    1950602491: {"name": "Twin Pools Cabin", "map": "C3", "grid": "F8"},
    2612748625: {"name": "Rock Cradle Cabin", "map": "C3", "grid": "F6"},
    2555575997: {"name": "Crossroads Shelter", "map": "C3", "grid": "E4"},
    2367972595: {"name": "Similkameen Lodge", "map": "C3", "grid": "G3"},
}


# NNNNNNNNNN: {"name": "nnnnnnnnnnnn", "map": "C3", "grid": ""},
# NNNNNNNNNN: {"name": "nnnnnnnnnnnn", "map": "C3", "grid": ""},
# NNNNNNNNNN: {"name": "nnnnnnnnnnnn", "map": "C3", "grid": ""},
# NNNNNNNNNN: {"name": "nnnnnnnnnnnn", "map": "C3", "grid": ""},
# NNNNNNNNNN: {"name": "nnnnnnnnnnnn", "map": "C3", "grid": ""},
# NNNNNNNNNN: {"name": "nnnnnnnnnnnn", "map": "C3", "grid": ""},
# NNNNNNNNNN: {"name": "nnnnnnnnnnnn", "map": "C3", "grid": ""},
# NNNNNNNNNN: {"name": "nnnnnnnnnnnn", "map": "C3", "grid": ""},

# old bad?
# 1749856058: {"name": "Elizabeth Lake Cabin", "map": "C1"},

TOOL_MAP: dict = {
    2317836723: "Portable Winch",
    1440544897: "Cloud Clearing Bell",
    2436578994: "Meteorite radar",
    2739151752: "Camp tool",
    2833126067: "Jack",
    3771754783: "Planks",
    1619438792: "Repair Kit",
}

TOOL_NAMES = {v: k for k, v in TOOL_MAP.items()}

COSMETIC_MAP: dict = {}

UNLOCK_MAP: dict = {}


class VClass(IntEnum):
    TRAIL = 1
    WAGON = 2
    WORKHORSE = 3
    EXPEDITION = 4
    UNKNOWN = 5


class PType(IntEnum):
    CRATE = 1
    SCENIC_VIEW = 2
    RECOVERY = 3
    TRAIL = 4
    CABIN = 5
    MERCHANT = 6


VIC_CLASSES: dict = {
    "trail": [
        1691061460,
        1236419262,
        1461055881,
        3404874685,
        3098383629,
        1046421331,
        2047734690,
        1043242486,
        3658652804,
    ],
    "wagon": [
        3847423181,
        2033237166,
        3262308567,
        2035762699,
        1779250133,
    ],
    "workhorse": [
        1808898351,
        2998940911,
        1260490138,
        1018520739,
        2098325991,
    ],
    "expedition": [
        1932033467,
        2266109950,
    ],
}


def _class_for_vic(vic_id: int) -> VClass:
    if vic_id in VIC_CLASSES["trail"]:
        return VClass.TRAIL
    if vic_id in VIC_CLASSES["wagon"]:
        return VClass.WAGON
    if vic_id in VIC_CLASSES["workhorse"]:
        return VClass.WORKHORSE
    if vic_id in VIC_CLASSES["expedition"]:
        return VClass.EXPEDITION
    return VClass.UNKNOWN


@dataclass
class Vehicle:
    id: int
    name: str
    count: int
    in_use: bool
    meters_travelled: int
    tools: list[str]
    vclass: VClass

    @staticmethod
    def from_dict(item: dict) -> Vehicle:
        vic_id = item["Data"]["ItemId"]
        name = VIC_MAP[item["Data"]["ItemId"]]
        count = item["Data"]["Count"]
        if "InUse" in item:
            in_use = item["Data"]["InUse"]
        else:
            in_use = False
        if "MetersTravelled" in item["Data"]:
            meters = item["Data"]["MetersTravelled"]
        else:
            meters = 0

        tools = []
        for tool_id in item["Data"]["ToolsetIDs"]:
            if tool_id in TOOL_MAP:
                tools.append(TOOL_MAP[tool_id])
        _vclass = _class_for_vic(vic_id)

        vic = Vehicle(vic_id, name, count, in_use, meters, tools, _vclass)
        return vic

    def to_dict(self) -> dict:
        """
        {
            'Type': 'VehicleItem, Assembly-CSharp',
            'Data': {'ItemId': 1808898351, 'Count': 1, 'InUse': True, 'MetersTravelled': 164050, 'ToolsetIDs': [2317836723, 2317836723, 1440544897, 2436578994]}
        }
        :return:
        """

        raw_ids: list[int] = []
        for tool in self.tools:
            tid = TOOL_NAMES[tool]
            raw_ids.append(tid)

        # pad the tool_ids with zeros out to 4 positions
        tool_ids: list[int] = raw_ids + [0] * (4 - len(raw_ids))

        return {
            "Type": "VehicleItem, Assembly-CSharp",
            "Data": {
                "ItemId": self.id,
                "Count": self.count,
                "InUse": self.in_use,
                "MetersTravelled": self.meters_travelled,
                "ToolsetIDs": tool_ids,
            },
        }

    def __hash__(self) -> int:
        return self.id

    def __lt__(self, other: Vehicle) -> bool:
        """
        Order by class then alphabetical

        1. Trail
        2. Wagon
        3. Workhorse
        4. Expedition
        """

        if self.vclass == other.vclass:
            return self.name < other.name

        return self.vclass < other.vclass


@dataclass
class Crate:
    id: int
    state: int
    completed: bool = False
    type_name: str = "PointOfInterestData"

    @staticmethod
    def from_dict(item: dict) -> Crate:
        item_id = item["Data"]["ItemId"]
        state = item["Data"]["State"]
        if "Completed" in item["Data"]:
            completed = item["Data"]["Completed"]
        else:
            completed = False

        result = Crate(
            id=item_id,
            state=state,
            completed=completed,
        )
        return result

    def to_dict(self) -> dict:
        result = {
            "Type": f"{self.type_name}, Assembly-CSharp",
            "Data": {
                "ItemId": self.id,
                "State": self.state,
            },
        }
        if self.completed:
            result["Date"]["Completed"] = True

        return result


@dataclass
class Cabin:
    id: int
    state: int
    completed: bool = False
    interaction_count: int = 0
    type_name: str = "PointOfInterestData"

    @staticmethod
    def from_dict(item: dict) -> Cabin:
        item_id = item["Data"]["ItemId"]
        state = item["Data"]["State"]
        if "Completed" in item["Data"]:
            completed = item["Data"]["Completed"]
        else:
            completed = False

        if "InteractionCount" in item["Data"]:
            interaction_count = item["Data"]["InteractionCount"]
        else:
            interaction_count = 0

        result = Cabin(
            id=item_id,
            state=state,
            completed=completed,
            interaction_count=interaction_count,
        )
        return result

    def to_dict(self) -> dict:
        result = {
            "Type": f"{self.type_name}, Assembly-CSharp",
            "Data": {
                "ItemId": self.id,
                "State": self.state,
                "InteractionCount": self.interaction_count,
            },
        }
        return result
