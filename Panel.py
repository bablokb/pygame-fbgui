#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# The base class for all Panels: panels are widget-collections and don't
#                                draw anything themselves (except background)
#
# Additional settings:
#
#  - margins: single value or (left,right,top,bottom)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import fbgui.Widget

class Panel(fbgui.Widget):
  """ base class for all Panels """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=None,toplevel=False):
    """ constructor """

    super(Panel,self).__init__(id,settings=settings,toplevel=toplevel)

    self.margins = getattr(settings,'margins',(0,0,0,0))
    if not type(self.margins) is tuple:
      self.margins = (self.margins,self.margins,self.margins,self.margins)

    self._childs    = []

  # --- add child   ----------------------------------------------------------

  def add(self,widget):
    """ add a child widget """

    self._childs.append(widget)
    widget._set_parent(self)

  # --- remove child   -------------------------------------------------------

  def remove(self,widget):
    """ remove a child widget """

    self._childs.remove(widget)

  # --- query minimum size   -------------------------------------------------

  def _minimum_size(self,w,h):
    """ query minimum size of widget """

    if self.w_min  > 0 and self.h_min > 0:
      return (self.w_min,self.h_min)

    (w_min,h_min) = super(Panel,self)._minimum_size(w,h)
    self.w_min = max(w_min,self.margins[0]+self.margins[1])
    self.h_min = max(h_min,self.margins[2]+self.margins[3])
    fbgui.App.logger.msg("DEBUG",
                 "min_size (%s): (%d,%d)" % (self._id,self.w_min,self.h_min))
    return (self.w_min,self.h_min)

  # --- layout widget   ------------------------------------------------------

  def _layout(self,x,y,w,h):
    """ layout widget """

    self._std_layout(x,y,w,h)

    # correct values for margins
    x = x + self.margins[0]
    y = y + self.margins[2]
    w = w - self.margins[0] - self.margins[1]
    h = h - self.margins[2] - self.margins[3]
    fbgui.App.logger.msg("DEBUG","x,y,w,h (%s childs): (%d,%d,%d,%d)" %
                         (self._id,x,y,w,h))
    
    # now layout children
    for child in self._childs:
      w_min, h_min = child._minimum_size(w,h)

      # horizontal alignment
      fbgui.App.logger.msg("DEBUG","halign (%s): %d" % (child._id,child.align[0]))
      if child.align[0] == fbgui.LEFT:
        x_c = x
      elif child.align[0] == fbgui.RIGHT:
        x_c = x + w - w_min
      else:
        x_c = x + int((w - w_min)/2)

      # vertical alignment
      fbgui.App.logger.msg("DEBUG","valign (%s): %d" % (child._id,child.align[1]))
      if child.align[1] == fbgui.TOP:
        y_c = y
      elif child.align[1] == fbgui.BOTTOM:
        y_c = y + h - h_min
      else:
        y_c = y + int((h - h_min)/2)

      child._layout(x_c,y_c,w,h)

  # --- redraw widget   ------------------------------------------------------

  def draw(self):
    """ draw the widget """

    if not self._parent or self.theme.bg_color != self._parent.theme.bg_color:
      fbgui.App.display.screen.fill(self.theme.bg_color,
                rect=(self.screen.x,self.screen.y,self.screen.w,self.screen.h))

    for child in self._childs:
      child.draw()
