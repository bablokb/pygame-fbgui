#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Testprogram buttons.
#
# The program tests the rendering of buttons.
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
  # add VBox
  vbox = fbgui.VBox("vbox",
                      settings=fbgui.Settings({
                      'margins': 20,
                      'padding': 2,
                      'align':    (fbgui.CENTER,fbgui.TOP),
                      }),parent=main)

  # add four buttons
  colors = [fbgui.Color.RED,fbgui.Color.GREEN,fbgui.Color.YELLOW,fbgui.Color.BLUE]
  text   = ["play","pause","stop","record"]
  images = ["play.png","pause.png","stop.png","record.png"]
  attribs = zip(colors,text,images)
  index   = 1
  for color,text,image in attribs:
    image = os.path.join(PGM_DIR,image)
    fbgui.Button("btn_%d"% index,img=image,text=text,
                      settings=fbgui.Settings({
                        'font_size': FONT_MEDIUM,
                        'bg_color':  color,
                        'align':     fbgui.CENTER,
                      }),parent=vbox)
    index += 1
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