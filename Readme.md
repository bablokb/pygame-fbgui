Framebuffer GUI for Pygame
==========================

Pygame-fbgui is a python3 GUI library based on pygame for small framebuffer 
devices. It supports various layouts and provides a number of standard widgets
like panels, texts, labels and buttons.

The library is under constant development. Implementation is not complete,
but everything implemented should work (if not, then it's a bug).

Although targeted at small framebuffer displays, it also works under X11. In
fact, development is done using X11.


Table of Contents
-----------------

  1. [News and Status](#news "News")
  2. [Hardware](#install "Hardware")
  3. [Installation](#install "Installation")
  4. [Documentation](#documentation "Documentation")


News
----

### April 2019 ###

  - Core widgets available
  - Border layout and flow layouts implemented
  - Support for mouse-events


Hardware
--------

You don't need additional steps if you install pygame-fbgui on your
development system - pygame-fbgui works fine with X11. Windows users
will probably have to tweak the class `App` (feedback and pull-requests
on this issue is welcome).

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

You will also find in the directories below `support` various sample-files,
e.g. udev-rules for configuring the touch-device or a sample systemd
unit-file. Copy these files or use them as templates.

Since Debian-Jessie one of pygames low-level support-libraries (SDL) has a
problem using the touchscreen-library `tslib`. Therefore, you need to
downgrade this library to the version used in Debian-Wheezy:

    sudo tools/sdl-downgrade.sh

This script is from Adafruit, you will find a link to the source-page in
the script-header. Note that downgrading is not necessary on the development
system (X11 does not use `tslib`).


Documentation
-------------

You should read the [User's Guide](doc/usersguide.md "User's Guide") for
a quick start. Also, read the [Reference](doc/reference.md "Reference")
and browse through the demo-programs from the
[demo directory](files/usr/local/lib/fbgui/demo/ "demo directory").
