#### manta trending
* syslog-ng should receive the syslog from webapi
create syslog-ng.conf

systemctl enable syslog-ng</br>
systemctl start syslog-ng</br>

* webapi should send data to syslo-ng
modify /etc/rsyslog.conf</br>
svcadm restart system-log</br>

* setup
mkdir -p /app/manta-tpscheck/logs</br>
mkdir -p /logdata/objstr/objstr-tps</br>
copy swift-tps.sh</br>
copy swift-accesslog-read.py</br>

* add swift-tps.sh to crontab
>* * * * * su - root -c "cd /app/manta-tpscheck;bash ./swift-tps.sh"
