### Kafka Connect Source Connector
The Kafka Connect Source Connector configuration contains the MSK Connect environment and debezium plugin parameters that are responsible for reading the source MySQL database transaction logs (binlog) and submit these events to the MSK Kafka Brokers. The json configuration file for a Connector contains the specifics about a given connector such as the address of database and tables/columns to read as well as transformations or filtering, along with operational aspects that inform debezium on batching, errors, etc.  In addition the configuration specifies the  AWS/MSK the following component aspects:<br>
1) Logging - Contains the associated S3 buckets and/or CloudWatch logGroup
2) MSK Cluster - That will receive the Kafka Connect events and includes associated subnets and security groups for MSK
3) IAM / Role credentials - That have permissions on the associated resources. 
4) Capacity Configuration - Specifying resource scaling and initial provisioning (note debezium/MySQL can only have 1 task)
5) Plugin - Idnetifies the ARN of the created plugin (See Plugins documentation)
6) Worker Configuration - Identifies the Worker ARN (Note worker specifies a persistent consumer-offset topic necessary for restartability.)
7) debezium connectorConfiguration - This represents the core logic of the Kafka Connect process and described in more detail below.  

<br>This example looks at the key components of an AWS/MSK configuration,namely





### Example debezium connectorConfiguration
<br> {
<br>   "connectorConfiguration": {
<br>     "connector.class": "io.debezium.connector.mysql.MySqlConnector",
<br>     "key.converter": "org.apache.kafka.connect.storage.StringConverter",
<br>     "value.converter": "org.apache.kafka.connect.json.JsonConverter",
<br>     "// Errors":  "Ensure creation and running connectors write errors to cloud watch.",
<br>     "errors.log.include.messages": "true",
<br>     "errors.log.enable": "true",
<br>     "// Credentials":  "Access secrets manager for MySQL credentials; Worker must be configured with SecMgr libs.",
<br>     "database.user": "${secretManager:}",
<br>     "database.password": "${secretManager:}",
<br>     "// Transforms":  "Use SMT/content filtering exclude messages based upon values.",
<br>     "// Transforms": "Route is one technique for routing the incoming event to a new topic name",
<br>     "transforms": "topicname,route",
<br>     "transforms.route.language": "jsr223.groovy",
<br>     "transforms.route.type": "io.debezium.transforms.ContentBasedRouter",
<br>     "transforms.route.topic.expression": "(value.op in ['c','u','d'] )   ? topic : null ",
<br>     "transforms.topicname.type": "org.apache.kafka.connect.transforms.RegexRouter",
<br>     "transforms.topicname.replacement": "int_$3",
<br>     "transforms.topicname.regex": "([^.]+)\\.([^.]+)\\.([^.]+)",
<br>     "// Default Topic Parameters":  "Topics maybe pre-created to automatically so, e.g. new tables may generate new topics",
<br>     "topic.creation.default.partitions": "1",
<br>     "topic.creation.default.compression.type": "lz4",
<br>     "topic.creation.default.replication.factor": "3",
<br>     "// AWS/MSK Brokers ":  "Provide the list of brokers,",
<br>     "database.history.kafka.bootstrap.servers": "<bootstrap server list>:9092",
<br>     "// Polling ":  "Number of records or bytes to return from the poll() call/Time between polling",
<br>     "max.poll.records": "10000",
<br>     "max.batch.size": "10001",
<br>     "poll.interval.ms": "50",
<br>     "// Topic Replicas ":  "When confirmation of write to the topic is confirmed (leader and/or additional replicas)",
<br>     "acks": "1",
<br>     "// Scalability ":  "For Source Connectors to MySQL only 1 connector thread can read the binlog at a time.",
<br>     "tasks.max": "1",
<br>     "// Database Server Info": "Server Connectivity Information",
<br>     "database.server.id": "XXXXXXXXX",
<br>     "database.server.name": "<connector db server name>",
<br>     "database.port": "3306",
<br>     "database.hostname": "<hostname/ip address>",
<br>     "// Database Table/Column Selection": "Allows for only specific tables to be selected for Kafka topics",
<br>     "database.whitelist": "<mysql schema name>",
<br>     "database.include.list": "<mysql schema name>",
<br>     "table.include.list": "<mysql schema name>.<table name>, <mysql schema name>.<table name2>,etc ",
<br>     "column.include.list": "<mysql schema name>.<table name1>.<column name>, <mysql schema name>.<table name1>.<column name>,<et al>  ,
<br>
<br>   "connectorName": "debezium-src-mysql",
<br>   "// No Auto Scaling for Debezium Connector ":  "Only one reader of the binlog at a time",
<br>   "capacity": {
<br>     "provisionedCapacity": {
<br>       "mcuCount": 1,
<br>       "workerCount": 1
<br>     }
<br>   },
<br>   "kafkaCluster": {
<br>     "apacheKafkaCluster": {
<br>       "bootstrapServers": "<msk-cluster-server-id1>:9092,<msk-cluster-server-id1>:9092,<msk-cluster-server-id1>9092",
<br>       "vpc": {
<br>         "securityGroups": [
<br>           "secgrp-xxxx"
<br>         ],
<br>         "subnets": [
<br>           "subnet-1",
<br>           "subnet-2"
<br>         ]
<br>       }
<br>     }
<br>   },
<br>   "//Encryption :":"Adding encryption between MySQL and the AWS/MSK Cluster",
<br>   "kafkaClusterClientAuthentication": {
<br>     "authenticationType": "NONE"
<br>   },
<br>   "//Intra Cluster Encryption :":"Adding encryption between the AWS/MSK Cluster Hosts",
<br>     "kafkaClusterEncryptionInTransit": {
<br>     "encryptionType": "PLAINTEXT"
<br>   },
<br>   "kafkaConnectVersion": "2.7.1",
<br>   "logDelivery": {
<br>     "workerLogDelivery": {
<br>       "cloudWatchLogs": {
<br>         "enabled": true,
<br>         "logGroup": "<msk-sink>/debezium-src-connector"
<br>       }
<br>     }
<br>   },
<br>   "plugins": [
<br>     {
<br>       "customPlugin": {
<br>         "// Debezium Plugin zip file":"Pre-constructed zip is feature dependant and critical see plugin doc",
<br>         "customPluginArn": "<arn of the S3 location of debezium plugin package>",
<br>         "revision": 1
<br>       }
<br>     }
<br>   ],
<br>   "serviceExecutionRoleArn": "<arn of assigned role with access to identified resources>",
<br>   "workerConfiguration": {
<br>     "revision": 1,
<br>     "// Worker Config": "Provides configuration of the Worker JVM that runs the Kafka Connector",
<br>     "workerConfigurationArn": "arn:aws:<redacted worker arn>:worker-configuration/<redacted worker arn>-offset/134143141-2"
<br>   }
<br> }