#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Testprogram fbgui-panels.
#
# The program tests the layout of various sub-panels and of a horizontal
# and vertical line.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import sys, os, datetime

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]),"../.."))

import fbgui

# --- global constants   -----------------------------------------------------

FG_COLOR = fbgui.Color.BLACK
BG_COLOR = fbgui.Color.WHITE

FONT_SMALL = 12
FONT_LARGE = 24

WIDTH  = 800
HEIGHT = 600

# ----------------------------------------------------------------------------

def get_widgets():
  """ create widget-tree """

  colors = [
    fbgui.Color.RED,
    fbgui.Color.GREEN,
    fbgui.Color.BLUE,
    fbgui.Color.RED075,
    fbgui.Color.GREEN075,
    fbgui.Color.BLUE075,
    fbgui.Color.RED025,
    fbgui.Color.GREEN025,
    fbgui.Color.BLUE025
    ]

  main = fbgui.Panel("main",
                      settings=fbgui.Settings({'margins': (5,5,5,5)}),
                      toplevel=True)
  # add child panels
  color = 0
  for valign in [fbgui.TOP,fbgui.CENTER,fbgui.BOTTOM]:
    for halign in [fbgui.LEFT,fbgui.CENTER,fbgui.RIGHT]:
      config = fbgui.Settings({
        'width'     : 80,
        'height'    : 40,
        'bg_color'  : colors[color],
        'align'     : (halign,valign)
        })
      box = fbgui.Panel("box%d" % color,settings=config,parent=main)
      color += 1

  # add child lines
  config = fbgui.Settings({
    'width'      : 1.0,
    'height'     : 0,
    'fg_color'   : fbgui.Color.BLACK,
    'align'      : fbgui.CENTER,
    'orientation': fbgui.HORIZONTAL 
        })
  line = fbgui.Line("hline",settings=config,parent=main)

  config.width       = 0
  config.height      = 1.0
  config.orientation = fbgui.VERTICAL
  line = fbgui.Line("vline",settings=config,parent=main)

  return main

# ----------------------------------------------------------------------------


if __name__ == '__main__':

  config           = fbgui.Settings()
  config.msg_level = "TRACE"
  config.bg_color  = BG_COLOR
  config.width     = WIDTH
  config.height    = HEIGHT
  config.title     = "Test Panels"

  app   = fbgui.App(config)
  panel = get_widgets()
  panel.pack()

  app.set_widget(panel)
  app.run()
