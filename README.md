# Introduction
pyAndChargeLimit calls a REST API when your Android mobile device reaches a user defined battery percentage. This enables optimized, ["40-80" battery charging](https://support.apple.com/en-us/HT210512) of unrooted, unattended devices using free, open-source software.

Charge shutoff requires:

* An external hardware IoT smart switch, with Wifi interface and REST API (such as a inexpensive ['DIY Mode' Sonoff device](https://github.com/arendst/Tasmota/wiki/Sonoff-DIY) or smartplug running Tasmoda)
* [QPython](https://github.com/qpython-android/qpython/releases/latest)
* Root is _not required_

Example:

<img src="doc/charge-limit.jpeg" width="50%" height="50%"/>

# Setup

* Install [QPython](https://github.com/qpython-android/qpython/releases/latest), tap `QPYPI` > `QPYPI CLIENT`, run `pip install requests PyYAML watchdog`
* Copy [stopcharge.py](stopcharge.py) to QPython `scripts/` directory
* Copy [config.yml](stopcharge.py) to QPython `scripts/` directory

_Setting up the hardware smart switch to connect to the Android device's Wifi hotspot or wifi network is beyond the scope of this README. (See: [Protocol Doc](https://github.com/itead/Sonoff_Devices_DIY_Tools/blob/5a49d77/SONOFF%20DIY%20MODE%20Protocol%20Doc%20v1.4.md) for Sonoff DIY Mode, etc.)_

# Usage
To run pyAndChargeLimit

* open QPython, tap `Explorer` > `scripts/` > `config.yml`
* Enter the Sonoff deviceId & IP address of the smart outlet your charger is plugged into, and tap 💾 icon
* Tap the ▶️ icon, tap ⬅️ icon near top of terminal screen (see Example above), tap `YES` at the prompt for `Run on background`

Charge limit is set at 80%, to minimize degradation of lithium-ion battery capacity.

# Background
Lithium-ion battery capacity can be conserved by minimizing recharge time while the battery state of charge (SoC) is low (<30-40%) or very high (>80%). ["How to prolong " (Cadex Electronics Inc.)](https://batteryuniversity.com/learn/article/do_and_dont_battery_table)
 
Stock Android 10 can easily set a Battery Saver minimum percentage, but unattended charging cannot be stopped at a specified maximum percentage without rooting.

Google Pixel 3a XL seems to try and _lessen_ capacity degredation, by reducing charging rate when battery is below 40% and significantly reducing rate above 80% charged.

<p align="center">
<img src="doc/Google-Pixel-3a-XL-benchmarks-charge-rate-768x863.jpg" width="60%" height="60%"/>
<br/>
Per <a href="https://www.trustedreviews.com/reviews/google-pixel-3a-xl-battery-life">Alex Walker-Todd, 2019 (trustedreviews.com)</a>
</p>

PyAndChargeLimit lets unrooted, unattended devices further reduce capacity degradation by eliminating all charging / discharging above a specified SoC.
