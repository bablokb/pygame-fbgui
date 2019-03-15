#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Testprogram for images. The program expects a list of images on the
# commandline.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import sys, os, datetime, threading, signal
import pygame

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]),"../.."))

import fbgui

# --- global constants   -----------------------------------------------------

FG_COLOR = fbgui.Color.BLACK
BG_COLOR = fbgui.Color.WHITE

FONT_SMALL  = 12
FONT_MEDIUM = 24
FONT_LARGE  = 48

WIDTH  = 800
HEIGHT = 600

# ----------------------------------------------------------------------------

class MyApp(fbgui.App):
  """ subclass of App for this application """

  # -------------------------------------------------------------------------

  def __init__(self,images,settings=fbgui.Settings()):
    """ constructor """

    super(MyApp,self).__init__(settings=settings)
    self._images     = images
    self._stop_event = threading.Event()

    panel = self.get_widgets()
    panel.pack()
    self.set_widget(panel)

  # -------------------------------------------------------------------------

  def get_widgets(self):
    """ create widget-tree """
    
    main = fbgui.Panel("main",
                      settings=fbgui.Settings({'margins': (10,10,10,10)}),
                      toplevel=True)
    # add Image
    self._img_widget = fbgui.Image("img",img=None,
                      settings=fbgui.Settings({
                        'width': 600,
                        'height': 200,
                        'scale': False,             
                        'align': (fbgui.CENTER,fbgui.CENTER),
                      }),parent=main)
    return main

  # -------------------------------------------------------------------------

  def update(self):
    n = -1
    total = len(self._images)
    while True:
      n = (n+1) % total
      self.logger.msg("DEBUG","image: %s" % self._images[n])
      self._img_widget.set_image(self._images[n],refresh=True)
      if self._stop_event.wait(3):
        break

  # -----------------------------------------------------------------------

  def on_start(self):
    """ override base-class on_start-method """
    # setup async-thread
    update_thread = threading.Thread(target=myapp.update)
    update_thread.start()

  # -----------------------------------------------------------------------

  def on_quit(self):
    """ override base-class quit-method """

    super(MyApp,self).on_quit()
    self._stop_event.set()
    sys.exit(0)

  # ----------------------------------------------------------------------------

if __name__ == '__main__':

  if len(sys.argv) < 2:
    print("usage: %s image [...]" % sys.argv[0])
    sys.exit(3)

  config           = fbgui.Settings()
  config.msg_level = "TRACE"
  config.bg_color  = BG_COLOR
  config.font_name = "couriernew"
  config.font_size = FONT_LARGE
  config.width     = WIDTH
  config.height    = HEIGHT
  config.title     = "Test class Image"

  myapp = MyApp(sys.argv[1:],config)
  myapp.run()
