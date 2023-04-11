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
	WTIH out_evt
	WTIH out_evt
	WHERE (out_evt.after.category  in ['email'] ) 
	MERGE (a:out_evt.after.sourceName {id:out_evt.after.id})
	RETURN 'ds-insupd: '+toString(out_evt.after.id) as type1 
}
)

return etest;


WITH event as evt_msg 
CALL { 
	WITH evt_msg 
	WITH evt_msg 
	WHERE (evt_msg.op in ['c','u'] and evt_msg.after.inactive_flg <> 'Y' and toInteger(evt_msg.after.author_id) >0 ) 
	MERGE(r:Researcher {researcherId: coalesce(evt_msg.after.res_id,0)}) 
	SET r.customerId=coalesce(evt_msg.after.home_inst_id,0), r.version=evt_msg.after.version 
	WITH r,evt_msg 
	MATCH(p:Person {personId: toInteger(evt_msg.after.author_id)}) 
	WITH r,p 
	MERGE (r)-[:ALIAS]->(p) 
	RETURN 'ds-insupd: '+toString(count(*)) as type1 
	UNION 
	WITH evt_msg 
	WITH evt_msg 
	WHERE ((evt_msg.op in ['c','u'] and evt_msg.after.inactive_flg <> 'Y') and (evt_msg.after.author_id is null or toInteger(evt_msg.after.author_id) = 0)) 
	MERGE(r:Researcher {researcherId: coalesce(evt_msg.after.res_id,0)}) 
	SET r.customerId=coalesce(evt_msg.after.home_inst_id,0), r.version=evt_msg.after.version 
	WITH r,evt_msg 
	MATCH(r)-[rrx:ALIAS]->(pp:Person) 
	DELETE rrx 
	RETURN 'ds-insupd: '+toString(count(*)) as type1 
	UNION 
	WITH evt_msg   
	WITH evt_msg 
	WHERE (evt_msg.op in ['d'] and evt_msg.before.res_id > 0 ) 
	MATCH(r:Researcher {researcherId: coalesce(evt_msg.before.res_id,0)}) 
	DETACH 
	DELETE r 
	RETURN 'ds-delete: '+toString(count(*)) as type1 } 
	RETURN evt_msg.op,evt_msg.ts_ms,type1",
