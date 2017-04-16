#!/bin/bash

if [[ -n "$TRACE" ]]; then                                                      
    export PS4='[\D{%FT%TZ}] ${BASH_SOURCE}:${LINENO}: ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
    set -o xtrace                                                               
fi                                                                              

set -o errexit

job_id=${1:-}

req_id=$(sdc-workflow "/jobs/$job_id" | json -Ha params.x-request-id)
cnapi=$(sdc-vmname cnapi)
zlogin "$cnapi" "source ~/.profile
  bunyan -c this.snapshot -o bunyan --strict -c 'this.req_id==\"$req_id\"' \
  \$(svcs -L cnapi) /var/log/sdc/upload/cnapi_* | json -ga snapshot \
  | base64 -d | gunzip - | json steps"
