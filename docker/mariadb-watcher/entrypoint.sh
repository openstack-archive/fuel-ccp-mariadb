#!/bin/bash
set -e

/usr/bin/watch_changes -prefix /pxc-cluster/"$CLUSTER_NAME" \
                       -proxy_user "$MYSQL_PROXY_USER" \
                       -proxy_pass "$MYSQL_PROXY_PASSWORD" \
                       -proxy_address "pxc-service" \
                       -root_pass "$MYSQL_ROOT_PASSWORD" \
                       -etcd_service "$DISCOVERY_SERVICE" 
