#!/bin/bash

cat Desktop/90024/Assignment2/sniffer.data | while read -r line
do
curl -H "Content-Type:application/json" -X POST http://admin:1228@127.0.0.1:5984/test -d "$line"
done
