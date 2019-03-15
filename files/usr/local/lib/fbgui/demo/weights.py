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

import sys, os, datetime, glob

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
  add_lines(main)
  add_labels(main)
  add_images(main)
  return main

# ----------------------------------------------------------------------------

def add_panels(parent):
  """ add HBox with panels """

  # add a full-size HBox
  hbox = fbgui.HBox("hbox_panels",
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

def add_lines(parent):
  """ add HBox with lines """

  # add HBox
  hbox = fbgui.HBox("hbox_lines",
                      settings=fbgui.Settings({
                      'margins': 5,
                      'padding': 30,
                      'width': 1.0,
                      'height': 30,
                      'bg_color': fbgui.Color.SILVER,
                      'align':    (fbgui.CENTER,fbgui.TOP),
                      }),parent=parent)
  # add two lines
  line1 = fbgui.Line("id_line1",
                     settings=fbgui.Settings({
                       'width': 0.25,
                       'weight': 1,
                       'fg_color' : fbgui.Color.RED,
                       'align':     fbgui.CENTER,
                       }),parent=hbox)
  line2 = fbgui.Line("id_line2",
                     settings=fbgui.Settings({
                       'width': 0.25,
                       'weight': 2,
                       'fg_color' : fbgui.Color.BLUE,
                       'align':     fbgui.CENTER,
                       }),parent=hbox)

# ----------------------------------------------------------------------------

def add_labels(parent):
  """ add HBox with labels """

  # add HBox
  hbox = fbgui.HBox("hbox_labels",
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
                       'align':     (fbgui.CENTER,fbgui.BOTTOM),
                       }),parent=hbox)
  txt2 = fbgui.Label("id_txt2","a small",
                     settings=fbgui.Settings({
                       'width': 0.25,
                       'font_size': FONT_MEDIUM,
                       'bg_color' : fbgui.Color.GREEN080,
                       'align':     (fbgui.RIGHT,fbgui.CENTER),
                       }),parent=hbox)
  txt3 = fbgui.Label("id_txt3","and long text",
                     settings=fbgui.Settings({
                       'weight': 2,
                       'bg_color' : fbgui.Color.BLUE080,
                       'font_size': FONT_LARGE,
                       }),parent=hbox)

# ----------------------------------------------------------------------------

def add_images(parent):
  """ add images """

  # add HBox
  hbox = fbgui.HBox("hbox_images",
                      settings=fbgui.Settings({
                      'margins': 5,
                      'padding': 30,
                      'width': 1.0,
                      'height': 80,
                      'bg_color': fbgui.Color.SILVER,
                      'align':    (fbgui.CENTER,fbgui.TOP),
                      }),parent=parent)

  images = glob.glob(os.path.join(os.path.dirname(sys.argv[0]),"*.png"))
  index = 0
  for img in images:
    settings = fbgui.Settings({
      'width': 40,
      'height': 40,
      'scale': False,
      'weight': 1,
      'align': (fbgui.CENTER,fbgui.CENTER),
      })
    if index % 2:
      settings.scale = True
    fbgui.Image("img_%d" % index,img=img,
                settings=settings,parent=hbox)
    index += 1


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
