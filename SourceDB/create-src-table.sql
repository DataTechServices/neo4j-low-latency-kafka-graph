use mskdev;
drop table cdc_msk_test;

CREATE TABLE `cdc_msk_test` (
                                `id` int(11) NOT NULL AUTO_INCREMENT,
                                `ue_id` int(11) NOT NULL,
                                `ue_name` varchar(30) NOT NULL,
                                `ue_count` int(11) DEFAULT NULL,
                                `cdc_modified_ts` datetime DEFAULT CURRENT_TIMESTAMP,
                                `cdc_status` varchar(15) DEFAULT NULL,
                                PRIMARY KEY (`id`),
                                UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3763 DEFAULT CHARSET=utf8;

insert into cdc_msk_test (  ue_id, ue_name, ue_count, cdc_modified_ts, cdc_status)
values (3,'test',12,current_timestamp,'pending');

select * from cdc_msk_test;

