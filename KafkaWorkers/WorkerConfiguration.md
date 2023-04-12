## Kafka Worker Configuration
The AWS/MSK Workers run as a  JVM within the MSK environment and are responsible for managing the source and sink Connector execution.  The workers need to provision, scale, connect, secure and retain state for the source connectors (incase of reconfiguration.)  

<br>
One key difference between MSK and other Kafka offerings is that Kafka Connectors cannot be paused or changed, but rather are DELETED and CREATED, as such source connectors need some form of state determining the last offset processed. In the below example note the "offset.storage.topic" parameter that identifies a topic that is used to track the last offset/request.  This internal topic specified in the worker configuration is only necessary for the Source Connector.  Additionally, Source Connectors in this case will only have a single task to ensure the MySQL transaction log is only read sequentially (tasks.max=1.)

See the extensive AWS / MSK worker documentation for details along with a basic example of the configuration below:
https://docs.aws.amazon.com/msk/latest/developerguide/msk-connect-workers.html

#### Source Worker Example 
<br>key.converter=org.apache.kafka.connect.storage.StringConverter
<br>value.converter=org.apache.kafka.connect.storage.StringConverter
<br>producer.max.request.size=2097152 
<br>max.poll.records=5000 
<br>tasks.max=1
<br>producer.batch.size=32768
<br>offset.storage.topic=msk-cdc-source-offset-topic
<br>reconnect.backoff.ms=1000
<br>reconnect.backoff.max.ms=5000

