ps -aux|grep 'uwsgi_logindemo' |awk '{print $2}'|xargs kill -9
echo "uwsgi logindemo is stop!"
sleep 2
ps -aux|grep 'qcluster' |awk '{print $2}'|xargs kill -9
sleep 2
echo "qcluster is stop!"