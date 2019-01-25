#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# A label widget.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import pygame.freetype

import fbgui

class Label(fbgui.Widget):
  """ draw a text """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,text,settings=None,toplevel=False):
    """ constructor """

    super(Label,self).__init__(id,settings=settings,toplevel=toplevel)
    if not hasattr(self.theme,"font"):
      if (self.theme.font_size != fbgui.App.theme.font_size or
          self.theme.font_name != fbgui.App.theme.font_name):
        fbgui.App.logger.msg("DEBUG","creating font: %s (%dpt)" %
                             (self.theme.font_name,self.theme.font_size))
        self.theme.font = pygame.freetype.SysFont(self.theme.font_name,
                                                  self.theme.font_size)
      else:
        fbgui.App.logger.msg("DEBUG","using default font")
        self.theme.font = self.theme.default_font

    self.set_text(text)

  # --- set the text of this label   -----------------------------------------

  def set_text(self,text,font=None):
    """ set the text of the label """

    self._text = text
    if self._text:
      self._surface, self._rect = self.theme.font.render(self._text,
                                      self.theme.fg_color,self.theme.bg_color)
    else:
      self._surface = None
      self._rect    = None
      
  # --- query minimum size   -------------------------------------------------

  def _minimum_size(self,w,h):
    """ query minimum size of widget """

    (w_min,h_min) = super(Label,self)._minimum_size(w,h)
    if not self._text:
      return (w_min,h_min)

    if w_min == 0:
      w_min = self._rect.w
    if h_min == 0:
      h_min = self._rect.h

    fbgui.App.logger.msg("DEBUG","min_size (%s): (%d,%d)" % (self._id,w_min,h_min))
    return (w_min,h_min)

  # --- redraw widget   ------------------------------------------------------

  def draw(self):
    """ draw the widget """

    if self._surface:
      fbgui.App.display.screen.blit(self._surface,
                                    (self.screen.x,self.screen.y))
    else:
      # if the widget has a size, just fill with background color
      if self.screen.w > 0 and self.screen.h > 0:
        if not self._parent or ( self.theme.bg_color !=
                                 self._parent.theme.bg_color ):
          fbgui.App.display.screen.fill(self.theme.bg_color,
               rect=(self.screen.x,self.screen.y,self.screen.w,self.screen.h))
