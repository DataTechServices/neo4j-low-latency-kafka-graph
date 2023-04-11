select category, sourceId,   sourceName, targetId,  targetName, eventDt, relationshipType, node_properties, subject_txt
from cdc_outbox;
insert into cdc_outbox (category, sourceId,   sourceName, targetId,  targetName, 
			eventDt, relationshipType, node_properties, subject_txt)   
select  category, sourceId, from_user, targetId, to_user,
        sent_timestamp, 'SENT' as relationshipType, 'subject' as node_properties,
        subject_txt
from   mskdev.email_dts;
select count(*) from mskdev.email_dts;
select from_user,count(*) from mskdev.email_dts group by from_user;
