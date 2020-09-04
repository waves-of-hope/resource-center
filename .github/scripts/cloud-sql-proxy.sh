#!/bin/sh

# Run cloud sql proxy
$PROXY_LOCATION/cloud_sql_proxy -instances=$INSTANCE_CONNECTION_NAME=tcp:3306