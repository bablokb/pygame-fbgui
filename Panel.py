#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# The base class for all Panels: panels are widget-collections and don't
#                                draw anything themselves (except background)
#
# Additional settings:
#
#  - margins: single value or (left,right,top,bottom)
#  - padding: single value or (horizontal,vertical)    (used by subclasses)
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
  
  def __init__(self,id,parent=None,settings=None,toplevel=False):
    """ constructor """

    super(Panel,self).__init__(id,settings=settings,
                               parent=parent,toplevel=toplevel)

    self.margins = getattr(settings,'margins',(0,0,0,0))
    if not type(self.margins) is tuple:
      self.margins = (self.margins,self.margins,self.margins,self.margins)

    self.padding = getattr(settings,'padding',(0,0))
    if not type(self.padding) is tuple:
      self.padding = (self.padding,self.padding)

    self._childs    = []

  # --- add child   ----------------------------------------------------------

  def add(self,widget):
    """ add a child widget """

    self._childs.append(widget)

  # --- remove child   -------------------------------------------------------

  def remove(self,widget):
    """ remove a child widget """

    self._childs.remove(widget)

  # --- query minimum size   -------------------------------------------------

  def _minimum_size(self,w,h):
    """ query minimum size of widget """

    (w_min,h_min) = super(Panel,self)._minimum_size(w,h)
    fbgui.App.logger.msg("DEBUG","min_size (%s): (%d,%d)" % (self._id,w_min,h_min))
    return (w_min,h_min)

  # --- layout widget   ------------------------------------------------------

  def _layout(self,x,y,w,h):
    """ layout widget """

    if self._is_layout:
      return                                # layout already done

    # do default behaviour (sets self._is_layout to True)
    super(Panel,self)._layout(x,y,w,h)

    # correct values for margins
    x = x + self.margins[0]
    y = y + self.margins[2]
    w = w - self.margins[0] - self.margins[1]
    h = h - self.margins[2] - self.margins[3]
    fbgui.App.logger.msg("DEBUG","x,y,w,h (%s): (%d,%d,%d,%d)" %
                         (self._id,x,y,w,h))
    
    # now layout children
    for child in self._childs:
      w_min, h_min = child._minimum_size(w,h)

      # horizontal alignment
      fbgui.App.logger.msg("DEBUG","halign (%s): %d" % (child._id,child.align[0]))
      if child.align[0] == fbgui.Widget.LEFT:
        x_c = x
      elif child.align[0] == fbgui.Widget.RIGHT:
        x_c = x + w - w_min
      else:
        x_c = x + w/2 - w_min/2

      # vertical alignment
      fbgui.App.logger.msg("DEBUG","valign (%s): %d" % (child._id,child.align[1]))
      if child.align[1] == fbgui.Widget.TOP:
        y_c = y
      elif child.align[1] == fbgui.Widget.BOTTOM:
        y_c = y + h - h_min
      else:
        y_c = y + h/2 - h_min/2

      child._layout(x_c,y_c,w,h)

  # --- redraw widget   ------------------------------------------------------

  def draw(self):
    """ draw the widget """

    if not self._parent or self.theme.bg_color != self._parent.theme.bg_color:
      fbgui.App.display.screen.fill(self.theme.bg_color,
                rect=(self.screen.x,self.screen.y,self.screen.w,self.screen.h))

    for child in self._childs:
      child.draw()
