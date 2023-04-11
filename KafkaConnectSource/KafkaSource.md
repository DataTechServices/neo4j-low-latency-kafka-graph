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
"acks": "1",<br>
"column.include.list": " mskdev.cdc_msk_test.id, mskdev.cdc_msk_test.ue_id, mskdev.cdc_msk_test.ue_name, mskdev.cdc_msk_test.ue_count, mskdev.cdc_msk_test.cdc_modified_ts, mskdev.cdc_msk_test.cdc_status",<br>
"connector.class": "io.debezium.connector.mysql.MySqlConnector",<br>
"database.history.kafka.bootstrap.servers": "b-1.redacted.leit85.c6.kafka.us-east-2.amazonaws.com:9092,b-2.redacted.leit85.c6.kafka.us-east-2.amazonaws.com:9092",<br>
"database.history.kafka.topic": "mskdcdc_history",<br>
"database.history.store.only.captured.tables.ddl": "true",<br>
"database.hostname": "dts-aws-msk.redacted.us-east-2.rds.amazonaws.com",<br>
"database.include.list": "mskdev",<br>
"database.port": "3306",<br>
"database.server.id": "redacted",<br>
"database.server.name": "mskdev_cdc",<br>
"database.user": "admin",<br>
"database.password": "redacted",<br>
"database.whitelist": "mskdev",<br>
"errors.log.enable": "true",<br>
"errors.log.include.messages": "true",<br>
"errors.retry.delay.max.ms": "10000",<br>
"errors.retry.timeout": "-1",<br>
"errors.tolerance": "all",<br>
"include.schema.changes": "false",<br>
"key.converter": "org.apache.kafka.connect.storage.StringConverter",<br>
"key.converter.schemas.enable": "false",<br>
"value.converter": "org.apache.kafka.connect.json.JsonConverter",<br>
"value.converter.schemas.enable": "false",<br>
"linger.ms": "30",<br>
"max.batch.size": "10001",<br>
"max.poll.records": "10000",<br>
"max.queue.size": "20000",<br>
"poll.interval.ms": "50",<br>
"reconnect.backoff.max.ms": "1000",<br>
"reconnect.backoff.ms": "50",<br>
"request.timeout.ms": "120000",<br>
"retries": "5",<br>
"retry.backoff.ms": "100",<br>
"snapshot.mode": "when_needed",<br>
"table.ignore.builtin": "true",<br>
"table.include.list": "mskdev.cdc_msk_test",<br>
"tasks.max": "1",<br>
"topic.creation.default.cleanup.policy": "compact",<br>
"topic.creation.default.compression.type": "lz4",<br>
"topic.creation.default.partitions": "1",<br>
"topic.creation.default.replication.factor": "2",<br>
"transforms": "topicname,route",<br>
"transforms.route.language": "jsr223.groovy",<br>
"transforms.route.topic.expression": "(value.op in ['c','u','d'] )   ? topic : null",<br>
"transforms.route.type": "io.debezium.transforms.ContentBasedRouter",<br>
"transforms.topicname.regex": "([^.]+)\\.([^.]+)\\.([^.]+)",<br>
"transforms.topicname.replacement": "msk_$3",<br>
"transforms.topicname.type": "org.apache.kafka.connect.transforms.RegexRouter"<br>
}<br>
