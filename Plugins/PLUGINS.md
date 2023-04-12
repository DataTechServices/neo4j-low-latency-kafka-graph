#### Configuring MSK Plugins
In our example using Kafka Connect with MSK requires the use of plugins that will provide the necessary functions and libraries for reading the RDBMS MySQL transaction log and writing these topics into Neo4j. For integrating into AWS/MSK these libraries must be packaged and uploaded to an accessible S3 bucket then referenced during plugin creation. This will then be associated with the MSK Connect Connectors and associated configuration.  As expected these connectors need to be download from the respective debezium and neo4j repositories and there appropriate versions along with any additional libraries of interest (e.g. debeizum groovy libraries.)  Additional links and comments are provide for each below.
 <br>
<br>


####  Debezium
In the case of the Source Kafka Connect Connector we are using debezium which supports a variety of database interfaces, having production quality connectors for  Oracle, MySQL, PostgreSQL, SQL Server, DB2 and MongoDB, along with incubating projects for Cassandara, Vitess and Spanner.  For this example we are using MySQL and will also want to include the additional functionality of Content-Based-Routing which will require the addition of the debezium scripting and groovy libraries.  To do so you will need to down load each of these libraries and combine them into a zip archive then upload to S3 so it may be referenced by the MSK Connectors, see the below references for datails.
<br>
<br>
References (all well documented on the debezium site)<br>
1) Download the core debezium Release (v2.1 at the time of this writing.)   https://debezium.io/releases/
2) Download the debezium scripting library (e.g. debezium-scripting-2.1.4.Final.tar.gz) https://debezium.io/documentation/reference/stable/transformations/content-based-routing.html#set-up-content-based-routing ;
3) Obtain tje JSR-223 script engine implementation and extract the groovy, groovy-json and groovy-jsr223 libraries

Once all these libraries have been combined you can follow the below instructions for zip formatting these files and uploading to S3. <br>
https://catalog.workshops.aws/msk-labs/en-US/mskconnect/source-connector-setup
<br>Your custom plugins should now be available for configuring your connectors. Note that any errors in this process should show up in the AWS MSK Connector logs upon Connector start up (ensure  "errors.log.enable": "true",)


#### Neo4j Kafka Connect Plugins
For the Neo4j Sink Connector visit the below github repo for the latest releases and download the appropriate version.  Also, documentation can be a little confusing, and will mention that neo4j-kafka-connect has both an open source and Confluent specific version. For MSK we will use the OpenSource version, also neo4j-streams is an early Kafka integration library that is in limited support and should be substituted with the neo4j-kafka-connect libraries.  <br> The below link contains 

Create an S3 bucket if you don’t have one already, and go to GitHub https://github.com/neo4j-contrib/neo4j-streams/releases to get neo4j-kafka-connect-neo4j-5.0.2-kc-oss.zip and upload it to your S3 bucket.

Please dont use the neo4j-kafka-connect-neo4j-5.0.2.zip, because that is intended for use with Confluent.

https://github.com/neo4j-contrib/neo4j-streams/releases/tag/5.0.2
