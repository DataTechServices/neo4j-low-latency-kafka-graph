### Kafka Source Connector
The Source Connector configuration contains generic kafka Connect features along with debezium plugin libraries that are responsible for reading the source MySQL database transaction logs (binlogs) and submit these events to the Kafka Cluster.  The AWS/MSK use vendor specific plugin libraries for reading the proprietary formats of the source database transaction logs at configurable polling intervals (<1/sec) and capture relevant changes in batch.
This example looks at the key components of an AWS/MSK configuration,namely

Debezium Plugin
The current demo configuration uses several additional libraries for performing groovy scripting in support of SMT (message routing/filtering) as well as AWS Secrets Manager implementation.


####Debezium connector for MySQL Documentation
-   https://debezium.io/documentation/reference/stable/connectors/mysql.html

MySQL DB parameter settings.


Partitioning
While the default partitioning strategy is round-robin, it is possible to manually define the partition keys to alleviate dead-lock situations however it is higly dependant on your graph data model and the batch size of the Kafka Sink transactions.   
https://debezium.io/documentation/reference/stable/connectors/mysql.html#mysql-property-message-key-columns
## Example debezium configuration
"acks": "1",
"column.include.list": " mskdev.cdc_msk_test.id, mskdev.cdc_msk_test.ue_id, mskdev.cdc_msk_test.ue_name, mskdev.cdc_msk_test.ue_count, mskdev.cdc_msk_test.cdc_modified_ts, mskdev.cdc_msk_test.cdc_status",
"connector.class": "io.debezium.connector.mysql.MySqlConnector",
"database.history.kafka.bootstrap.servers": "b-1.redacted.leit85.c6.kafka.us-east-2.amazonaws.com:9092,b-2.redacted.leit85.c6.kafka.us-east-2.amazonaws.com:9092",
"database.history.kafka.topic": "mskdcdc_history",
"database.history.store.only.captured.tables.ddl": "true",
"database.hostname": "dts-aws-msk.redacted.us-east-2.rds.amazonaws.com",
"database.include.list": "mskdev",
"database.port": "3306",
"database.server.id": "redacted",
"database.server.name": "mskdev_cdc",
"database.user": "admin",
"database.password": "redacted",
"database.whitelist": "mskdev",
"errors.log.enable": "true",
"errors.log.include.messages": "true",
"errors.retry.delay.max.ms": "10000",
"errors.retry.timeout": "-1",
"errors.tolerance": "all",
"include.schema.changes": "false",
"key.converter": "org.apache.kafka.connect.storage.StringConverter",
"key.converter.schemas.enable": "false",
"value.converter": "org.apache.kafka.connect.json.JsonConverter",
"value.converter.schemas.enable": "false",
"linger.ms": "30",
"max.batch.size": "10001",
"max.poll.records": "10000",
"max.queue.size": "20000",
"poll.interval.ms": "50",
"reconnect.backoff.max.ms": "1000",
"reconnect.backoff.ms": "50",
"request.timeout.ms": "120000",
"retries": "5",
"retry.backoff.ms": "100",
"snapshot.mode": "when_needed",
"table.ignore.builtin": "true",
"table.include.list": "mskdev.cdc_msk_test",
"tasks.max": "1",
"topic.creation.default.cleanup.policy": "compact",
"topic.creation.default.compression.type": "lz4",
"topic.creation.default.partitions": "1",
"topic.creation.default.replication.factor": "2",
"transforms": "topicname,route",
"transforms.route.language": "jsr223.groovy",
"transforms.route.topic.expression": "(value.op in ['c','u','d'] )   ? topic : null",
"transforms.route.type": "io.debezium.transforms.ContentBasedRouter",
"transforms.topicname.regex": "([^.]+)\\.([^.]+)\\.([^.]+)",
"transforms.topicname.replacement": "msk_$3",
"transforms.topicname.type": "org.apache.kafka.connect.transforms.RegexRouter"
}