sudo su
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools git
pip install wheel
git clone https://github.com/CycloneBiz/OpenLoop.git
cd OpenLoop
pip install -r requirements.txt
echo "Software downloaded, install systemd with it pointing to ./start.sh"