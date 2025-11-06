#!/bin/bash
echo "######### Starting to execute SH script... #########"

# If you have credentials for your DB uncomment the following two lines
#USER_NAME='user_name'
#PASSWORD='user_password'

echo "######### Sleeping for 25 seconds #########"
sleep 5

# If you have credentials for your DB use: while ! cqlsh scylla -u "${USER_NAME}" -p "${PASSWORD}" -e 'describe cluster' ; do
while ! cqlsh scylla -e 'describe cluster' ; do
     echo "######### Waiting for main instance to be ready... #########"
     sleep 5
done


cqlsh scylla -f "./scylla_scripts/create_schema.cql"
echo "######### Stopping temporary instance! #########"