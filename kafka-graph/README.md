
Configuring EC2 host along side MSK cluster


https://docs.aws.amazon.com/msk/latest/developerguide/mkc-create-topic.html
                                     
1) VPC connection
   2) sec. grp.- default , launch-wizard-1/2 on vpc-1451c27f
   3)  secgrp: sg-020c7d0cb0f213f17 on  vpc-05c476575c322c357
2) ec2 instance vpc  vpc-1451c27f   and launch-wizard-2   subnet:subnet-b2257dfe
3)     msk subnets subnet-ee51ea85/subnet-586a9b25
   4) secgroup sg-4b29653c
# MSK Security Group :  sg-4b29653c
# 



# AWS Configure
This assigns the aws-access-key-id and aws-secret-access-key values
?? the newer versions of kafka need additional config to work.  2.2.1 
worked out of the box..3.3.1 did not.
     

# MySQL install 

wget 'https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-test-8.0.31-linux-glibc2.17-x86_64-minimal.tar.xz'


sudo amazon-linux-extras install epel -y
sudo yum install https://dev.mysql.com/get/mysql80-community-release-el7-5.noarch.rpm

sudo yum install mysql-community-server 
