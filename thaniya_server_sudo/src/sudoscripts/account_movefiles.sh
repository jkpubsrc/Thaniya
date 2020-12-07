#!/bin/bash

set -e



if ! [[ "$1" =~ ^[0-9][0-9]$ ]]; then
	echo "ERR: errInvArgs"
	exit 1
fi

THANIYA_ACCOUNT="thaniya_$1"
HOME_DIR=$( getent passwd "$THANIYA_ACCOUNT" | cut -d: -f6 )

if [[ -z "$HOME_DIR" ]]; then
	echo "ERR: errInvAccount"
	exit 1
fi

if ! [[ "$2" =~ ^[a-zA-Z0-9_]+$ ]]; then
	echo "ERR: errInvArgs"
	exit 1
fi

TARGET_USER="$2"
SERVER_DIR=$( getent passwd "$TARGET_USER" | cut -d: -f6 )

if [[ -z "$SERVER_DIR" ]]; then
	echo "ERR: errInvAccount"
	exit 1
fi




# select target directory
DT=`date +"%Y%m%d%H%M%S-%N"`
RESULT_DIR=`/usr/bin/python3 -B -W ignore -c 'import thaniya_server_upload; print(thaniya_server_upload.UploadHttpdCfg.load().slotMgr.getValue("resultDir"))'`
if ! [[ "$RESULT_DIR" =~ ^/[a-zA-Z] ]]; then
	echo "ERR: errResultDir"
	exit 1
fi
TARGET_DIR="$RESULT_DIR/$DT-$THANIYA_ACCOUNT"



HOME_UPLOAD_DIR="$HOME_DIR/upload"
if [[ -d "$HOME_UPLOAD_DIR" ]]
then
	# move all data
	mv "$HOME_UPLOAD_DIR" "$TARGET_DIR"

	# set ownership
	chmod 700 "$TARGET_DIR"
	chown -R $TARGET_USER:$TARGET_USER "$TARGET_DIR"
fi


echo "$TARGET_DIR"












