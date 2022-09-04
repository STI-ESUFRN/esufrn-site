#!/bin/bash

### BEGIN INIT INFO
# Provides:          esufrn_site
# Required-Start:	 apache2 mysql $local_fs $time
# Required-Stop:     apache2 mysql $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Site da Escola de Saúde da UFRN
# Description:       Inicializador do site da Escola de Saúde da UFRN
### END INIT INFO

. /lib/lsb/init-functions

USER=suporte
GROUP=suporte
BIND=0.0.0.0:8000
EXECDIR=/var/www/html/esufrn/novo-site

NAME=NovoSite
APP=esufrn
APPMODULE=$APP.wsgi:application
DAEMON=gunicorn
PYTHONPATH=esufrn
ENV=_env/bin/activate
WORKERS=4
THREADS=2

NOW=$(date +"%F")
NOWT=$(date +"%T")

# Logging
LOGPATH=$EXECDIR/logs/$NOW
LOGFILE=$LOGPATH/$DAEMON-$NOWT.log

# PID
PIDPATH=$EXECDIR
PIDFILE=$PIDPATH/$DAEMON.pid

case $1 in
start)
	if [ -e $PIDFILE ]; then
		status_of_proc -p $PIDFILE $DAEMON "$NAME process" && status="0" || status="$?"
		if [ $status = "0" ]; then
			exit
		fi
	fi

	mkdir -p $LOGPATH
	mkdir -p $LOGPATH

	log_daemon_msg "Iniciando $DAEMON como $USER:$GROUP"
	log_daemon_msg "Os arquivos de log serão gravados em $LOGFILE"

	cd $EXECDIR &&
	source $ENV &&
	$DAEMON --name $NAME `[[ ! -z ${PYTHONPATH} ]] && echo --pythonpath $PYTHONPATH` -u $USER -g $GROUP --bind $BIND --workers $WORKERS --threads $THREADS --pid $PIDFILE --log-file $LOGFILE --daemon $APPMODULE
	log_end_msg $?
;;
stop)
	if [ -e $PIDFILE ]; then
		log_daemon_msg "Interrompendo o processo $NAME..."
		status_of_proc -p $PIDFILE $DAEMON && status="0" || status="$?"
		if [ "$status" = 0 ]; then
			start-stop-daemon --stop --quiet --oknodo --pidfile $PIDFILE
			/bin/rm -rf $PIDFILE
	 	fi
	else
		log_failure_msg "O serviço $NAME não está sendo executado"
		log_end_msg 0
	fi
;;  
restart)
	if [ -e $PIDFILE ]; then
		$0 stop
	fi
	sleep 5
	$0 start
;;
reload)
	if [ -e $PIDFILE ]; then
		start-stop-daemon --stop --signal USR1 --quiet --pidfile $PIDFILE --name $NAME
		log_success_msg "$NAME process reloaded successfully"
	else
		log_failure_msg "$PIDFILE does not exists"
	fi
;;
force-reload)
	$0 reload
;;
status)
	if [ -e $PIDFILE ]; then
		status_of_proc -p $PIDFILE $DAEMON "Processo $NAME" && exit 0 || exit $?
	else
		log_daemon_msg "O processo $NAME não está sendo executado"
		log_end_msg 0
	fi
;;
test)
	echo "Nada por aqui"
;;
*)
	echo "Uso: $0 {start|stop|restart|reload|force-reload|status}"
	exit 2
;; 
esac

