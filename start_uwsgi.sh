#!/bin/sh
SCRIPTDIR=`dirname $0`
echo $SCRIPTDIR
cd $SCRIPTDIR

if [ $# -gt 1 ]; then
  echo "Usage: $0 <server_name>"
  exit
fi
if [ $# -eq 0 ]; then
  echo "No arg specified, starting default server"
  instance=default
else
  instance=$1
fi
if [ $USER == "root" ]
    then
	echo "it's recommanded not to run KaraCos as root"
	exit
fi

if [ -d $(pwd)/server/$instance ]
then
	if [ ! -d $(pwd)/server/$instance/deploy ]
	then
		mkdir $(pwd)/server/$instance/deploy
	fi
	if [ ! -d $(pwd)/server/$instance/log ]
	then
		mkdir $(pwd)/server/$instance/log
	fi
	if [ ! -d $(pwd)/server/$instance/temp ]
	then
		mkdir $(pwd)/server/$instance/temp
	fi
else
	echo "$instance doesnt exist in $KARACOS_HOME/servers"
fi


/usr/local/sbin/uwsgi --ini $(pwd)/server/$instance/conf/wsgi.ini --python-path $(pwd)/lib/ --python-path $(pwd)/py/ -d $(pwd)/server/$instance/log/sysout.log
