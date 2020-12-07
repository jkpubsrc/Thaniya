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



/usr/sbin/usermod -U "$THANIYA_ACCOUNT"















