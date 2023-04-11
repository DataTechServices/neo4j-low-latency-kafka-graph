-- drop table if exists mskdev.email_dts;
--  Id|category|sourceId|from_user|targetId|to_user|msg_id|node_properties
-- select 'dropped table';
-- CREATE TABLE mskdev.email_dts ( id int not NULL, category varchar(30), sourceId int DEFAULT NULL,
--   from_user varchar(50), targetId int DEFAULT NULL, to_user varchar(50), msg_id varchar(100),
--   node_properties varchar(500), PRIMARY KEY (id), UNIQUE KEY id_UNIQUE (id)) ENGINE=InnoDB AUTO_INCREMENT=1 ;
-- select 'create table';
--
-- LOAD DATA local INFILE 'email_dts.csv' 
-- LOAD DATA local INFILE 'email_orob.csv' 
truncate table mskdev.email_dts;
select 'loading table';
LOAD DATA local INFILE 'email_orob.csv' 
INTO TABLE mskdev.email_dts 
FIELDS TERMINATED BY '|' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
select 'loaded';
select from_user,count(*) from mskdev.email_dts group by from_user;
select count(*) from mskdev.email_dts;


-- Id|category|sourceId|from_user|targetId|to_user|sent_timestamp|subject_txt|msg_id
