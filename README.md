# rpi-field-backup
Let's back up a Canon camera to USB storage on an RPI, using FTP.

# prereqs.

Need the rpi configured to run as a wifi access point, and configure vstftpd to allow the camera
to connect. Have fun!

# rpi setup

as root:

```
apt-get install python3-pip
update-alternatives --install $(which python) python $(readlink -f $(which python3)) 3
update-alternatives --config python
pip3 install --upgrade setuptoolsp
pip3 install --uprade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
python3 raspi-blinka.py
reboot
```

post reboot (as root still)
```
pip3 install adafruit-circuitpython-charlcd
```

# pinouts

```
pi         adafruit shield
     __________
    |          |
 __________    |
|          |   |
2 4 6 8    2 4 6 8
. . . .    . . . .
. . . .    . . . .
1 3 5 9    1 3 5 9
  | |__________|
  |__________|
```

# commands

lcd-daemon.py responds to these buttons on the lcd hat:

* "SELECT" (leftmost button) = system shutdown
