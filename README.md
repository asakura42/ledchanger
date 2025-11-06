# ledchanger
Change LED colors on Maono PD200X mic


Usage (sudo is optional, read below):

```
sudo ledchanger.py {0..8}|off
```

colors:

```
off - LED off
0   - white
1   - red
2   - orange
3   - yellow
4   - green
5   - blue
6   - deep blue
7   - purple
8   - RGB
```


To run without sudo add UDEV rules:

/etc/udev/rules.d/99-maono.rules:

```
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="352f", ATTRS{idProduct}=="0104", ATTRS{bInterfaceNumber}=="03", TAG+="uaccess"
```

after that:

```
sudo udevadm control --reload
sudo udevadm trigger -s hidraw
```
