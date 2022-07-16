# Installation Instructions

# Requirements

* Vultr $100 free trial account or Google Cloud $300 trial account
* 1 standalone honeypot or 1 hive honeypot and 1+ hive sensor honeypots
* 

## Steps

1. Start a server on any cloud services provider.
    * Requirements: use a password for initial login or both private key and password, but NOT private key alone.
2. Connect to the server using ssh with password (or private key)
3. IMPORTANT!: make a new file called .env with the credentials you'd like, similar to example.env in the root directory.
4. Put the credentials you would like to use for your machine(s) inside .env

### Steps for Standalone (>= 16gb RAM)

1. Run the [Hive install standalone](install/install-tpot-hive-standalone.sh)
2. Wait until the machine reboots
3. Run the [Hive install script cleanup](install/install-tpot-hive-cleanup.sh)

### Steps for Hive (>= 8gb RAM)

1. Run the [Hive install script](install/install-tpot-hive.sh)
2. Wait until the machine reboots
3. Run the [Hive install script cleanup](install/install-tpot-hive-cleanup.sh)

### Steps for Hive Sensors (>= 8gb RAM)

1. Run the [Hive Sensor install script](install/install-tpot-hive-sensor.sh)
2. Wait until the machine reboots
3. Run the [Hive Sensor install script part2](install/install-tpot-hive-sensor-part2.sh)