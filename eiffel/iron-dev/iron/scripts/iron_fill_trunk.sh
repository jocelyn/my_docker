#!/bin/bash

T_IRON_DIR=$1
T_IRON_PORT=$2
T_IRON_username=$3
T_IRON_password=$4

T_IRON_VERSION=trunk

T_IRON_BIN=$T_IRON_DIR/bin
T_IRON_WEB=$T_IRON_DIR/www

mkdir -p $T_IRON_WEB/_iron/repo/versions/$T_IRON_VERSION
cd $T_IRON_WEB
#Launch the irond server for the building time.
$T_IRON_BIN/irond &

cp -rf $EIFFEL_SRC/tools/iron/delivery/VERSIONS/alter $T_IRON_DIR/scripts/upload/VERSIONS/alter

iron repository -a http://localhost:$T_IRON_PORT/$T_IRON_VERSION

cd $T_IRON_DIR/scripts/upload/
#Build credential.py
echo "#!/usr/bin/python" > credential.py
echo >> credential.py
echo "def login():" >> credential.py
echo -e  "\treturn \"${T_IRON_username}\"" >> credential.py
echo >> credential.py
echo "def password():" >> credential.py
echo -e  "\treturn \"${T_IRON_password}\"" >> credential.py
echo >> credential.py

#Build repository_cfg
echo "#!/usr/bin/python" > repository_cfg.py
echo >> repository_cfg.py
echo "def version():" >> repository_cfg.py
echo -e  "\treturn \"${T_IRON_VERSION}\"" >> repository_cfg.py
echo >> repository_cfg.py
echo "def branch():" >> repository_cfg.py
echo -e  "\treturn \"${T_IRON_VERSION}\"" >> repository_cfg.py
echo >> repository_cfg.py
echo "def repository():" >> repository_cfg.py
echo -e  "\treturn \"http://localhost:${T_IRON_PORT}\"" >> repository_cfg.py
echo >> repository_cfg.py

./ise_upload_version.py

#Kill previous irond for the building time.
pkill -9 irond

