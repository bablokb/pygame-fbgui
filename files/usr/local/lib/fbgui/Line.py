#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# A line widget.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import pygame.gfxdraw

import fbgui

class Line(fbgui.Widget):
  """ draw a line """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=None,toplevel=False,parent=None):
    """ constructor """

    super(Line,self).__init__(id,settings=settings,
                              toplevel=toplevel,parent=parent)
    self.orientation = getattr(settings,'orientation',fbgui.HORIZONTAL)

  # --- query minimum size   -------------------------------------------------

  def _calc_minimum_size(self,w,h):
    """ query minimum size of widget """

    if self._is_size_valid:
      return

    super(Line,self)._calc_minimum_size(w,h)
    if self.orientation == fbgui.HORIZONTAL:
      self.h_min = 1            # horizontal lines have height==1
      if self.w_min == 0:       # no explicit width, so
        self.w_min = 1          # use default (line is one pixel wide)
    else:
      self.w_min = 1            # vertical lines have width==1
      if self.h_min == 0:       # no explicit height, so
        self.h_min = 1          # use default (line is one pixel wide)

    fbgui.App.logger.msg("TRACE","min_size (%s): (%d,%d)" %
                                             (self._id,self.w_min,self.h_min))
    self._is_size_valid = True

  # --- redraw widget   ------------------------------------------------------

  def draw(self):
    """ draw the widget """

    if self.orientation == fbgui.HORIZONTAL:
      pygame.gfxdraw.hline(fbgui.App.display.screen,
                           self.screen.x,self.screen.x+self.screen.w,
                           self.screen.y,self.theme.fg_color)
    else:
      pygame.gfxdraw.vline(fbgui.App.display.screen,
                           self.screen.x,self.screen.y,
                           self.screen.y+self.screen.h,self.theme.fg_color)
