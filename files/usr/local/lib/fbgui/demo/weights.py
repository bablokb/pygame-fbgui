#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Testprogram for weight-attribute.
#
# The program tests the layout of flexible panels within a HBox.
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
    
  main = fbgui.VBox("main",
                      settings=fbgui.Settings({
                      'margins': (10,10,10,10),
                      'padding': 20,
                      }),
                      toplevel=True)
  add_panels(main)
  add_labels(main)
  return main

# ----------------------------------------------------------------------------

def add_panels(parent):
  """ add HBox with panels """

  # add a full-size HBox
  hbox = fbgui.HBox("hbox",
                      settings=fbgui.Settings({
                      'margins': 5,
                      'padding': 30,
                      'width': 1.0,
                      'bg_color': fbgui.Color.SILVER,
                      'align':    (fbgui.CENTER,fbgui.TOP),
                      }),parent=parent)

  # add three panels
  panel1 = fbgui.Panel("id_panel1",
                      settings=fbgui.Settings({
                         'height': 20,
                         'weight': 1,
                         'bg_color' : fbgui.Color.RED080,
                         'align':     fbgui.BOTTOM,
                         }),parent=hbox)
  panel2 = fbgui.Panel("id_panel2",
                      settings=fbgui.Settings({
                         'height': 30,
                         'weight': 1,
                         'bg_color' : fbgui.Color.GREEN080,
                         'align':     fbgui.CENTER,
                         }),parent=hbox)
  panel3 = fbgui.Panel("id_panel3",
                       settings=fbgui.Settings({
                         'height': 40,
                         'weight': 2,
                         'bg_color' : fbgui.Color.BLUE080,
                         }),parent=hbox)

# ----------------------------------------------------------------------------

def add_labels(parent):
  """ add HBox with labels """

  # add HBox
  hbox = fbgui.HBox("hbox",
                      settings=fbgui.Settings({
                      'margins': 5,
                      'padding': 30,
                      'width': 1.0,
                      'bg_color': fbgui.Color.SILVER,
                      'align':    (fbgui.CENTER,fbgui.TOP),
                      }),parent=parent)

  # add three texts
  txt1 = fbgui.Label("id_txt1","this is",
                     settings=fbgui.Settings({
                       'width': 0.25,
                       'font_size': FONT_SMALL,
                       'bg_color' : fbgui.Color.RED080,
                       'align':     fbgui.BOTTOM,
                       }),parent=hbox)
  txt2 = fbgui.Label("id_txt2","a small",
                     settings=fbgui.Settings({
                       'width': 0.25,
                       'font_size': FONT_MEDIUM,
                       'bg_color' : fbgui.Color.GREEN080,
                       'align':     fbgui.CENTER,
                       }),parent=hbox)
  txt3 = fbgui.Label("id_txt3","and long text",
                     settings=fbgui.Settings({
                       'weight': 2,
                       'bg_color' : fbgui.Color.BLUE080,
                       'font_size': FONT_LARGE,
                       }),parent=hbox)

# ----------------------------------------------------------------------------


if __name__ == '__main__':

  config           = fbgui.Settings()
  config.msg_level = "TRACE"
  config.bg_color  = BG_COLOR
  config.font_size = FONT_MEDIUM
  config.width     = WIDTH
  config.height    = HEIGHT
  config.title     = "Test Weights"

  app   = fbgui.App(config)
  panel = get_widgets()
  panel.pack()

  app.set_widget(panel)
  app.run()
