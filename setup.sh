sudo su
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
pip install wheel
pip install flask flask_httpauth requests
git clone https://github.com/CycloneBiz/OpenLoop.git
cd OpenLoop