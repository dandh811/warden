apt-get -y install nmap
apt-get -y install masscan
apt-get -y install redis-server
apt-get -y install sqlmap
apt-get -y install whatweb
apt-get -y install rabbitmq-server
apt-get -y install mongodb-clients
apt-get -y install awscli
apt-get -y install build-essential python3-dev libssl-dev libffi-dev libxml2 libxml2-dev libxslt1-dev zlib1g-dev libmysqlclient-dev
apt-get -y install phantomjs

source /opt/warden/bin/activate

/opt/warden/bin/python -m pip install --upgrade pip
pip install -r /opt/warden/warden/requirements.txt

cp /opt/warden/warden/warden.sh /etc/init.d/warden
chmod +x /etc/init.d/warden

/etc/init.d/warden restart
