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

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,img=None,text=None,
               settings=fbgui.Settings(),toplevel=False,parent=None):
    """ constructor """

    settings.padding = getattr(settings,'padding',5)
    settings.margins = getattr(settings,'margins',10)
    super(Button,self).__init__(id,settings=settings,
                              toplevel=toplevel,parent=parent)


    self._img = None     # image filename
    self._Image = None   # Image widget

    self._text  = None   # button text
    self._Label = None   # Label widget

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
