# install mongodb
## mac
brew tap mongodb/brew
brew install mongodb-community
brew install mongodb-community-shell # mongo command

sudo mkdir -p /usr/local/var/mongodb
sudo chown -R $USER /usr/local/var/mongodb
sudo mkdir -p /usr/local/var/log/mongod
sudo chown -R $USER /usr/local/var/log/mongodb
cat mongod.conf.dev > /usr/local/etc/mongod.conf # set systemLog.destination and storage.dbPath

# install python library
pip install flake8 black isort mypy
pip install pymongo
pip install lxml --index-url=https://pypi.python.org/simple/
pip install cssselect