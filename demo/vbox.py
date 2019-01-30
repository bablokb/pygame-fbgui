#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Testprogram fbgui-vbox.
#
# The program tests the layout of various labels within a VBox.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import sys, os, datetime

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
  # add VBox
  vbox = fbgui.VBox("vbox",
                      settings=fbgui.Settings({
                      'margins': 5,
                      'padding': 2,
                      'bg_color': fbgui.Color.SILVER,
                      'align':    (fbgui.LEFT,fbgui.TOP),
                      }))
  main.add(vbox)

  # add three texts
  txt1 = fbgui.Label("id_txt1","this is",
                      settings=fbgui.Settings({
                      'font_size': FONT_SMALL,
                      'bg_color' : fbgui.Color.RED080,
                      'align':     fbgui.LEFT,
                      }))
  vbox.add(txt1)
  txt2 = fbgui.Label("id_txt2","a small",
                      settings=fbgui.Settings({
                      'font_size': FONT_MEDIUM,
                      'bg_color' : fbgui.Color.GREEN080,
                      'align':     fbgui.CENTER,
                      }))
  vbox.add(txt2)
  txt3 = fbgui.Label("id_txt1","and long text",
                      settings=fbgui.Settings({
                      'bg_color' : fbgui.Color.SILVER,
                      'font_size': FONT_LARGE,
                      'align':     fbgui.RIGHT,
                      }))
  vbox.add(txt3)
  return main

# ----------------------------------------------------------------------------


if __name__ == '__main__':

  config           = fbgui.Settings()
  config.msg_level = "DEBUG"
  config.bg_color  = BG_COLOR
  config.font_size = FONT_MEDIUM
  config.width     = WIDTH
  config.height    = HEIGHT
  config.title     = "Test VBox"

  app   = fbgui.App(config)
  panel = get_widgets()
  panel.pack()

  app.set_widget(panel)
  app.run()
