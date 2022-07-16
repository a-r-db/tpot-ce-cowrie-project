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
myCONF_TPOT_FLAVOR='HIVE_SENSOR'
myCONF_WEB_USER='$web_user'
myCONF_WEB_PW='$web_pass'
EOF

./install.sh --type=auto --conf=tpot.conf

port_tcp="80 64295 443 5555 8443 443 102 502 1025 2404 10001 44818 47808 50100 22 23 11112 21 42 135 1433 1723 1883 3306 8081 9200 25 110 143 993 995 1080 5432 5900 389 1433 1521 5432 6379 8080 9200 11211 631 9200 2575 5060"

for val in $port_tcp
do
    ufw allow ${val}/tcp
done

port_udp="5000 161 623 19 53 123 1900 69 5060"

for val in $port_udp
do
    ufw allow ${val}/udp
done

reboot