#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Sample GUI for a mediaplayer.
#
# The program only implements the gui, not the complete player logic.
#
# Icons are from the GTK-distribution.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import fbgui

# ----------------------------------------------------------------------------

def get_gui():
  """ create GUI-elements """
    
  vbox = fbgui.VBox("main",
                      settings=fbgui.Settings({
                      'margins': 10,
                      'padding': 2
                      }),toplevel=True)
  # first HBox
  zeile1 = fbgui.HBox("img_and_title",
                      settings=fbgui.Settings({
                       'bg_color': fbgui.Color.CORNFLOWERBLUE,
                       'radius': 0.1,
                       'margins': 5,
                       'padding': 5,
                       'width': 1.0,   # 100%
                       'weight': (0,1),
                      'align':   fbgui.LEFT,
                      }),parent=vbox)

  # elements of the first HBox
  bild  = fbgui.Image("cover", img="music.png",
                      settings=fbgui.Settings({
                        'align': fbgui.CENTER,
                        'min_size': (50,50),
                        'scale': True,
                      }),parent=zeile1)

  titel = fbgui.Label("title","Money for Nothing ...",
                      settings=fbgui.Settings({
                        'weight': 1,
                        'align':  (fbgui.LEFT,fbgui.CENTER),
                      }),parent=zeile1)

  # second HBox
  zeile2 = fbgui.HBox("buttons1",
                      settings=fbgui.Settings({
                       'margins': 2,
                       'padding': 1,
                       'uniform': True,
                       'width': 1.0,   # 100%
                       'align':   fbgui.CENTER,
                      }),parent=vbox)

  # add buttons
  liste = [ ("pause.png",do_pause), ("start.png",do_start),
                                            ("stop.png",do_stop)]
  for icon,methode in liste:
    btn = fbgui.Button("%s"% icon,img=icon,
                      settings=fbgui.Settings({
                         'margins': 5,
                         'padding': 1,
                         'bg_color': fbgui.Color.CORNFLOWERBLUE
                      }),parent=zeile2)
    btn.on_click = methode

  # third HBox
  zeile3 = fbgui.HBox("buttons2",
                      settings=fbgui.Settings({
                       'margins': 2,
                       'padding': 1,
                       'uniform': True,
                       'width': 1.0,   # 100%
                       'align':   fbgui.CENTER,
                      }),parent=vbox)

  # add buttons
  liste = [("skip-backward.png",do_skip_back),
           ("seek-backward.png",do_seek_back),
           ("seek-forward.png",do_seek_fwd),
           ("skip-forward.png",do_skip_fwd)]
  for icon,methode in liste:
    btn = fbgui.Button("%s"% icon,img=icon,
                      settings=fbgui.Settings({
                         'margins': 5,
                         'padding': 1,
                         'bg_color': fbgui.Color.CORNFLOWERBLUE,
                         'weight': 1
                      }),parent=zeile3)
    btn.on_click = methode

  # return toplevel-element
  return vbox

# ----------------------------------------------------------------------------

def  do_pause(widget,event):
  """ process button-click """

  fbgui.App.logger.msg("DEBUG","click for %s: %r" % (widget._id,event))
  return True

def  do_start(widget,event):
  """ process button-click """

  fbgui.App.logger.msg("DEBUG","click for %s: %r" % (widget._id,event))
  return True

def  do_stop(widget,event):
  """ process button-click """

  fbgui.App.logger.msg("DEBUG","click for %s: %r" % (widget._id,event))
  return True

def  do_skip_back(widget,event):
  """ process button-click """

  fbgui.App.logger.msg("DEBUG","click for %s: %r" % (widget._id,event))
  return True

def  do_seek_back(widget,event):
  """ process button-click """

  fbgui.App.logger.msg("DEBUG","click for %s: %r" % (widget._id,event))
  return True

def  do_seek_fwd(widget,event):
  """ process button-click """

  fbgui.App.logger.msg("DEBUG","click for %s: %r" % (widget._id,event))
  return True

def  do_skip_fwd(widget,event):
  """ process button-click """

  fbgui.App.logger.msg("DEBUG","click for %s: %r" % (widget._id,event))
  return True

# ----------------------------------------------------------------------------


if __name__ == '__main__':

  config            = fbgui.Settings()
  config.msg_level  = "DEBUG"
  config.msg_syslog = False
  config.fg_color   = fbgui.Color.BLACK
  config.bg_color   = fbgui.Color.BLACK
  config.font_size  = 24
  config.width      = 320
  config.height     = 240
  config.title      = "Mediaplayer"

  app   = fbgui.App(config)
  topbox = get_gui()
  topbox.pack()

  app.set_widget(topbox)
  app.run()
