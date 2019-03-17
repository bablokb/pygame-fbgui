#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# The program tests the rendering of equal-sized buttons.
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
                      settings=fbgui.Settings({
                       'bg_color': fbgui.Color.GRAY090,
                       'margins': (10,10,10,10)}),
                      toplevel=True)

  box = fbgui.HBox("button_box",
                   settings=fbgui.Settings({
                     'bg_color': fbgui.Color.SILVER,
                     'uniform': True,
                     'width': 1.0,
                     'padding': 10,
                     'align': fbgui.CENTER
                     }),parent=main)

  fbgui.Button("btn_red",None,"Off",
                 settings=fbgui.Settings({
                   'bg_color': fbgui.Color.RED
                   }),parent=box)
    
  fbgui.Button("btn_green",None,"Standby",
                 settings=fbgui.Settings({
                   'bg_color': fbgui.Color.GREEN
                   }),parent=box)
    
  fbgui.Button("btn_yellow",None,"Kodi",
                 settings=fbgui.Settings({
                   'bg_color': fbgui.Color.YELLOW
                   }),parent=box)
    
  fbgui.Button("btn_blue",None,"Switch mode",
                 settings=fbgui.Settings({
                   'bg_color': fbgui.Color.BLUE
                   }),parent=box)
  return main

# ----------------------------------------------------------------------------


if __name__ == '__main__':

  config           = fbgui.Settings()
  config.msg_level = "TRACE"
  config.bg_color  = BG_COLOR
  config.font_size = FONT_MEDIUM
  config.width     = WIDTH
  config.height    = HEIGHT
  config.title     = "Test equally sized buttons"

  app   = fbgui.App(config)
  panel = get_widgets()
  panel.pack()

  app.set_widget(panel)
  app.run()
