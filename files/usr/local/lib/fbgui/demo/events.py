#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Testprogram events.
#
# The program tests layout-events
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

  def __init__(self,settings=fbgui.Settings()):
    """ constructor """

    super(MyApp,self).__init__(settings=settings)
    self._stop_event = threading.Event()

    panel,self.number_label = self.get_widgets()
    panel.pack()
    self.set_widget(panel)

  # -------------------------------------------------------------------------

  def get_widgets(self):
    """ create widget-tree """
    
    main = fbgui.Panel("main",
                      settings=fbgui.Settings({'margins': (10,10,10,10)}),
                      toplevel=True)
    # add HBox
    hbox = fbgui.HBox("hbox",
                      settings=fbgui.Settings({
                      'margins': 5,
                      'padding': 30,
                      'bg_color': fbgui.Color.SILVER,
                      'align':    (fbgui.CENTER,fbgui.CENTER),
                      }),parent=main)
    main.add(hbox)

    # and text
    label = fbgui.Label("id_label","Number:",
                      settings=fbgui.Settings({
                      'font_size': FONT_LARGE,
                      }),parent=hbox)
    number = fbgui.Label("id_number","x",
                      settings=fbgui.Settings({
                      'font_size': FONT_LARGE,
                      }),parent=hbox)
    return main,number

  # -------------------------------------------------------------------------

  def update(self):
    n = 0
    while True:
      if self._stop_event.wait(1):
        break
      n += 1
      self.logger.msg("DEBUG","new value of n: %d" % n)
      self.number_label.set_text("%d" % n)

  # -----------------------------------------------------------------------

  def on_quit(self,rc=0):
    """ override base-class quit-method """

    rc = super(MyApp,self).on_quit(rc=rc)
    self._stop_event.set()
    sys.exit(rc)

  # ----------------------------------------------------------------------------

if __name__ == '__main__':

  config           = fbgui.Settings()
  config.msg_level = "TRACE"
  config.bg_color  = BG_COLOR
  config.font_name = "couriernew"
  config.font_size = FONT_LARGE
  config.width     = WIDTH
  config.height    = HEIGHT
  config.title     = "Test Events"

  myapp        = MyApp(config)

  # setup async-thread
  update_thread = threading.Thread(target=myapp.update)
  update_thread.start()

  myapp.run()
