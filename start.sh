sleep 2
source /opt/pyenv/bin/activate && cd /opt/pyenv/logindemo/ && uwsgi --ini uwsgi_logindemo.ini > start.log 2>&1 &
echo "uwsgi logindemo is start ..."
sleep 2
source /opt/pyenv/bin/activate && cd /opt/pyenv/logindemo/ && python manage.py qcluster > qcluster.log 2>&1 &
echo "qcluster is start ..."
sleep 2