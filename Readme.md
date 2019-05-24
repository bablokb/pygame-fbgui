Framebuffer GUI for Pygame
==========================

Pygame-fbgui is a python3 GUI library based on pygame for small framebuffer 
devices. It supports various layouts and provides a number of standard widgets
like panels, texts, labels and buttons.

The library is under constant development. Implementation is not complete,
but everything implemented should work (if not, then it's a bug).

Although targeted at small framebuffer displays, it also works under X11. In
fact, development is done using X11. Adding support for Windows is
probably a matter of a few lines of code (patches are welcome).


Table of Contents
-----------------

  1. [News and Status](#news "News")
  2. [Hardware](#install "Hardware")
  3. [Installation](#install "Installation")
  4. [System Configuration](#system-configuration "System Configuration")
  5. [Running pygame-fbgui as a systemd-service](#running-pygame-fbgui-as-a-systemd-service "Running pygame-fbgui as a systemd-service")
  6. [Documentation](#documentation "Documentation")


News
----

### April 2019 ###

  - Core widgets available
  - Border layout and flow layouts implemented
  - Support for mouse-events


Hardware
--------

The target-platform for pygame-fbgui is a SBC with a small display. You
should install and configure the display according to the vendor. Usually
this is a matter of adding some entries to `/boot/config.txt` and
`/boot/cmdline.txt`.

Touch support typically needs the packages `tslib` and `libts-bin`.

Installation
------------

On Debian based systems, you can just run

    git clone https://github.com/bablokb/pygame-fbgui.git
    cd pygame-fbgui
    sudo tools/install

On other systems, you should inspect `tools/install` and adapt it to your needs.
The install-command basically copies the library and installs prerequisites
(currently only python3-pygame).


System Configuration
--------------------

For X11, no additional system-configuration should be necessary. You can
test the library by running one of the demo programs:

    /usr/local/lib/fbgui/demo/buttons.py

The program displays a simple gui with four buttons. Try to press each
button and see what happens.

If you are running the program from a console window (Raspbian-lite, direct
login - not via ssh) with a normal monitor attached, you must either install
"gpm" (console-mouse support) or add the following line to the configuration
of `buttons.py` (near the end of the program):

    config.mouse_dev = None

For small touch displays, you would install and configure the display
according to the instructions of your vendor. This usually includes the
installation of the packages `tslib` and `libts-bin`. You should also
calibrate the touch device on the console using `ts_calibrate`.

Since Debian-Jessie one of pygames low-level support-libraries (SDL) has a
problem using the touchscreen-library `tslib`. Therefore, you need to
downgrade this library to the version used in Debian-Wheezy:

    sudo tools/sdl-downgrade.sh

This script is from Adafruit, you will find a link to the source-page in
the script-header. Note that downgrading is not necessary on the development
system (X11 does not use `tslib`).

If pygame-fbgui does not identify your touch-device, you might have to add
an udev-rule to your system. In this case, copy `98-touchscreen.rules`
from the directory `support/etc/udev/rules.d` to `/etc/udev/rules.d`.
Check your system-log (`/var/log/messages`) and adapt the "name" in the
rule to the string from your system-log.


Running pygame-fbgui as a systemd-service
-----------------------------------------

To run a pygame-fbgui program as a systemd-service, you should copy the
template `support/etc/systemd/system/fbguidemo.service` to
`/etc/systemd/system/` and adapt it to your needs.


Documentation
-------------

You should read the [User's Guide](doc/usersguide.md "User's Guide") for
a quick start. Also, read the [Reference](doc/reference.md "Reference")
and browse through the demo-programs from the
[demo directory](files/usr/local/lib/fbgui/demo/ "demo directory").
