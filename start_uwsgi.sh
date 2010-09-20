#!/bin/sh
SCRIPTDIR=`dirname $0`
echo $SCRIPTDIR
cd $SCRIPTDIR
/usr/local/sbin/uwsgi -s 0.0.0.0:10000 -w karacos.wsgi --python-path $(pwd)/lib/ --python-path $(pwd)/py/ -b 25000 -d $(pwd)/server/default/log/sysout.log
