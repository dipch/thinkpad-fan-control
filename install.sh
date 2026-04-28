#!/bin/sh
install_folder=/opt/fancontrol
mkdir -p $install_folder/src
chmod +x src/fan-pkexec
chmod +x src/fan.py
cp src/fan.py $install_folder/src/fan.py
cp src/fan-pkexec $install_folder/fan-pkexec
cp Resources/Thinkfan.policy /usr/share/polkit-1/actions/Thinkfan.policy
cp Resources/thinkfan.desktop /usr/share/applications/thinkfan.desktop
#cp Resources/thinkfan.desktop /home/[youruser]/.config/autostart/thinkfan.desktop
ln -s $install_folder/fan-pkexec /bin/fancontrol
mkdir $install_folder/Resources
cp Resources/icon.png $install_folder/Resources/icon.png
cp Resources/on.png $install_folder/Resources/on.png
cp Resources/off.png $install_folder/Resources/off.png
chmod +r $install_folder/Resources/off.png
chmod +r $install_folder/Resources/on.png
touch /etc/modprobe.d/thinkpad_acpi.conf
echo "options thinkpad_acpi fan_control=1" > /etc/modprobe.d/thinkpad_acpi.conf
