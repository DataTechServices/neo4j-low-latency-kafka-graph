
{"before":null,"after":{"id":4047,"category":"email","sourceId":"304","sourceName":"no-reply@accounts.go","targetId":"1","targetName":"owenr@dts5280.com","eventdt":1674323557000,"relationshipType":"SENT","node_properties":"{subject:\"2-Step Verification turned on\" , date:2023-01-21 17:52:37,msg_id:WuXi8mneCufjBvxy49RQ}","subject_txt":"2-Step Verification turned on"},"source":{"version":"1.8.1.Final","connector":"mysql","name":"mskdev_cdc","ts_ms":1674335539000,"snapshot":"false","db":"mskdev","sequence":null,"table":"cdc_outbox","server_id":1691652969,"gtid":null,"file":"mysql-bin-changelog.002073","pos":892312,"row":14,"thread":null,"query":null},"op":"c","ts_ms":1674335539556,"transaction":null}




// {"before":null,"after":{"id":4019,"category":"email","sourceId":"161","sourceName":"no-reply@experfy.com","targetId":"1","targetName":"owenr@dts5280.com","eventdt":1674085064000,"relationshipType":"SENT","node_properties":"{subject:\"xx\" , date:\"2012-10-10\"}","subject_txt":"New Opportunity in Your TalentCloud"},"source":{"version":"1.8.1.Final","connector":"mysql","name":"mskdev_cdc","ts_ms":1674333702000,"snapshot":"false","db":"mskdev","sequence":null,"table":"cdc_outbox","server_id":1691652969,"gtid":null,"file":"mysql-bin-changelog.002067","pos":1082783,"row":11,"thread":null,"query":null},"op":"c","ts_ms":1674333703042,"transaction":null}

WITH { event: [ 
{ before:' ', after: { id:25, category:"email", sourceId:"robeyrobey@gmail.com", sourceName:"User",
		targetId:"Gibson Jazz Party", targetName:"Email", eventDt:1446422400000, 
		relationshipType:"SENT", cdc_status:"ACTIVE", subject:' '},
	    source:{version:"1.8.1.Final", connector:"mysql", name:"mskdev_cdc", ts_ms:1674174806622,
		snapshot:"last", db:"mskdev", sequence:' ', table:"cdc_outbox", server_id:0, gtid:' ',
		file:"mysql-bin-changelog.001532", pos:457, row:0, thread:' ', query:' '},
		op:"r", ts_ms:1674174806622, transaction:' '
	}
] } as msg 
unwind msg.event as out_evt 
CALL {
 WITH out_evt 
 WITH out_evt
 WHERE ( out_evt.after.category  in ['email'] ) 
  MERGE (u:User {id:out_evt.after.sourceId}) remove  u.new 
  MERGE (e:Email {id:out_evt.after.targetId}) set e.eventDt=out_evt.after.eventDt
  MERGE(u)-[:SENT]->(e)
 RETURN 'ds-insupd: '+toString(count(*)) +":"+toString(out_evt.after.id) as type1 
}
return type1
;
match p=((u:User)-[r]->(e:Email)) return p;
// match(a:sourceName) return a;
// CALL {
//         WTIH out_evt
//         WTIH out_evt
//         WHERE (out_evt.after.category  in ['email'] )
//         MERGE (a:out_evt.after.sourceName {id:out_evt.after.id})
//         RETURN 'ds-insupd: '+toString(out_evt.after.id) as type1
// }
