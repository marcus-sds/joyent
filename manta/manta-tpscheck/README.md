#### manta trending
1. syslog-ng should receive the syslog from webapi
create syslog-ng.conf

systemctl enable syslog-ng</br>
systemctl start syslog-ng</br>

2. webapi should send data to syslo-ng
modify /etc/rsyslog.conf
svcadm restart system-log

3. setup
mkdir -p /app/manta-tpscheck/logs</br>
mkdir -p /logdata/objstr/objstr-tps</br>
copy swift-tps.sh
copy swift-accesslog-read.py

4. add swift-tps.sh to crontab
