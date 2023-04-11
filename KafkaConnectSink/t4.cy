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
  CALL apoc.create.nodes(out_evt.after.sourceName, $properties )
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
