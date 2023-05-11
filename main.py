import csv
import os

from neo4j import GraphDatabase,Record
from neo4j.exceptions import ConstraintError

class Flight_data(object):
    def __init__(self, uri, user, password):
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self._create_constraints()

    def close(self):
        self.driver.close()

    def _create_constraints(self):
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT unique_airline IF NOT EXISTS FOR (a:Airline) REQUIRE a.airline_name IS UNIQUE")
            session.run("CREATE CONSTRAINT unique_destiny IF NOT EXISTS FOR (d:Destiny) REQUIRE d.destiny_name IS UNIQUE")
            session.run("CREATE CONSTRAINT unique_origin IF NOT EXISTS FOR (o:Origin) REQUIRE o.origin_name IS UNIQUE")
            session.run("CREATE CONSTRAINT unique_reason IF NOT EXISTS FOR (r:Reason) REQUIRE r.reason_name IS UNIQUE")
            session.run("CREATE CONSTRAINT unique_stay IF NOT EXISTS FOR (s:Stay) REQUIRE s.stay_name IS UNIQUE")
            session.run("CREATE CONSTRAINT unique_transit IF NOT EXISTS FOR (t:Transit) REQUIRE t.transit_name IS UNIQUE")
    
    def _create_user_node(self, username, age, gender):
        with self.driver.session() as session:
            try:
                session.run("CREATE (u:User {username: $username, age: $age, gender: $gender})", username = username, age = age, gender = gender )
            except ConstraintError:
                pass
    
    def _create_airline_node(self, airline_name):
        with self.driver.session() as session:
            try:
                session.run("CREATE (a:Airline {airline_name: $airline_name})", airline_name = airline_name)
            except ConstraintError:
                pass
    
    def _create_destiny_node(self, destiny_name):
        with self.driver.session() as session:
            try:
                session.run("CREATE (d:Destiny {destiny_name: $destiny_name})", destiny_name = destiny_name)
            except ConstraintError:
                pass

    def _create_origin_node(self, origin_name):
        with self.driver.session() as session:
            try:
                session.run("CREATE (o:Origin {origin_name: $origin_name})", origin_name = origin_name)
            except ConstraintError:
                pass

    def _create_reason_node(self, reason_name):
        with self.driver.session() as session:
            try:
                session.run("CREATE (r:Reason {reason_name: $reason_name})", reason_name = reason_name)
            except ConstraintError:
                pass
        
    def _create_stay_node(self, stay_name):
        with self.driver.session() as session:
            try:
                session.run("CREATE (s:Stay {stay_name: $stay_name})", stay_name = stay_name)
            except ConstraintError:
                pass

    def _create_transit_node(self, transit_name):
        with self.driver.session() as session:
            try:
                session.run("CREATE (t:Transit {transit_name: $transit_name})", transit_name = transit_name)
            except ConstraintError:
                pass
    
    def _create_flight_node(self, flight_id,airline_name, origin_name, destiny_name, day, month, year):
        with self.driver.session() as session:
            try:
                session.run("CREATE (f:Flight {flight_id:$flight_id, airline_name: $airline_name, origin_name:$origin_name, destiny_name:$destiny_name, day:$day, month:$month, year:$year})", flight_id=flight_id, airline_name=airline_name, origin_name=origin_name, destiny_name=destiny_name, day=day, month=month, year=year)
            except ConstraintError:
                pass

    def _create_HasFlight_relationship(self, flight_id, airline_name):
        with self.driver.session() as session:
            session.run("""
                MATCH (f:Flight), (a:Airline)
                WHERE f.flight_id=$flight_id AND a.airline_name=$airline_name
                CREATE (a)-[:HAS_FLIGHT]->(f)
            """, flight_id=flight_id, airline_name=airline_name)

    def _create_FROM_relationship(self, flight_id, origin_name):
        with self.driver.session() as session:
            session.run("""
                MATCH (f:Flight), (o:Origin)
                WHERE f.flight_id=$flight_id AND o.origin_name=$origin_name
                CREATE (f)-[:FROM]->(o)
            """, flight_id=flight_id, origin_name=origin_name)

    def _create_TO_relationship(self, flight_id, destiny_name):
        with self.driver.session() as session:
            session.run("""
                MATCH (f:Flight), (d:Destiny)
                WHERE f.flight_id=$flight_id AND d.destiny_name=$destiny_name
                CREATE (f)-[:TO]->(d)
            """, flight_id=flight_id, destiny_name=destiny_name)
    
    def _create_HasPassenger_relationship(self, flight_id, username):
        with self.driver.session() as session:
            session.run("""
                MATCH (u:User), (f:Flight) 
                WHERE u.username=$username AND f.flight_id=$flight_id
                CREATE (f)-[:HAS_PASSENGER]->(u)
            """, flight_id=flight_id, username=username)
    
    def _create_HasReason_relationship(self, username, reason_name):
        with self.driver.session() as session:
            session.run("""
                MATCH (u:User), (r:Reason) 
                WHERE u.username=$username AND r.reason_name=$reason_name
                CREATE (u)-[:HAS_REASON]->(r)
            """, username=username, reason_name=reason_name)

    def _create_HasStay_relationship(self, username, stay_name):
        with self.driver.session() as session:
            session.run("""
                MATCH (u:User),(s:Stay) 
                WHERE u.username=$username AND s.stay_name=$stay_name
                CREATE (u)-[:HAS_STAY]->(s)
            """, username=username, stay_name=stay_name)
    
    def _create_HasTransit_relationship(self, username, transit_name):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:User), (t:Transit)
                WHERE u.username=$username AND t.transit_name=$transit_name
                CREATE (u)-[:HAS_TRANSIT]->(t)
            """, username=username, transit_name=transit_name)
    
    def get_destinations_with_most_flights(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (f:Flight)-[:TO]->(d:Destiny)
                RETURN d.destiny_name, count(f) AS flight_count
                ORDER BY flight_count DESC
            """) 
            print(f"Los mejores aeropuertos para construir restaurantes son en las siguientes ciudades:\n")
            for record in result:
                destiny_name = record["d.destiny_name"]
                flight_count = record["flight_count"]
                print(f"Destiny: {destiny_name}, Flight Count: {flight_count}") 

    def get_destinations_popular_vacation(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (r:Reason)<-[:HAS_REASON]-(u:User)<-[:HAS_PASSENGER]-(f:Flight)-[:TO]->(d:Destiny)
                WHERE r.reason_name = 'On vacation/Pleasure'
                RETURN d.destiny_name, count(u) AS passenger_count
                ORDER BY passenger_count DESC
            """)
            print(f"Estas son las ciudades donde es mas conveniente construir hoteles familiares y la cantidad de pasajeros que viajaron a ese destino con este motivo\n")
            for record in result:
                destiny_name = record["d.destiny_name"]
                passenger_count = record["passenger_count"]
                print(f"Destino: {destiny_name}, Cantidad de pasajeros: {passenger_count}")

    def get_destinations_popular_business(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (r:Reason)<-[:HAS_REASON]-(u:User)<-[:HAS_PASSENGER]-(f:Flight)-[:TO]->(d:Destiny)
                WHERE r.reason_name = 'Business/Work'
                RETURN d.destiny_name, count(u) AS passenger_count
                ORDER BY passenger_count DESC
            """)
            print(f"Estas son las ciudades donde es mas conveniente construir hoteles de negocios y la cantidad de pasajeros que viajaron a ese destino con este motivo\n")
            for record in result:
                destiny_name = record["d.destiny_name"]
                passenger_count = record["passenger_count"]
                print(f"Destino: {destiny_name}, Cantidad de pasajeros: {passenger_count}")

    
        
    def init(self, source):
            with open(source, newline='') as csv_file:
                reader = csv.DictReader(csv_file,  delimiter=',')
                for r in reader:
                    self._create_user_node(r["username"], r["age"], r["gender"])
                    self._create_airline_node(r["airline"])
                    self._create_origin_node( r["from"])
                    self._create_destiny_node( r["to"])
                    self._create_reason_node( r["reason"])
                    self._create_stay_node( r["stay"])
                    self._create_transit_node( r["transit"])
                    self._create_flight_node( r["id"], r["airline"], r["from"], r["to"], r["day"], r["month"], ["year"])
                    self._create_HasFlight_relationship(r["id"], r["airline"])
                    self._create_FROM_relationship(r["id"], r["from"])
                    self._create_TO_relationship(r["id"], r["to"])
                    self._create_HasPassenger_relationship(r["id"], r["username"])
                    self._create_HasReason_relationship(r["username"], r["reason"])
                    self._create_HasStay_relationship(r["username"], r["stay"])
                    self._create_HasTransit_relationship(r["username"], r["transit"])
    
            
            

if __name__ == "__main__":
    # Read connection env variables
    neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD', 'proyectoFinal')

    flight_data = Flight_data(neo4j_uri, neo4j_user, neo4j_password)
    flight_data.init("./flight_passengers.csv")
    flight_data.get_destinations_with_most_flights()
    flight_data.get_destinations_popular_business()
    flight_data.get_destinations_popular_vacation()
    flight_data.close()