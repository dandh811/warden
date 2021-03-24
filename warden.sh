#!/bin/bash

source /opt/warden/bin/activate
cd /opt/warden/warden

case "$1" in
start)
   python manage.py makemigrations
   python manage.py migrate
   #nohup python manage.py runserver 0.0.0.0:80 > /var/log/warden/run.log 2>&1 &
   #echo $!>/var/run/warden.pid
   export C_FORCE_ROOT="true"
   nohup /opt/warden/bin/celery -A ProjectSettings worker -l info -n worker > /var/log/warden/celery.log 2>&1 &
   python manage.py crontab add
   echo $!>>/var/run/warden.pid
   service apache2 restart
   ;;
stop)
   python manage.py crontab remove
   kill `cat /var/run/warden.pid`
   cat /var/run/warden.pid | while read line
   do
	   kill $line
   done
   rm /var/run/warden.pid
   pkill celery
   pkill chrome
   ;;
restart)
   $0 stop
   $0 start
   ;;
status)
   if [ -e /var/run/warden.pid ]; then
      echo warden is running, pid=`cat /var/run/warden.pid`
   else
      echo warden is NOT running
      exit 1
   fi
   ;;
*)
   echo "Usage: $0 {start|stop|status|restart}"
esac

exit 0
