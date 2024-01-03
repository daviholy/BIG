from neomodel import Relationship
from .entities import Person


def init():
    """
    Initilialize and filll the mongo db

    Args:
        Path (src): path to the source file
    """

    users = []
    pepa = Person(name="Pepa", age=34, hobbies=["programming", "running"]).save()
    jana = Person(name="Jana", age=30, hobbies=["cats", "running"]).save()
    michal = Person(name="Michal", age=40, hobbies=["partying", "cats"]).save()
    alena = Person(name="Alena", age=32, hobbies=["kids", "cats"]).save()
    richard = Person(name="Richard", age=33, hobbies=["partying", "cats"]).save()

    pepa.likes.connect(jana) # type: ignore
    jana.likes.connect(pepa) # type: ignore
    michal.likes.connect(alena) # type: ignore
    alena.dislikes.connect(michal) # type: ignore