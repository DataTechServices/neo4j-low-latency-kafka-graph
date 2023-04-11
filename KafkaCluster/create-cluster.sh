aws kafka create-cluster \
    --cluster-name "dts-cdc-owr-cluster" \
    --broker-node-group-info file://broker-node-info.json \
    --logging-info file://logging-info.json \
    --encryption-info file://encryption-info.json \
    --kafka-version "3.3.1" \
    --enhanced-monitoring PER_TOPIC_PER_PARTITION \
    --number-of-broker-nodes 2
