#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# A line widget.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import pygame.gfxdraw

import fbgui

class Line(fbgui.Widget):
  """ draw a line """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=None,parent=None,toplevel=False):
    """ constructor """

    super(Panel,self).__init__(id,settings=settings,
                               parent=parent,toplevel=toplevel)
    self.orientation = getattr(settings,'orientation',fbgui.Widget.HORIZONTAL)

  # --- query minimum size   -------------------------------------------------

  def _minimum_size(self):
    """ query minimum size of widget """

    (w_min,h_min) = super(Line,self)._minimum_size()
    if self._settings.orientation == fbgui.Widget.HORIZONTAL:
      h_min = 1            # horizontal lines have height==1
      if w_min == 0:       # no explicit width, so
        w_min = 1          # use default (line is one pixel wide)
    else:
      w_min = 1            # vertical lines have width==1
      if h_min == 0:       # no explicit height, so
        h_min = 1          # use default (line is one pixel wide)

    fbgui.App.logger.msg("DEBUG","min_size (%s): (%d,%d)" % self._id,w_min,h_min)
    return (w_min,h_min)

  # --- redraw widget   ------------------------------------------------------

  def draw(self):
    """ draw the widget """

    if not self._dirty:
      return

    if self._settings.orientation == fbgui.Widget.HORIZONTAL:
      pygame.gfxdraw.hline(fbgui.App.display.screen,
                           self.screen.x,x+self.screen.w,
                           self.screen.y,self.theme.fg_color)
    else:
      pygame.gfxdraw.vline(fbgui.App.display.screen,
                           self.screen.x,self.screen.y,
                           self.screen.y+self.screen.h,self.theme.fg_color)
    self._dirty = False
