#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Testprogram for lists.
#
# The program tests the rendering of lists.
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
BG_COLOR = fbgui.Color.RED075

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

  # add a list at the top
  labels = [ fbgui.Label('id1',"first item"),
             fbgui.Label('id2',"second item"),
             fbgui.Label('id3',"third item")]
  for label in labels:
    label.on_click = lambda widget,event: on_click(widget,event)
  
  list1 = fbgui.List("list1",labels,
                      settings=fbgui.Settings({
                       'margins':  5,
                       'bg_color': fbgui.Color.BLUE,
                       'fg_color': fbgui.Color.WHITE,
                       'align': (fbgui.CENTER,fbgui.TOP),
                      }),parent=main)

  return main

# ----------------------------------------------------------------------------

def on_click(widget,event):
  """ click-event handler for list-items """

  global app
  app.logger.msg("DEBUG","running on_click-handler for %s" % widget.id())

# ----------------------------------------------------------------------------


if __name__ == '__main__':

  config           = fbgui.Settings()
  config.msg_level = "TRACE"
  config.bg_color  = BG_COLOR
  config.font_size = FONT_MEDIUM
  config.width     = WIDTH
  config.height    = HEIGHT
  config.title     = "Test Lists"

  app   = fbgui.App(config)
  panel = get_widgets()
  panel.pack()
  app.set_widget(panel)
  app.run()
