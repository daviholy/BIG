from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing_extensions import Annotated
from dataclasses import dataclass

intpk = Annotated[int,mapped_column(primary_key=True)]

class Base(DeclarativeBase):
    ...

@dataclass
class School(Base):
    __tablename__ = "schools"

    id: Mapped[intpk]
    name: Mapped[str]
    total_absolvents: Mapped[int]
    faculty: Mapped[str]
    program: Mapped[str]
    www: Mapped[str]
