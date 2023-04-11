match(a) detach delete a;
WITH {events: [{before:' ',after:{id:4043,category:"email",sourceId:"453",sourceName:"comments@facebookmai",targetId:"4",targetName:"owen@dts5280.com",eventdt:1674291397000,relationshipType:"SENT",node_properties:"{subject: 'owen, what do you think of these jobs?', msg_id: '20221019193655.c570fcbf7c4216c3', event_dt: '2022-10-19 19:36:55'}",subject_txt:"Alex Robertson commented on your post."},source:{version:"1.8.1.Final",connector:"mysql",name:"mskdev_cdc",ts_ms:1674335539000,snapshot:"false",db:"mskdev",sequence:' ',table:"cdc_outbox",server_id:1691652969,gtid:' ',file:"mysql-bin-changelog.002073",pos:892312,row:10,thread:' ',query:' '},op:"c",ts_ms:1674335539556,transaction:' '}
 ]} as msg  
unwind msg.events as evt_msg  
CALL {
 WITH evt_msg
 WITH evt_msg
 WHERE ( evt_msg.after.category  in ['email'] ) 
  MERGE (from:User {id:evt_msg.after.sourceId}) set from.useremail = evt_msg.after.sourceName
  MERGE (to:User {id:evt_msg.after.targetId}) set to.useremail = evt_msg.after.targetName
  MERGE (e:Email {id:evt_msg.after.targetId}) on create set e = apoc.convert.fromJsonMap(evt_msg.after.node_properties)
  MERGE(from)-[:SENT]->(e)
  MERGE(e)-[:RECEIVED]->(to)
 RETURN 'insupd: '+toString(count(*)) +":"+toString(evt_msg.after.id) as type1 
}
return type1
;
match p=((u:User)-[r]->(e:Email)) return p;
//   MERGE (e:Email {id:out_evt.after.targetId}) set e = {subject:'Alex Robertson commented on your post.' , date:'2023-01-21 08:56:37',msg_id:'916b008299ac11ed92711597f0c77c3f'}
// match(a:sourceName) return a;
// CALL {
//         WTIH out_evt
//         WTIH out_evt
//         WHERE (out_evt.after.category  in ['email'] )
//         MERGE (a:out_evt.after.sourceName {id:out_evt.after.id})
//         RETURN 'ds-insupd: '+toString(out_evt.after.id) as type1
// }
// { 'subject': 'owen, you have the right experience for this job.', 
	'msg_id': '20221228163833.df4b0afa663e9dcc', 'event_dt': datetime.datetime(2022, 12, 28, 16, 38, 33)}
