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
BG_COLOR = fbgui.Color.WHITE

FONT_SMALL  = 12
FONT_MEDIUM = 24
FONT_LARGE  = 48

WIDTH  = 800
HEIGHT = 600

# ----------------------------------------------------------------------------

class ListItem(fbgui.HBox):
  """ an item with two childs """

  counter = 0
  def __init__(self):
    """ constructor """
    ListItem.counter += 1
    id = "Item_%d" % ListItem.counter
    super(ListItem,self).__init__(id,
                                  settings=fbgui.Settings({
                                    'width': 1.0,
                                    'align': fbgui.CENTER,
                                    'radius': 0.2,
                                    'margins': 2,
                                    'padding': 2
                                    }))
    # add first child (big number)
    font_size = fbgui.App.theme.font_size * 2
    fbgui.Label("label_%d" % ListItem.counter,
                "%d" % ListItem.counter,
                settings=fbgui.Settings({
                  'width': 0.05,
                  'align': fbgui.RIGHT,
                  'font_size': font_size
                }),parent=self)

    # add second child (Text)
    text = "First line of item %d\nSecond line of item %d" % (
                                          ListItem.counter, ListItem.counter)
    fbgui.Text("text_%d" % ListItem.counter,text,parent=self)

# ----------------------------------------------------------------------------

def create_scroll_box(parent,widget):
  """ create the scroll-box for the list """

  bbox = fbgui.VBox("list2_bbox",
                    settings=fbgui.Settings({
                      'height': 1.0,
                       'bg_color': fbgui.Color.GRAY090,
                      }),
                    parent=parent)
  prev_button = fbgui.Button("prev",text="^",parent=bbox)
  prev_button.list = widget
  prev_button.on_click = on_up
  fbgui.VGap("prev",settings=fbgui.Settings({'weight': 1}),parent=bbox)
  next_button = fbgui.Button("next",text="v",parent=bbox)
  next_button.list = widget
  next_button.on_click = on_down

# ----------------------------------------------------------------------------

def get_widgets():
  """ create widget-tree """
    
  main = fbgui.Panel("main",
                      settings=fbgui.Settings({'margins': (10,10,10,10)}),
                      toplevel=True)

  # add a info-label
  global info
  info = fbgui.Label("info","please select an item",
                      settings=fbgui.Settings({
                       'width': 1.0,
                       'bg_color': fbgui.Color.GRAY,
                       'fg_color': fbgui.Color.WHITE,
                      'align':    (fbgui.LEFT,fbgui.BOTTOM),
                      }),parent=main)

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
  list1.on_selection_changed = lambda widget: on_selection_changed(widget)

  # add a list at the center with scroll-buttons
  hbox  = fbgui.HBox("list2_hbox",
                     settings=fbgui.Settings({
                       'margins':  2,
                       'height': 0.5,
                       'bg_color': fbgui.Color.BLUE,
                       'align': (fbgui.CENTER,fbgui.CENTER)}),
                       parent=main)

  items = [ ListItem() for i in range(8) ]
  
  list2 = fbgui.List("list2",items,
                      settings=fbgui.Settings({
                       'multiselect': True,
                       'weight': 1,
                       'bg_color': fbgui.Color.BLUE,
                       'fg_color': fbgui.Color.WHITE,
                       'align': (fbgui.CENTER,fbgui.TOP)
                      }),parent=hbox)
  list2.on_selection_changed = lambda widget: on_selection_changed(widget)
  create_scroll_box(hbox,list2)

  return main

# ----------------------------------------------------------------------------

def on_up(widget,event):
  """ prev button of list """

  app.logger.msg("DEBUG","scroll list up")
  widget.list.dec_offset()
  widget.post_layout()

# ----------------------------------------------------------------------------

def on_down(widget,event):
  """ next button of list """

  app.logger.msg("DEBUG","scroll list down")
  widget.list.inc_offset()
  widget.post_layout()

# ----------------------------------------------------------------------------

def on_click(widget,event):
  """ click-event handler for list-items """

  global app
  app.logger.msg("DEBUG","running on_click-handler for %s" % widget.id())

# ----------------------------------------------------------------------------

def on_selection_changed(widget):
  """ on selection changed event """

  global app,info
  if isinstance(widget,list):
    text = ", ".join([ w.id() for w in widget ])
  else:
    if widget:
      text = widget.id()
    else:
      text = "none"
  app.logger.msg("DEBUG","selected items: %s" % text)
  info.set_text("selected items: %s" % text,refresh=True)

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
