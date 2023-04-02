# install mongodb
## mac
brew tap mongodb/brew
brew install mongodb-community

sudo mkdir -p /usr/local/var/mongodb
sudo chown -R $USER /usr/local/var/mongodb
sudo mkdir -p /usr/local/var/log/mongod
sudo chown -R $USER /usr/local/var/log/mongodb
cat mongod.conf.dev > /usr/local/etc/mongod.conf # set systemLog.destination and storage.dbPath

# install python library
pip install flake8 black isort mypy
pip install pymongo