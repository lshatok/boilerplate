#!/bin/sh
export JAVA_HOME=/usr/lib/jvm/j2sdk1.6-oracle
while read table_name; do
  hbase org.apache.hadoop.hbase.mapreduce.Export -D hbase.client.scanner.caching=100000 -D mapred.output.compress=true -D mapred.output.compression.codec=org.apache.hadoop.io.compress.SnappyCodec $table_name /tmp/tables/$table_name
done < "tables.txt"