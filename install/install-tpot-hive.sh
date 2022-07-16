#!/bin/bash

source .env

useradd -s /bin/bash -m -p $(echo "$user_pass" | openssl passwd -1 -stdin) tsec
usermod -aG sudo tsec

apt install git ufw -y

git clone https://github.com/telekom-security/tpotce
cd tpotce/iso/installer/

cat > tpot.conf << EOF
# tpot configuration file
# myCONF_TPOT_FLAVOR=[STANDARD, HIVE, HIVE_SENSOR, INDUSTRIAL, LOG4J, MEDICAL, MINI, SENSOR]
myCONF_TPOT_FLAVOR='HIVE'
myCONF_WEB_USER='$web_user'
myCONF_WEB_PW='$web_pass'
EOF

./install.sh --type=auto --conf=tpot.conf

ufw allow 64295/tcp
reboot