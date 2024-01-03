from typing import Self
from neomodel import StructuredNode, ArrayProperty, StringProperty, RelationshipTo, db

class Person(StructuredNode):
    name = StringProperty(required=True)
    age = StringProperty(required=True)
    hobbies= ArrayProperty(StringProperty())
    likes = RelationshipTo('Person',"LIKES")
    dislikes = RelationshipTo('Person', "DISLIKES")

    def matches(self) -> list[Self]:
        rows, columns = db.cypher_query(f"""
        MATCH (friend:Person)-[:LIKES]->(user:Person)-[:LIKES]->(friend:Person) 
        WHERE user.name = "{self.name}"
        RETURN friend
    """)
        return [self.inflate(person[0]) for person in rows]
    
    def available_matches(self) -> list[Self]:
        rows, columns = db.cypher_query(f"""
                MATCH (user:Person)
                MATCH (friend:Person)
                WHERE user.name = "{self.name}"
                AND NOT (user:Person)-[:LIKES]->(friend:Person)
                AND NOT (friend:Person)-[:DISLIKES]->(user:Person)
                AND NOT (user:Person)-[:DISLIKES]->(friend:Person)
                AND NOT friend.name = "{self.name}"
                RETURN friend
            """)
        return [self.inflate(person[0]) for person in rows]
    
    def like(self,other:Self):
        return self.likes.connect(other) # type: ignore
    
    def dislike(self,other:Self):
        return self.dislikes.connect(other) # type: ignore