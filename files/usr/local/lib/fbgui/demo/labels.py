#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Testprogram fbgui-labels.
#
# The program tests the layout of various labels.
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

FONT_SMALL  = 12
FONT_MEDIUM = 24
FONT_LARGE  = 48

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

  labels = [
    "top-left",
    "top-center",
    "top-right",
    "center-left",
    "center-center",
    "center-right",
    "bottom-left",
    "bottom-center",
    "bottom-right"
    ]

  sizes = [
    FONT_SMALL,FONT_MEDIUM,FONT_LARGE,
    FONT_SMALL,FONT_MEDIUM,FONT_LARGE,
    FONT_SMALL,FONT_MEDIUM,FONT_LARGE
    ]
    
  main = fbgui.Panel("main",
                      settings=fbgui.Settings({'margins': (5,5,5,5)}),
                      toplevel=True)
  # add child panels
  index = 0
  for valign in [fbgui.TOP,fbgui.CENTER,fbgui.BOTTOM]:
    for halign in [fbgui.LEFT,fbgui.CENTER,fbgui.RIGHT]:
      config = fbgui.Settings({
        'fg_color'  : colors[index],
        'font_size' : sizes[index],
        'align'     : (halign,valign)
        })
      text = labels[index]
      if index == 1:
        # test background
        config.bg_color = fbgui.Color.GRAY090
      elif index == 4:
        # test empty label: fill with background
        text = ""
        config.bg_color = fbgui.Color.BLACK
        config.width    = 80
        config.height   = 40
      label = fbgui.Label("label-%d" % index,text,settings=config,parent=main)
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
  config.title     = "Test Panels"

  app   = fbgui.App(config)
  panel = get_widgets()
  panel.pack()

  app.set_widget(panel)
  app.run()
