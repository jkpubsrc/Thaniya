#!/bin/bash

set -e



if ! [[ "$@" =~ ^[0-9][0-9]$ ]]; then
	echo "ERR: errInvArgs"
	exit 1
fi

THANIYA_ACCOUNT="thaniya_$@"
HOME_DIR=$( getent passwd "$THANIYA_ACCOUNT" | cut -d: -f6 )

if [[ -z "$HOME_DIR" ]]; then
	echo "ERR: errInvAccount"
	exit 1
fi



RESULT_DIR=`/usr/bin/python3 -B -c 'import thaniya_server_upload; print(thaniya_server_upload.UploadHttpdCfg.load().slotMgr.getValue("resultDir"))'`
if ! [[ "$RESULT_DIR" =~ ^/[a-zA-Z] ]]; then
	echo "ERR: errResultDir"
	exit 1
fi



echo "TEST :: THANIYA_ACCOUNT = $THANIYA_ACCOUNT"
echo "TEST :: HOME_DIR = $HOME_DIR"
echo "TEST :: RESULT_DIR = $RESULT_DIR"
echo "TEST :: `id`"















