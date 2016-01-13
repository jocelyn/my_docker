#!/bin/bash

if [[ "$1" == "" ]]; then
	op="none"
else
	op=$1
fi
if [[ "$op" == "demo" ]]; then
	echo Launching the demo.
	cd $ROCDIR/examples/demo
	./demo
else
	if [[ "$op" == "estudio" ]]; then
		cd $ROCDIR
		estudio -config $ROCDIR/examples/demo/demo-safe.ecf -target demo_standalone_scoop
	else
		if [[ "$op" == "console" ]]; then
			xterm
		else
			echo "Bye ..."
		fi
	fi
fi
