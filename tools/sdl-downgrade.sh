#!/bin/bash
# --------------------------------------------------------------------------
# In order to run tslib with pygame, a downgrade to an older version
# is currently necessary.
#
# source: 
# https://learn.adafruit.com/adafruit-2-4-pitft-hat-with-resistive-touchscreen-mini-kit/pitft-pygame-tips
#
# Note that this is a modified version:
#   - wheezy is now moved to legacy.raspbian.org
#   - the script not only works with stretch, but with all versions
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# --------------------------------------------------------------------------

# enable wheezy package sources
echo "deb http://legacy.raspbian.org/raspbian wheezy main
" > /etc/apt/sources.list.d/wheezy.list

# set stable as default package source
echo "APT::Default-release \"stable\";
" > /etc/apt/apt.conf.d/10defaultRelease

# current release
current=$(grep -E '^deb' /etc/apt/sources.list | cut -d' ' -f3)

# set the priority for libsdl from wheezy higher then the current package
echo "Package: libsdl1.2debian
Pin: release n=$current
Pin-Priority: -10
Package: libsdl1.2debian
Pin: release n=wheezy
Pin-Priority: 900
" > /etc/apt/preferences.d/libsdl

# install
apt-get update
apt-get -y --allow-downgrades install libsdl1.2debian/wheezy
