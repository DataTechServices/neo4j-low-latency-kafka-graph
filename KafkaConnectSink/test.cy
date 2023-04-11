WITH { 
event: [
{before:' ',after:{id:3794,ue_id:417,ue_name:"test",ue_count:429,cdc_modified_ts:1673989998000,cdc_status:"pending"},source:{version:"1.8.1.Final",connector:"mysql",name:"mskdev_cdc",ts_ms:1673989998000,snapshot:"false",db:"mskdev",sequence:' ',table:"cdc_msk_test",server_id:1691652969,gtid:' ',file:"mysql-bin-changelog.000911",pos:1185,row:0,thread:' ',query:' '},op:"c",ts_ms:1673989998683,transaction:' '},
{before:' ',after:{id:3795,ue_id:418,ue_name:"test",ue_count:430,cdc_modified_ts:1673990003000,cdc_status:"pending"},source:{version:"1.8.1.Final",connector:"mysql",name:"mskdev_cdc",ts_ms:1673990003000,snapshot:"false",db:"mskdev",sequence:' ',table:"cdc_msk_test",server_id:1691652969,gtid:' ',file:"mysql-bin-changelog.000911",pos:1516,row:0,thread:' ',query:' '},op:"c",ts_ms:1673990003688,transaction:' '},
{before:' ',after:{id:3796,ue_id:419,ue_name:"test",ue_count:431,cdc_modified_ts:1673990008000,cdc_status:"pending"},source:{version:"1.8.1.Final",connector:"mysql",name:"mskdev_cdc",ts_ms:1673990008000,snapshot:"false",db:"mskdev",sequence:' ',table:"cdc_msk_test",server_id:1691652969,gtid:' ',file:"mysql-bin-changelog.000911",pos:1847,row:0,thread:' ',query:' '},op:"c",ts_ms:1673990008688,transaction:' '},
{before:' ',after:{id:3797,ue_id:420,ue_name:"test",ue_count:432,cdc_modified_ts:1673990013000,cdc_status:"pending"},source:{version:"1.8.1.Final",connector:"mysql",name:"mskdev_cdc",ts_ms:1673990013000,snapshot:"false",db:"mskdev",sequence:' ',table:"cdc_msk_test",server_id:1691652969,gtid:' ',file:"mysql-bin-changelog.000911",pos:2178,row:0,thread:' ',query:' '},op:"c",ts_ms:1673990013690,transaction:' '}
]
} as msg 
unwind msg.event as etest 
return etest.after.id
;
