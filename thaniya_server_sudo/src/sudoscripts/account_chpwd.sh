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



STDIN_DATA=$(</dev/stdin)
echo "$STDIN_DATA" | /usr/sbin/chpasswd "$THANIYA_ACCOUNT"















