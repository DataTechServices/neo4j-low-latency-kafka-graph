AWS EC2 Client

<br>Testing Connectivity      
<br>curl http://localhost:7474/
<br>{
<br>"transaction" : "http://localhost:7474/db/{databaseName}/tx",
<br>"bolt_routing" : "neo4j://localhost:7687",
<br>"transaction" : "http://localhost:7474/db/{databaseName}/tx",
<br>"bolt_direct" : "bolt://localhost:7687",
<br>"neo4j_version" : "4.3.6",
<br>"neo4j_edition" : "community"
<br>}