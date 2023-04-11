WITH {events: [{before:' ',after:{id:4043,category:"email",sourceId:"453",sourceName:"comments@facebookmai",targetId:"4",targetName:"owen@dts5280.com",eventdt:1674291397000,relationshipType:"SENT",node_properties:"{subject:\'Alex Robertson commented on your post.\' , date:'2023-01-21 08:56:37',msg_id:'916b008299ac11ed92711597f0c77c3f'}",subject_txt:"Alex Robertson commented on your post."},source:{version:"1.8.1.Final",connector:"mysql",name:"mskdev_cdc",ts_ms:1674335539000,snapshot:"false",db:"mskdev",sequence:' ',table:"cdc_outbox",server_id:1691652969,gtid:' ',file:"mysql-bin-changelog.002073",pos:892312,row:10,thread:' ',query:' '},op:"c",ts_ms:1674335539556,transaction:' '}
 ]} as msg  
unwind msg.events as out_evt  
WITH out_evt,apoc.convert.fromJsonMap(out_evt.after.node_properties) as map
WITH out_evt,apoc.convert.fromJsonMap(out_evt.after.node_properties) as map
CALL {
 WITH out_evt,map
 WITH out_evt,map
 WHERE ( out_evt.after.category  in ['email'] ) 
  MERGE (u:User {id:out_evt.after.sourceId}) set u.useremail = out_evt.after.sourceName
  MERGE (e:Email {id:out_evt.after.targetId}) set e = map
  MERGE(u)-[:SENT]->(e)
 RETURN 'ds-insupd: '+toString(count(*)) +":"+toString(out_evt.after.id) as type1 
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
