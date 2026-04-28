#!/bin/sh
install_folder=/opt/fancontrol
rm -r $install_folder
rm -r /bin/fancontrol
rm -r /usr/share/applications/thinkfan.desktop
rm -r /usr/share/polkit-1/actions/Thinkfan.policy
#rm -r /home/youruser/.config/autostart/thinkfan.desktop
rm -f /etc/modprobe.d/thinkpad_acpi.conf
