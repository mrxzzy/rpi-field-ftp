#!/bin/bash

echo "copying udev rules.."
cp 99-field-backup.rules /etc/udev/rules.d/
echo "copying systemd unit.."
cp media-dest.mount /etc/systemd/system/
cp lcd.service /etc/systemd/system/
cp lcd-daemon.py /usr/local/bin/lcd-daemon.py

echo "reloading configs.."
systemctl daemon-reload
systemctl enable media-dest.mount
systemctl enable lcd.service
systemctl restart lcd.service
udevadm control --reload-rules

echo "chmod sd-backup script.."
chmod 755 /usr/local/bin/lcd-daemon.py
