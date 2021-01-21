#!/bin/bash


set -e



cd thaniya_common
pip3install
cd ..

cd thaniya_server
pip3install
cd ..

cd thaniya_server_upload
pip3install
cd ..

cd thaniya_server_sudo
pip3install
cd ..

cd thaniya_server_archive
pip3install
cd ..

cd thaniya_server_ctrl
pip3install
cd ..


echo ""
echo "SUCCESS."
echo ""


