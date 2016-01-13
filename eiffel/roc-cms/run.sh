#!/bin/bash

tmp_docker_name=roc-cms
tmp_docker_fullname=local/${tmp_docker_name}
tmp_docker_instance=my-${tmp_docker_name}
tmp_docker_opts=" -h roc-cms --name ${tmp_docker_instance} -P "

if [[ "$OS" =~ ^Windows.* ]]; then
  tmp_docker_opts="$tmp_docker_opts -e=DISPLAY "
else
  tmp_docker_opts="$tmp_docker_opts -e=DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix "
fi


if [[ "$1" == "" ]]; then
	docker run -t -i ${tmp_docker_opts}  ${tmp_docker_fullname}

	tmp_docker_machine_ip="$(docker-machine ip default)"
	tmp_docker_machine_port="$(docker inspect ${tmp_docker_instance}  | awk -F'"' '/HostPort/ {print $4}')"
	echo OS=$OS
	if [[ "$OS" =~ ^Windows.* ]]; then
		echo "Host machine is Windows"
	fi
	echo "IP=$tmp_docker_machine_ip"
	echo "PORT=$tmp_docker_machine_port"

else
	docker run ${tmp_docker_opts} ${tmp_docker_fullname} $1 &
fi


#echo Info $(docker ps --no-trunc | grep ${tmp_docker_instance})
