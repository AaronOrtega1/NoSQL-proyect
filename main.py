import os
import csv
from neo4j import GraphDatabase
from neo4j.exceptions import ConstraintError
from fastapi import FastAPI
from routes import router as book_router

class flight_data(object):
    def __init__(self, uri, user, password):
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self._create_constraints()

    def close(self):
        self.driver.close()

    def _create_constraints(self):
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT unique_user IF NOT EXISTS FOR (u:User) REQUIRE u.username IS UNIQUE")
            session.run("CREATE CONSTRAINT unique_airline IF NOT EXISTS FOR (a:Airline) REQUIRE a.airline_name IS UNIQUE")
            session.run("CREATE CONSTRAINT unique_destiny IF NOT EXISTS FOR (d:Destiny) REQUIRE d.destiny_name IS UNIQUE")
    
    def _create_user_node(self, username, age, gender):
        with self.driver.session() as session:
            try:
                session.run("CREATE (u:User {username: $username, age: $age, gender: $gender})", username = username, age = age, gender = gender )
            except ConstraintError:
                print(eval(ConstraintError))
                pass
    
    def _create_airline_node(self, airline_name):
        with self.driver.session() as session:
            try:
                session.run("CREATE (a:Airline {airline_name: $airline_name})", airline_name = airline_name)
            except ConstraintError:
                print(eval(ConstraintError))
                pass
    
    def _create_destiny_node(self, destiny_name):
        with self.driver.session() as session:
            try:
                session.run("CREATE (d:Destiny {destiny_name: $destiny_name})", destiny_name = destiny_name)
            except ConstraintError:
                print(eval(ConstraintError))
                pass

    def _create_reason_node(self, reason_name):
        with self.driver.session() as session:
            try:
                session.run("CREATE (r:Reason {reason_name: $reason_name})", reason_name = reason_name)
            except ConstraintError:
                print(eval(ConstraintError))
                pass
        
    def _create_stay_node(self, stay_name):
        with self.driver.session() as session:
            try:
                session.run("CREATE (s:Stay {stay_name: $stay_name})", stay_name = stay_name)
            except ConstraintError:
                print(eval(ConstraintError))
                pass

    def _create_user_to_movie_relationship(self, username, movie_name):
            with self.driver.session() as session:
                session.run("""
                    MATCH (u:User), (m:Movie)
                    WHERE u.username=$username AND m.movie_name=$movie_name
                    CREATE (u)-[r:HAS_SEEN]->(m)
                    RETURN type(r)""", username=username, movie_name = movie_name)
                
    def _create_actor_to_movie_relationship(self, actor_name, movie_name):
            with self.driver.session() as session:
                session.run("""
                    MATCH (a:Actor), (m:Movie)
                    WHERE a.actor_name=$actor_name AND m.movie_name=$movie_name
                    CREATE (a)-[r:ACTED_IN]->(m)
                    RETURN type(r)""", actor_name = actor_name, movie_name = movie_name)
                
    def _create_movie_to_category_relationship(self, movie_name, category_name):
            with self.driver.session() as session:
                session.run("""
                    MATCH (m:Movie), (c:Category)
                    WHERE m.movie_name=$movie_name AND c.category_name=$category_name
                    CREATE (m)-[r:BELONGS_IN]->(c)
                    RETURN type(r)""", movie_name = movie_name, category_name = category_name)
                
    def _create_user_to_category_relationship(self, username, category_name):
            with self.driver.session() as session:
                session.run("""
                    MATCH (u:User), (c:Category)
                    WHERE u.username=$username AND c.category_name=$category_name
                    CREATE (u)-[r:LIKES]->(c)
                    RETURN type(r)""", username = username, category_name = category_name)
                
    def _create_category_to_actor_relationship(self, category_name, actor_name):
            with self.driver.session() as session:
                session.run("""
                    MATCH (c:Category), (a:Actor)
                    WHERE c.category_name=$category_name AND a.actor_name=$actor_name
                    CREATE (a)-[r:LIKELY_TO_PARTICIPATE]->(c)
                    RETURN type(r)""", category_name = category_name, actor_name=actor_name)
                
    def _create_user_to_actor_relationship(self, username, actor_name):
            with self.driver.session() as session:
                session.run("""
                    MATCH (u:User), (a:Actor)
                    WHERE u.username=$username AND a.actor_name=$actor_name
                    CREATE (u)-[r:LIKES]->(a)
                    RETURN type(r)""", username=username, actor_name = actor_name)
                
        
    def init(self, source):
            with open(source, newline='') as csv_file:
                reader = csv.DictReader(csv_file,  delimiter='|')
                for r in reader:
                    self._create_user_node(r["username"], r["email"])
                    self._create_movie_node(r["movie_name"], r["movie_category"], r["movie_actor"])
                    self._create_actor_node( r["movie_actor"])
                    self._create_category_node( r["movie_category"])
                    self._create_user_to_movie_relationship(r["username"], r["movie_name"])
                    self._create_actor_to_movie_relationship(r["movie_actor"], r["movie_name"])
                    self._create_movie_to_category_relationship(r["movie_name"], r["movie_category"])
                    self._create_user_to_category_relationship(r["username"], r["movie_category"])
                    self._create_category_to_actor_relationship(r["movie_category"], r["movie_actor"])
                    self._create_user_to_actor_relationship(r["username"], r["movie_actor"])
            
            

if __name__ == "__main__":
    # Read connection env variables
    neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD', 'Patineta2000')

    netflix = Netflix(neo4j_uri, neo4j_user, neo4j_password)
    netflix.init("data/Data.csv")

    netflix.close()