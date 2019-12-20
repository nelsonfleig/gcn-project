# Jazz Knowledge Graph Creation

## Starting Point

This graph was created as an experimental jazz collaboration graph for Neo4J. Starting point was a graph derived from the MusicBrainz relational model (http://example-data.neo4j.org/3.4-datasets/musicbrainz.tgz)

The objective of the master project was to make link predictions on nodes. Specifically, we wanted to make predictions on collaborations between jazz musicians. The original graph was inadequate for this task.

Some of the problems in the original graph that needed resolving included:

1. Artist nodes lack genre information so it is not possible to filter out jazz musicians
2. There is no existing direct edge between artists that have worked together
3. There is no information about the country of birth nor if the artist is deceased

We approached a solution to these problems by downloading the complete MusicBrainz web application and running it in a Virtual Machine. This way we were able to run queries from Neo4J in order to supplement, i.e. "enrich" the data.
For this we used the MusicBrainz identifier (mbid) in order to match records in both databases. Below are some of the queries that were executed.


### Musicbrainz Info

Virtual box login information
user: vagrant
pw: vagrant

The following terminal command was used to connect to the PSQL instance running in the VM 
psql -h localhost -U musicbrainz -p 15432

Then authentified with the following credentials
user: musicbrainz
pw: musicbrainz

The JDBC driver for PostgreSQL had to be downloaded and loaded in Neo4J in order to run queries using the APOC library in Neo4J.

// neo4j.configuration PostgreSQL settings
JDBC Driver downloaded @ https://jdbc.postgresql.org/download.html -> version "9.4.1209 JDBC 42"
apoc.jdbc.myDB.url=jdbc:postgresql://localhost:15432/musicbrainz?user=musicbrainz&password=musicbrainz

### 1. Extracting Genre Information

The genre information regarding an artist was stored in the "artist_tag" table in PSQL. We used the following command to enrich the Neo4J-DB with a "jazz" attribute. This enables us to filter out musicians who are associated with the jazz genre. 

CALL apoc.load.jdbc('myDB',
"select DISTINCT a.gid from artist a inner join artist_tag at on a.id = at.artist inner join tag t on at.tag = t.id WHERE (t.name like '%jazz%' OR t.name like '%big band%') AND a.name NOT LIKE 'Various Artists'")
YIELD row
MATCH (a:Artist)
WHERE a.mbid = row.gid
SET a.genre = 'jazz'
RETURN a.name, a.genre



After some data analysis, we noticed that some well known jazz musicians did not contain the "jazz" tag in the PSQL-DB. We solved this by extending the "jazz" attribute to musicians that had collaborated on an album release.
This in effect propagated the "jazz" genre attribute to first neighbors

Match (a:Artist)-[:INSTRUMENT]->(r:Release)<-[:INSTRUMENT]-(other:Artist)
Where a.genre = 'jazz'
WITH collect(DISTINCT other.mbid) as other_mbids
UNWIND other_mbids as other_mbid
MATCH (a2:Artist)
WHERE a2.mbid = other_mbid
SET a2.genre = 'jazz'
RETURN COUNT(DISTINCT a2)


### 2. Linking jazz musicians who have collaborated on same album release

With the "jazz" attribute, we can create edges between jazz musicians who have collaborated in the same album release. 

// Creates relationships PLAYED_WITH between Jazz entities
MATCH (a:Artist)-[:INSTRUMENT]->(:Release)<-[:INSTRUMENT]-(other:Artist)
WHERE a.genre = 'jazz' 
WITH DISTINCT a, other
MERGE (a)-[r:PLAYED_WITH]-(other)
RETURN  count(DISTINCT r)

### 3. Enriching nodes with additional attributes.

In order to extract further information that may be useful to a Machine Learning model, we extracted additional information from the PSQL-DB like country, gender, and deceased.

// Enrich nodes with othe attributes
MATCH (a:Artist)
WITH COLLECT(a.mbid) AS ids
UNWIND ids AS id
CALL apoc.load.jdbc('myDB',
"select DISTINCT a.gid::text, ar.name as country, a.gender as gender, a.ended as ended FROM artist a INNER JOIN area ar on a.area = ar.id WHERE a.gid = UUID(?)", [id]) YIELD row
MATCH (a:Artist) WHERE a.mbid = row.gid 
SET a += {country: row.country, gender: row.gender, deceased: row.ended}
RETURN COUNT(a)

## Export and Import Process

Finally we exported the file to the cypher format in order to be uploaded to a cloud Neo4J-DB

// Exporting subgraph (RUN NEO4J-BROWSER AS ADMINISTRATOR!)
CALL apoc.export.cypher.query(
'MATCH (a1:Artist)-[r:PLAYED_WITH]->(a2:Artist) RETURN *',
'jazz.cypher',{format:'cypher-shell'});


### Loading to local Neo4J Graph
Execute the following commands from the bin folder of the DB instance

For example:
~/.Neo4jDesktop/neo4jDatabases/database-416596ed-0b5e-4444-934f-fcbc8f4366b0/installation-3.5.2/bin

Then execute the following:

cat ./jazz.cypher | ./cypher-shell.bat -u neo4j -p nelson


### Loading to Neo4J Remote Graph
from the same location as described above, you can connect to the cloud Neo4J instance by running the following

cat ./jazz.cypher | ./cypher-shell.bat -a bolt+routing://ea085e03.databases.neo4j.io:7687 -u nelson -p Chichapi198

