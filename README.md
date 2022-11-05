# PiJuice netdata collector
Monitor PiJuice HAT battery and power input informations through netdata. Netdata visualizes: battery charge level, battery voltage, battery current, battery temperature, power voltage, power current.

[PiJuice HAT](https://github.com/PiSupply/PiJuice) is a fully uninterruptable / uninterupted power supply that will always keep your Raspberry Pi powered!

[Netdata](https://github.com/netdata/netdata) is high-fidelity infrastructure monitoring and troubleshooting.
Open-source, free, preconfigured, opinionated, and always real-time.

## Installation
1. Clone or download this repo into a folder on your Pi
2. Change directory `cd Pijuice-netdata`
3. Copy collector file to netdata plugins.d destination. `cp pijuice.chart.py /usr/libexec/netdata/python.d/`
4. Copy collector config file. `cp pijuice.conf /etc/netdata/python.d/.`
5. Append `pijuice: yes` to `/etc/netdata/python.d.conf`

## Sample
![PiJuice-netdata sample](https://github.com/r-sherwood/PiJuice-netdata/blob/main/pijuice-netdata_sample.png)

## Debug
1. Login as netdata user `sudo su -s /bin/bash netdata`
2. Re/start netdata `systemctl restart netdata`
3. Execute `/usr/libexec/netdata/plugins.d/python.d.plugin pijuice debug trace nolock`

## Troubleshooting
Error: Permisson denied *(ERROR: pijuice[PiJuice] : update() unhandled exception: [Errno 13])*

`sudo chmod a+rw /dev/i2c-*` This is temporary and is lost at next boot so, to fix it permanently you need to do the following:

`vi /etc/udev/rules.d/99-com.rules` If this line exists: SUBSYSTEM=="ic2-dev", GROUP="i2c", MODE="0660"


