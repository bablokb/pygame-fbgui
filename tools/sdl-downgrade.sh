#!/bin/bash
# --------------------------------------------------------------------------
# In order to run tslib with pygame, a downgrade to an older version
# is currently (Stretch) necessary.
#
# source: 
# https://learn.adafruit.com/adafruit-2-4-pitft-hat-with-resistive-touchscreen-mini-kit/pitft-pygame-tips
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# --------------------------------------------------------------------------

# enable wheezy package sources
echo "deb http://archive.raspbian.org/raspbian wheezy main
" > /etc/apt/sources.list.d/wheezy.list

# set stable as default package source (currently stretch)
echo "APT::Default-release \"stable\";
" > /etc/apt/apt.conf.d/10defaultRelease

# set the priority for libsdl from wheezy higher then the stretch package
echo "Package: libsdl1.2debian
Pin: release n=stretch
Pin-Priority: -10
Package: libsdl1.2debian
Pin: release n=wheezy
Pin-Priority: 900
" > /etc/apt/preferences.d/libsdl

# install
apt-get update
apt-get -y --allow-downgrades install libsdl1.2debian/wheezy
