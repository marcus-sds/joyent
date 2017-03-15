ps -a | grep -v grep | grep swift-accesslog-read.py|grep -v vi > /dev/null
result=$?
if [ "${result}" -eq "0" ]; then
        echo "it's running"
        exit 0;
fi

LOGDIR="/logdata/objstr/objstr-tps"
M=`date +%Y%m`
D=`date +%d`

hosts=`ls /logdata/muskie/$M/$D/muskie*|awk -F\- '{print $2}'|uniq`

# muskie default creation
for host in hosts
do
if [ ! -f muskie-$host.txt ];then
echo "/logdata/muskie muskie-$host 551 dummy" > muskie-$host.txt
fi
done

for host in $hosts
do
python swift-accesslog-read.py interval=60 swift=mantabmt infile=muskie-$host.txt outfile=$LOGDIR/muskie-$host.log host=$host &
done
rm -f *.tmp
