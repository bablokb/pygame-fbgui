#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Testprogram events.
#
# The program tests layout-events
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import sys, os, datetime, threading, signal

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

def get_widgets():
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
                      }))
  main.add(hbox)

  # and text
  label = fbgui.Label("id_label","Number:",
                      settings=fbgui.Settings({
                      'bg_color': fbgui.Color.SILVER,
                      'font_size': FONT_LARGE,
                      }))
  hbox.add(label)
  number = fbgui.Label("id_number","x",
                      settings=fbgui.Settings({
                      'bg_color': fbgui.Color.SILVER,
                      'font_size': FONT_LARGE,
                      }))
  hbox.add(number)
  return main,number

# ----------------------------------------------------------------------------

def update(stop,number):
  n = 0
  global app
  while True:
    if stop.wait(1):
      break
    n += 1
    app.logger.msg("DEBUG","new value of n: %d" % n)
    number.set_text("%d" % n)
    
# --------------------------------------------------------------------------

def signal_handler(_signo, _stack_frame):
  """ Signal-handler to cleanup threads """

  global stop
  stop.set()
  sys.exit(0)

# ----------------------------------------------------------------------------

if __name__ == '__main__':

  config           = fbgui.Settings()
  config.msg_level = "DEBUG"
  config.bg_color  = BG_COLOR
  config.font_size = FONT_MEDIUM
  config.width     = WIDTH
  config.height    = HEIGHT
  config.title     = "Test Events"

  app          = fbgui.App(config)
  panel,number = get_widgets()
  panel.pack()
  app.set_widget(panel)

  # setup signal handlers
  signal.signal(signal.SIGTERM, signal_handler)
  signal.signal(signal.SIGINT, signal_handler)

  # setup async-thread
  stop = threading.Event()
  update_thread = threading.Thread(target=update,args=(stop,number))
  update_thread.start()

  app.run()
  stop.set()
  app.quit()
