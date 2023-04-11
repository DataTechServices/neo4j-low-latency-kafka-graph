WITH event as evt_msg 
CALL { 
WITH evt_msg 
WITH evt_msg 
WHERE ( evt_msg.after.category IN ['email'] ) 
MERGE (from:User {id:evt_msg.after.sourceId}) 
SET from.useremail = evt_msg.after.sourceName 
MERGE (to:User {id:evt_msg.after.targetId}) 
SET to.useremail = evt_msg.after.targetName MERGE (e:Email {id:evt_msg.after.msg_id}) ON create SET e = apoc.convert.fromJsonMap(evt_msg.after.node_properties) MERGE(from)-[:SENT]->(e) MERGE(e)-[:RECEIVED]->(to) RETURN 'insupd: '+toString(count(*)) +":"+toString(evt_msg.after.id) as type1 } return type1
