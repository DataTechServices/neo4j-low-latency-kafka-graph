SELECT * FROM mskdev.cdc_msk_outbox;

select * from email_scratch limit 10;
drop table cdc_outbox;
CREATE TABLE cdc_outbox (
  id int NOT NULL AUTO_INCREMENT,
  category varchar(10) NOT NULL,
  sourceId varchar(30) NOT NULL,
  sourceName varchar(100) NOT NULL,
  targetId varchar(30) NOT NULL,
  targetName varchar(100) NOT NULL,
  eventdt datetime DEFAULT CURRENT_TIMESTAMP,
  relationshipType varchar(10) NOT NULL,
  node_properties varchar(150) ,
  subject_txt varchar(45) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY id_UNIQUE (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- insert into cdc_msk_outbox 
--        ( category,sourceId,   sourceName, targetId,  targetName,eventDt,relationshipType,cdc_status)
--      -- ,       'User',     subject,   'Email',   timestamp,'SENT','ACTIVE'
-- from mskdev.email_scratch;
insert into cdc_outbox(id,category, sourceId,   sourceName, targetId,  targetName, eventDt,
        relationshipType, node_properties, subject_txt)
        values(2,'email','sourceid','sname','tid','tname','2021-10-10', 'sent','x','sssubj');
        --
select  Id,category
        sourceId,
        from_user,
        targetId,
        to_user,
        sent_timestamp,
        'new' as relationshipType,
        'new2' as node_properties,
        subject_txt
from   mskdev.email_dts;

insert into cdc_outbox(id,category, sourceId,   sourceName
       )
select  Id,category
        sourceId,
        from_user
from   mskdev.email_dts;

select  category sourceId, from_user, targetId, to_user,
        sent_timestamp, 'SENT' as relationshipType, 'subject' as node_properties,
        subject_txt
from   mskdev.email_dts;

describe  cdc_outbox;

select category, sourceId,   sourceName, targetId,  targetName, eventdt, relationshipType, node_properties, subject_txt
from mskdev.cdc_outbox;
select  category
        sourceId,
        from_user,
        targetId,
        to_user,
        sent_timestamp,
        'SENT',
        '{subject:"xx",date:"2012-10-10"}' as node_properties,
        subject_txt
from   mskdev.email_dts;

truncate cdc_outbox;
truncate email_dts;
insert into cdc_outbox (category, sourceId,   sourceName, targetId,  targetName, 
        relationshipType1, relationshipType2 ,msg_id,   node_properties)
        select  'email',
        sourceId,
        from_user as sourceName,
        targetId as targetId,
        to_user as targetName,
        'SENT' as relationshipType1,
        'RECIEVED' as relationshipType2,
		msg_id as msg_id,
		node_properties
from   mskdev.email_dts
-- where from_user = 'damondrillsdtc@gmail.com';
where id > 1 ;

select * from mskdev.email_dts limit 100;

select sourceName,count(*) from mskdev.cdc_outbox group by sourceName;

select * from cdc_outbox ;
-- where sourceName is null or targetName is null or msg_id is null;

select * from mskdev.email_dts;

select from_user,count(*) from mskdev.email_dts group by from_user order by count(*) desc;


select * from email_dev;CREATE TABLE email_dev (
  Id int DEFAULT NULL,
  category text,
  sourceId int DEFAULT NULL,
  from text,
  targetId int DEFAULT NULL,
  to text,
  timestamp text,
  subject text,
  msg_id text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
