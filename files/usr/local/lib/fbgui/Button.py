#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Class Button: a HBox with an image and a label (both optional)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import fbgui

class Button(fbgui.HBox):
  """ Horizontal box """

  NORMAL = 0
  HOVER  = 1
  DOWN   = 2

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,img=None,text=None,
               settings=fbgui.Settings(),toplevel=False,parent=None):
    """ constructor """

    settings.padding = getattr(settings,'padding',5)
    settings.margins = getattr(settings,'margins',10)
    super(Button,self).__init__(id,settings=settings,
                              toplevel=toplevel,parent=parent)

    # add default handlers
    if not self._on_mouse_motion:
      self._on_mouse_motion = self.on_mouse_motion
    if not self._on_mouse_btn_down:
      self._on_mouse_btn_down = self.on_mouse_btn_down
    if not self._on_mouse_btn_up:
      self._on_mouse_btn_up = self.on_mouse_btn_up

    self._img = None     # image filename
    self._Image = None   # Image widget

    self._text  = None   # button text
    self._Label = None   # Label widget

    # state of button
    self._state = Button.NORMAL

    self.set_image(img,refresh=False)
    self.set_text(text,refresh=False)

  # --- set the image of this Button   ---------------------------------------

  def set_image(self,img,refresh=True):
    """ set the image of the button """

    if img == self._img:
      return
    fbgui.App.logger.msg("TRACE","changing image of Button %s" % self._id)

    if img:
      if self._Image:
        self._Image.set_image(refresh=refresh)
      else:
        settings = fbgui.Settings(self._settings)
        settings.width  = 0
        settings.height = 0
        self._Image = fbgui.Image(self._id+"_img",img=img,
                                  settings=settings,parent=self)

    self._img = img

  # --- set the text of this Button   ----------------------------------------

  def set_text(self,text,refresh=True):
    """ set the text of the button """

    if text == self._text:
      return
    fbgui.App.logger.msg("TRACE","changing image of Button %s" % self._id)

    if text:
      if self._Label:
        self._Label.set_text(refresh=refresh)
      else:
        settings = fbgui.Settings(self._settings)
        settings.width  = 0
        settings.height = 0
        self._Label = fbgui.Label(self._id+"_text",text,
                                  settings=settings,parent=self)

    self._text = text

  # --- handle mouse-motion events    ----------------------------------------

  def on_mouse_motion(self,event):
    """ handle mouse-motion events """

    if self._draw_rect.collidepoint(event.pos):
      fbgui.App.logger.msg("TRACE","on_mouse_motion for Button %s" % self._id)
      self._state = Button.HOVER
    else:
      self._state = Button.NORMAL
    return False

  # --- handle mouse-button down events    ----------------------------------

  def on_mouse_btn_down(self,event):
    """ handle mouse-button down events """

    if self._draw_rect.collidepoint(event.pos):
      fbgui.App.logger.msg("TRACE","on_mouse_btn_down for Button %s" % self._id)
      self._state = Button.DOWN
    return False

  # --- handle mouse-button up events    ------------------------------------

  def on_mouse_btn_up(self,event):
    """ handle mouse-button up events """

    if self._draw_rect.collidepoint(event.pos):
      fbgui.App.logger.msg("TRACE","on_mouse_btn_up for Button %s" % self._id)
      self._state = Button.NORMAL
    return False
