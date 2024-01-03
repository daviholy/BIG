from math import ceil
from pathlib import Path
from typing import Callable
from sqlalchemy import create_engine, URL, inspect, select, func
from sqlalchemy.orm import sessionmaker, InstrumentedAttribute
from .db_schema import Base, School
import csv
import os

pagination = 20

engine = create_engine(
    URL.create(
        "postgresql+psycopg2",
        username=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host="db",
        database=os.environ["POSTGRES_DB"],
    ),
    future=True
)

Session = sessionmaker(engine, future=True)

def create_db(csv_file: Path) -> None:
    Base.metadata.create_all(engine)

    with Session() as session:
        with open(csv_file) as file:
            for line in csv.DictReader(file):
                session.add(
                    School(
                        id=int(line["OBJECTID"]),
                        name=line["nazev"],
                        faculty=line["fakulta_pracoviste"],
                        program=line["nazev_studijniho_programu"],
                        www=line["www"],
                        total_absolvents=int(line["celkem_cr"])
                    )
                )
        session.flush()
        session.commit()

def fetch_data(page:int, order_by: InstrumentedAttribute | None = None):
    stms = select(School)
    if order_by:
        stms = stms.order_by(order_by.desc())
    with Session() as session:
        res = session.execute(stms.execution_options(yield_per=pagination)).partitions(pagination)

        for _ in range(page):
            next(res)
        return [item for item, in next(res)]
    
def school_count() -> int:
    with Session() as session:
        res = session.scalar(select(func.count()).select_from(School))
        if res is None:
            raise Exception("not any data returned")

        return res// pagination

def initialized() -> bool:
    return inspect(engine).has_table(School.__tablename__)


if not initialized():
    create_db(Path("data.csv"))
