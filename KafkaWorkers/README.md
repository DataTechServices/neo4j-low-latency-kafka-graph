## Kafka Worker Configuration
The AWS/MSK Workers run as a virtual JVM within the MSK environment and are responsible for managing the source and sink worked execution.  This includes scaling, connectivity, security and the actual plugin libraries used to integate the source/target environments with MSK.  

For a source connector in MSK the worker should also include an offset topic for your Kafka Connect process. In some Kafka version this offset file was kept as a file and in MSK was not originally available resulting in a full snapshot or laps in event messages between the time the connector was stop and restarted.

Recall that AWS/MSK at the time of this writing only allowed CREATE and DELETE functions which resulted in this gap between start and stops, this could also be induced by a failure of some kind.

Regardless below is a sample of this configuration and can easily be configured via the AWS/MSK UI or CLI.


See the AWS / MSK worker documentation for details 
#### Source Worker Example 
key.converter=org.apache.kafka.connect.storage.StringConverter  <br>
value.converter=org.apache.kafka.connect.storage.StringConverter  <br>
producer.max.request.size=2097152   <br>
max.poll.records=5000     <br>
tasks.max=1          <br>
producer.batch.size=32768  <br>
offset.storage.topic=msk-cdc-source-offset-topic
reconnect.backoff.ms=1000      <br>
reconnect.backoff.max.ms=5000   <br>
