#!/bin/bash

sudo docker run -t -i -e DISPLAY=:0 -v /tmp/.X11-unix:/tmp/.X11-unix -p 9999:9090 local/iron-dev $1
