#!/bin/bash

cat Desktop/90024/Assignment2/sniffer.data | while read -r line
do
curl -H "Content-Type:application/json" -X POST http://admin:616161@172.26.133.30:5984/test -d "$line"
done
