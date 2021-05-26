#!/bin/bash -x
PS4='$(date "+%s.%N ($LINENO) + ")'
cd $1
WORK=$(pwd)

rm -rf node_modules*
rm -rf node-v8.11.2-linux-x64*

cp -a ../../../../../nms_vue/node_modules.tar ./
cp -a ../../../../../nms_vue/node-v8.11.2-linux-x64.tar ./

tar -xf node-v8.11.2-linux-x64.tar
tar -xf node_modules.tar

export PATH=$PATH:$WORK/node-v8.11.2-linux-x64/bin
npm install
npm run build:prod

rm -rf node_modules*
rm -rf node-v8.11.2-linux-x64*

cd -