#!/bin/sh
set -x
set -e
rm -r cookbooks/webtelemetry
cp -r vendor/cookbooks/webtelemetry cookbooks

tar czf cookbooks.tar.gz cookbooks
s3cmd put -P cookbooks.tar.gz s3://ubalo/webtelemetry/cookbooks.tar.gz
tar czf roles.tar.gz roles
s3cmd put -P roles.tar.gz s3://ubalo/webtelemetry/roles.tar.gz
