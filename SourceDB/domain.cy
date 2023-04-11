match(a:User)  with a, split(a.id,"@")[1] as emailaddr 
with a, emailaddr where not emailaddr is null
MERGE (d:Domain {id:emailaddr})
MERGE (d)-[:DOMAINED]->(a) return count(*);
