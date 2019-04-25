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
  2. [Installation](#install "Installation")
  3. [Documentation](#documentation "Documentation")


News
----

### April 2019 ###

  - Core widgets available
  - Border layout and flow layouts implemented
  - Support for mouse-events


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


Documentation
-------------

You should read the [User's Guide](doc/usersguide.md "User's Guide") for
a quick start. Also, read the [Reference](doc/reference.md "Reference")
and browse through the demo-programs from the
[demo directory](files/usr/local/lib/fbgui/demo/ "demo directory").
