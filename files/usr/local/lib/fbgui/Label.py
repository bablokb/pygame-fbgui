#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# A label widget.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import pygame.freetype

import fbgui

class Label(fbgui.Widget):
  """ draw a text """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,text,settings=fbgui.Settings(),toplevel=False,parent=None):
    """ constructor """

    super(Label,self).__init__(id,settings=settings,
                               toplevel=toplevel,parent=parent)

    if not hasattr(self.theme,"font"):
      if (self.theme.font_size != fbgui.App.theme.font_size or
          self.theme.font_name != fbgui.App.theme.font_name):
        self.theme.font = fbgui.App.create_font(self.theme.font_name,
                                                  self.theme.font_size,
                                                self.theme.font_path)
      else:
        fbgui.App.logger.msg("TRACE","using default font for label: %s" %
                             self._id)
        self.theme.font = self.theme.default_font

    self._text = None
    self._rect = pygame.Rect(0,0,0,0)
    self.set_text(text,refresh=False)

  # --- set the text of this label   -----------------------------------------

  def set_text(self,text,refresh=True):
    """ set the text of the label """

    if text == self._text:
      return
    fbgui.App.logger.msg("TRACE","changing text of label %s" % self._id)

    self._text = text
    if self._text:
      self._rect = self.theme.font.get_rect(self._text)
    else:
      self._rect = pygame.Rect(0,0,0,0)

    if refresh:
      if ( self._rect.w != self.screen.w or
           self._rect.h != self.screen.h or
           fbgui.Color.eq(self.bg_color,fbgui.Color.TRANSPARENT)):
        # size changed, so post a layout-event
        self.post_layout()
      else:
        # only content changed, so post a redraw-event
        self.post_redraw()
      
  # --- get the text of this label   -----------------------------------------

  def get_text(self):
    """ return the text of the label """
    return self._text

  # --- query minimum size   -------------------------------------------------

  def _calc_minimum_size(self,w,h):
    """ query minimum size of widget """

    if self._is_size_valid:
      return

    super(Label,self)._calc_minimum_size(w,h)
    if not self._text:
      return

    if self.w_min == 0:
      self.w_min = self._rect.w
    if self.h_min == 0:
      self.h_min = self._rect.h

    fbgui.App.logger.msg("TRACE",
                   "min_size (%s): (%d,%d)" % (self._id,self.w_min,self.h_min))

    self._is_size_valid = True

  # --- redraw widget   ------------------------------------------------------

  def draw(self,surface=None):
    """ draw the widget """

    # surface is None for redraw events, so save surface
    if surface is not None:
      self._surface = surface

    # if the widget has a size, fill with background color
    if self.screen.w > 0 and self.screen.h > 0:
      if not self._parent or ( self.bg_color.a > 0 and
                       fbgui.Color.neq(self.bg_color,self._parent.bg_color) ):
        self._surface.fill(self.bg_color,
               rect=(self.screen.x,self.screen.y,self.screen.w,self.screen.h))

    # now render the font
    if self._rect.w > 0 and self._rect.h > 0:
      # align the label on it's drawing area
      pos = self._align(self._rect)
      self._clip_push()
      surface, _ = self.theme.font.render(self._text,
                                                 self.fg_color,self.bg_color)
      self._surface.blit(surface,pos)
      self._clip_pop()
