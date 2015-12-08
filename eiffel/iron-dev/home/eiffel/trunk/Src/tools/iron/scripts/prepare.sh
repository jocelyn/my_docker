#!/bin/bash

TMP_EIF_COMP=/home/eiffel/_comp
TMP_EIF_IRONBIN=/home/eiffel/iron/bin
mkdir -p $TMP_EIF_COMP
mkdir -p $TMP_EIF_IRONBIN

function eif_generate_exec {
	TMP_EIF_FILE=$1
	TMP_EIF_TARGET=$2
	TMP_EIF_SYSTNAME=$3
	TMP_EIF_EXECNAME=$4

	ec -finalize -c_compile -config $TMP_EIF_FILE -target $TMP_EIF_TARGET -project_path $TMP_EIF_COMP
	cp $TMP_EIF_COMP/EIFGENs/$TMP_EIF_TARGET/F_code/$TMP_EIF_SYSTNAME $TMP_EIF_IRONBIN/$TMP_EIF_EXECNAME
	#\rm -rf $TMP_EIF_COMP/EIFGENs/$TMP_EIF_TARGET
}

echo Compile IRON controller
eif_generate_exec ../server/controller.ecf controller ironctl ironctl
eif_generate_exec ../server/server.ecf server_any irond irond
eif_generate_exec ../server/server.ecf server_libfcgi irond irond-libfcgi

cd $TMP_EIF_IRONBIN
echo port=8080 > iron.ini
mkdir -p _iron
cp -rf $EIFFEL_SRC/tools/iron/delivery/resources/node/doc  _iron/doc
cp -rf $EIFFEL_SRC/tools/iron/delivery/resources/node/html  _iron/html
cp -rf $EIFFEL_SRC/tools/iron/delivery/resources/node/template  _iron/template
./ironctl system initialize
./ironctl user create eiffel "eiffel123#" 

./irond &
