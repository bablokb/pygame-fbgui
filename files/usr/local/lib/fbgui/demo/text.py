#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Testprogram for text-areas.
#
# The program tests the rendering of text-areas.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import sys, os, datetime

PGM_DIR = os.path.dirname(sys.argv[0])
sys.path.append(os.path.join(PGM_DIR,"../.."))

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

  # add a text-box at the top
  txt1 = "The first line.\nThe second line.\n xxx \nThe fourth line."
  text1 = fbgui.Text("txt1",txt1,
                      settings=fbgui.Settings({
                       'margins':  5,
                       'bg_color': fbgui.Color.BLUE,
                       'fg_color': fbgui.Color.WHITE,
                       'rows': 3,
                       'align': (fbgui.CENTER,fbgui.TOP),
                      }),parent=main)

  # add a text-box at the bottom
  txt2 = "The first line.\nThe second line.\n xxx \nThe fourth line"
  text2 = fbgui.Text("txt2",txt2,
                      settings=fbgui.Settings({
                       'margins':  5,
                       'bg_color': fbgui.Color.BLUE,
                       'fg_color': fbgui.Color.WHITE,
                       'align': (fbgui.CENTER,fbgui.BOTTOM),
                      }),parent=main)
  return main

# ----------------------------------------------------------------------------


if __name__ == '__main__':

  config           = fbgui.Settings()
  config.msg_level = "TRACE"
  config.bg_color  = BG_COLOR
  config.font_size = FONT_MEDIUM
  config.width     = WIDTH
  config.height    = HEIGHT
  config.title     = "Test Buttons"

  app   = fbgui.App(config)
  panel = get_widgets()
  panel.pack()
  app.set_widget(panel)
  app.run()
