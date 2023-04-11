export conn_config=$1
if ! [ -f $conn_config ]; then
	echo "Input configuration file not present exiting"
fi
json=$(jq '.' $conn_config 2>/dev/null)
jsonstat=$? 
if [ $jsonstat != 0 ]; then
	echo "error in config file not valid json"
	echo "status : $jsonstat"
fi
# echo "jsonstat    $jsonstat"
aws kafkaconnect create-connector --cli-input-json file://${conn_config}
aws kafkaconnect list-connectors|jq '.connectors[]| [ .connectorName, .connectorState, .creationTime ]|@tsv '|cat |sed 's/,/ | /g'| sed  's/$/\n/'
