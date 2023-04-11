The Kafka Source Connector configuration contains generic kafka Connect features along with debezium specific libraries that are responsible for reading the source MySQL database transaction logs (binlogs) and submit these events to the Kafka Cluster.  The AWS/MSK KafkaConnector leverage these highly stable connector libraries for reading the proprietary formats of the source database at very low (and configurable) latencies and sub-second ingestion for Change Data Capture processing.
This example looks at the key components of an AWS/MSK configuration,namely

Debezium Plugin
The current demo configuration uses several additional libraries for performing groovy scripting in support of SMT (message routing/filtering) as well as AWS Secrets Manager implementation.

Th
####Debezium connector for MySQL Documentation
-   https://debezium.io/documentation/reference/stable/connectors/mysql.html

MySQL DB parameter settings.


Partitioning
While the default partitioning strategy is round-robin, it is possible to manually define the partiion keys 
to eliviate dead-lock situations.  
https://debezium.io/documentation/reference/stable/connectors/mysql.html#mysql-property-message-key-columns

{
"name": "my-connector",
"config": {
"...": "...",
"message.key.columns": "my_database.users:department_id"
}
}