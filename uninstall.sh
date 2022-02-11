#!/bin/bash

echo "stopping and disabling units.."
systemctl stop media-dest.mount
systemctl stop lcd.service
systemctl disable media-dest.mount
systemctl disable lcd.service

echo "removing udev rules.."
rm -f /etc/udev/rules.d/99-field-backup.rules
echo "removing systemd units.."
rm -f /etc/systemd/system/media-dest.mount
rm -f /etc/systemd/system/lcd.service
rm -f /usr/local/bin/lcd-daemon.py

echo "reloading udev"
udevadm control --reload-rules

