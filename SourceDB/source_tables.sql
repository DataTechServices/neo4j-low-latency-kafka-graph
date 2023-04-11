show variables;

use mskdev;
drop procedure mskdev.add_msk_test_records;
DELIMITER $$
CREATE PROCEDURE mskdev.add_msk_test_records()
begin
declare  max_msk_id int ;
    select max(ue_id)+1 into max_msk_id
    from mskdev.cdc_msk_test;
    insert into mskdev.cdc_msk_test (  ue_id, ue_name, ue_count,
        cdc_modified_ts,
        cdc_status)
    values (max_msk_id,'test',max_msk_id+12,current_timestamp,'pending');
END    $$
DELIMITER ;

call mskdev.add_msk_test_records;

select count(*) from mskdev.cdc_msk_test;

select * from mskdev.cdc_msk_test;
alter event run_msk_cdc_5 enable;
alter event run_msk_cdc_5 disable;
drop  event if exists run_msk_cdc_5;
CREATE EVENT run_msk_cdc_5
    ON SCHEDULE EVERY 5 SECOND
      DO
        CALL mskdev.add_msk_test_records();