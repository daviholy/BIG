import csv
from pathlib import Path
import re
from pymongo.collection import Collection


def init(src: Path,col: Collection):
    """
    Initilialize and filll the mongo db

    Args:
        Path (src): path to the source file
    """
    reg_exp = "(\d+)(?:\s*-\s*(\d+))?(?:\s*až\s*(\d+))?" # type: ignore
    res = []
    with src.open("r") as opened_file:
        for line in csv.DictReader(opened_file):
            pat = re.search(reg_exp, line["velikostobce_txt"])
            if pat:
                line["velikostobce_txt"] = pat.group()
            res.append(line)
        col.insert_many(res)