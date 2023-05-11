# NoSQL-proyect
# Install project python requirements
python3 -m pip install -r requirements.txt
```

### To load data
Ensure you have a running neo4j instance
i.e.:
```
docker run --name neo4j_leo --publish=7474:7474 --publish=7687:7687 neo4j
```
Run main.py
i.e.:
```
python3 main.py
```

## GDSL Workaround

```
docker cp gds/neo4j.conf neo4j:/var/lib/neo4j/conf/
docker cp gds/neo4j-graph-data-science-2.2.2.jar neo4j:/var/lib/neo4j/plugins/
docker restart neo4j
```