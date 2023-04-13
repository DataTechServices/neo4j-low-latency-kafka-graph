### Kafka Connect Source Connector
The Kafka Connect Source Connector configuration contains the MSK Connect environment and debezium plugin parameters that are responsible for reading the source MySQL database transaction logs (binlog) and submit these events to the MSK Kafka Brokers. The json configuration file for a Connector contains the specifics about a given connector such as the address of database and tables/columns to read as well as transformations or filtering, along with operational aspects that inform debezium on batching, errors, etc.  In addition the configuration specifies the  AWS/MSK the following component aspects:<br>
1) Logging - Contains the associated S3 buckets and/or CloudWatch logGroup
2) MSK Cluster - That will receive the Kafka Connect events and includes associated subnets and security groups for MSK
3) IAM / Role credentials - That have permissions on the associated resources. 
4) Capacity Configuration - Specifying resource scaling and initial provisioning (note debezium/MySQL can only have 1 task)
5) Plugin - Idnetifies the ARN of the created plugin (See Plugins documentation)
6) Worker Configuration - Identifies the Worker ARN (Note worker specifies a persistent consumer-offset topic necessary for restartability.)
7) debezium connectorConfiguration - This represents the core logic of the Kafka Connect process and described in more detail below.  

 This example looks at the key components of an AWS/MSK configuration,namely





### Example debezium connectorConfiguration
```json
  {
    "connectorConfiguration": {
      "connector.class": "io.debezium.connector.mysql.MySqlConnector",
      "key.converter": "org.apache.kafka.connect.storage.StringConverter",
      "value.converter": "org.apache.kafka.connect.json.JsonConverter",
      "// Errors":  "Ensure creation and running connectors write errors to cloud watch.",
      "errors.log.include.messages": "true",
      "errors.log.enable": "true",
      "// Credentials":  "Access secrets manager for MySQL credentials; Worker must be configured with SecMgr libs.",
      "database.user": "${secretManager:}",
      "database.password": "${secretManager:}",
      "// Transforms":  "Use SMT/content filtering exclude messages based upon values.",
      "// Transforms": "Route is one technique for routing the incoming event to a new topic name",
      "transforms": "topicname,route",
      "transforms.route.language": "jsr223.groovy",
      "transforms.route.type": "io.debezium.transforms.ContentBasedRouter",
      "transforms.route.topic.expression": "(value.op in ['c','u','d'] )   ? topic : null ",
      "transforms.topicname.type": "org.apache.kafka.connect.transforms.RegexRouter",
      "transforms.topicname.replacement": "int_$3",
      "transforms.topicname.regex": "([^.]+)\\.([^.]+)\\.([^.]+)",
      "// Default Topic Parameters":  "Topics maybe pre-created to automatically so, e.g. new tables may generate new topics",
      "topic.creation.default.partitions": "1",
      "topic.creation.default.compression.type": "lz4",
      "topic.creation.default.replication.factor": "3",
      "// AWS/MSK Brokers ":  "Provide the list of brokers,",
      "database.history.kafka.bootstrap.servers": "<bootstrap server list>:9092",
      "// Polling ":  "Number of records or bytes to return from the poll() call/Time between polling",
      "max.poll.records": "10000",
      "max.batch.size": "10001",
      "poll.interval.ms": "50",
      "// Topic Replicas ":  "When confirmation of write to the topic is confirmed (leader and/or additional replicas)",
      "acks": "1",
      "// Scalability ":  "For Source Connectors to MySQL only 1 connector thread can read the binlog at a time.",
      "tasks.max": "1",
      "// Database Server Info": "Server Connectivity Information",
      "database.server.id": "XXXXXXXXX",
      "database.server.name": "<connector db server name>",
      "database.port": "3306",
      "database.hostname": "<hostname/ip address>",
      "// Database Table/Column Selection": "Allows for only specific tables to be selected for Kafka topics",
      "database.whitelist": "<mysql schema name>",
      "database.include.list": "<mysql schema name>",
      "table.include.list": "<mysql schema name>.<table name>, <mysql schema name>.<table name2>,etc ",
      "column.include.list": "<mysql schema name>.<table name1>.<column name>, <mysql schema name>.<table name1>.<column name>,<et al>  ,
 
    "connectorName": "debezium-src-mysql",
    "// No Auto Scaling for Debezium Connector ":  "Only one reader of the binlog at a time",
    "capacity": {
      "provisionedCapacity": {
        "mcuCount": 1,
        "workerCount": 1
      }
    },
    "kafkaCluster": {
      "apacheKafkaCluster": {
        "bootstrapServers": "<msk-cluster-server-id1>:9092,<msk-cluster-server-id1>:9092,<msk-cluster-server-id1>9092",
        "vpc": {
          "securityGroups": [
            "secgrp-xxxx"
          ],
          "subnets": [
            "subnet-1",
            "subnet-2"
          ]
        }
      }
    },
    "//Encryption :":"Adding encryption between MySQL and the AWS/MSK Cluster",
    "kafkaClusterClientAuthentication": {
      "authenticationType": "NONE"
    },
    "//Intra Cluster Encryption :":"Adding encryption between the AWS/MSK Cluster Hosts",
      "kafkaClusterEncryptionInTransit": {
      "encryptionType": "PLAINTEXT"
    },
    "kafkaConnectVersion": "2.7.1",
    "logDelivery": {
      "workerLogDelivery": {
        "cloudWatchLogs": {
          "enabled": true,
          "logGroup": "<msk-sink>/debezium-src-connector"
        }
      }
    },
    "plugins": [
      {
        "customPlugin": {
          "// Debezium Plugin zip file":"Pre-constructed zip is feature dependant and critical see plugin doc",
          "customPluginArn": "<arn of the S3 location of debezium plugin package>",
          "revision": 1
        }
      }
    ],
    "serviceExecutionRoleArn": "<arn of assigned role with access to identified resources>",
    "workerConfiguration": {
      "revision": 1,
      "// Worker Config": "Provides configuration of the Worker JVM that runs the Kafka Connector",
      "workerConfigurationArn": "arn:aws:<redacted worker arn>:worker-configuration/<redacted worker arn>-offset/134143141-2"
    }
  }
```
Sample Messages

```json
{
  "before": {
    "id": 3796,
    "ue_id": 419,
    "ue_name": "test-orig",
    "ue_count": 430,
    "cdc_modified_ts": 1673990000000,
    "cdc_status": "active"
  },
  "after": {
    "id": 3796,
    "ue_id": 419,
    "ue_name": "test",
    "ue_count": 431,
    "cdc_modified_ts": 1673990008000,
    "cdc_status": "pending"
  },
  "source": {
    "version": "1.8.1.Final",
    "connector": "mysql",
    "name": "mskdev_cdc",
    "ts_ms": 1673990008000,
    "snapshot": "false",
    "db": "mskdev",
    "table": "cdc_msk_test",
    "server_id": 1691652969,
    "file": "mysql-bin-changelog.000911",
    "pos": 1847,
    "row": 0
  },
  "op": "c",
  "ts_ms": 1673990008688
}
```
