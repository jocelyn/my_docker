#!/bin/bash

tmp_docker_name=roc-cms
tmp_docker_instance=my-${tmp_docker_name}
docker rm -f ${tmp_docker_instance}

