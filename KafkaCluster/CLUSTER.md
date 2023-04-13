#### Configuring MSK Cluster
Creating the AWS MSK Cluster is can be performed from the AWS/MSK Console or via command line scripts.  For existing environments many of the properties in the json configuration files will need to be curated with you environments specific VPCs subnets and security groups.  These will also need to be aligned with the Source and Target data stores and ensure that MySQL port of 3306 and Neo4j ports of 7474,7687 (potentially others) are included in your security group rules.
 <br>
The associated scripting here provides the outline for a freestanding environment, (i.e. no pre-existing infrastructure)

The create-cluster.sh script will use three json configuration files to construct your test MSK cluster.  Note this is NOT FREE and you will incur charges against you AWS account so be sure to tear down all components (i.e. Cluster, Workers, Connectors, MySQL, Neo4j) 
<br>
Prerequisites include the subnets and security groups that need to be aligned  with your source and target data stores; where these need to be inserted into
the associated json configurations.  
<br>
Once complete use the AWS Console to confirm your configurations.
<br>
Note: you can use the AWS MSK Console 

Here is a great article on standing up the AWS MSK Cluster (it includes 
creation of generic client machines which we'll substitute MySQL and the 
Neo4j server.

https://medium.com/aws-in-plain-english/it-cant-get-simpler-than-this-setup-kafka-cluster-in-aws-431cd6cf914d



### !!!This will Cost you!!
As mentioned AWS/MSK is not free unless you're using credits and while some of the costs are nominal the MSK Cluster,MSK Workers/Connectors, RDS, EC2 and heavy traffic can mount up.
### AWS Sample scripts
The below aws cli's will provide the basic framework for standing up your environment
####  AWS Creating the VPC
aws ec2 create-vpc   --cidr-block 172.31.0.0/16
vpc-0a9dcdb5837ecafb7
#### AWS Create the Subnets
aws ec2 create-subnet   
   --vpc-id vpc-0a9dcdb5837ecafb7 \
   --cidr-block 172.31.0.0/16     \  
   --availability-zone us-east-2a
aws ec2 create-subnet \
   --vpc-id vpc-0a9dcdb5837ecafb7 \
   --cidr-block 172.31.1.0/16 \
   --availability-zone us-east-2b
aws ec2 create-subnet \
   --vpc-id vpc-0a9dcdb5837ecafb7 \
   --cidr-block 172.31.2.0/16 \
   --availability-zone us-east-2c
### AWS Security Groups
By default, clients can access an MSK cluster only if they're in the same VPC as the cluster. To connect to your MSK cluster from a client that's in the same VPC as the cluster, make sure the cluster's security group has an inbound rule that accepts traffic from the client's security group
https://docs.aws.amazon.com/msk/latest/developerguide/client-access.html




### MySQL Configuration
Using the associated security groiup
aws rds create-db-instance \
--db-instance-identifier test-mysql-instance \
--db-instance-class db.t3.micro \
--engine mysql \
--master-username admin \
--master-user-password secret99 \
--generate-cli-skeleton output \
--vpc-security-group-ids  vpc-<redacted-secgroup>  \
--availability-zone us-east-2a \
--allocated-storage 20


### Neo4j AWS Images
Starting a small Neo4j instance 
See details here https://neo4j.com/developer/neo4j-cloud-aws-ec2-ami/#:~:text=Open%20the%20AWS%20EC2%20console,you%20would%20like%20to%20use.

aws ec2 describe-images \
--region us-east-1 \
--owner 385155106615 \
--query "Images[*].{ImageId:ImageId,Name:Name}"

export KEY_NAME=myNeoKey.pem
ami-03ba6b555d51ab0ff
aws ec2 run-instances \
--image-id <selected Neo4j Image> \
--count 1 \
--instance-type m3.medium \
--key-name $KEY_NAME \
--security-groups $GROUP \
--query "Instances[*].InstanceId" \
--region us-east-1
aws ec2 terminate-instances \
--instance-ids [InstanceId] \
--region us-east-1



sudo amazon-linux-extras install epel -y
sudo yum install https://dev.mysql.com/get/mysql80-community-release-el7-5.noarch.rpm

sudo yum install mysql-community-server 
