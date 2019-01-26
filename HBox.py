#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Class HBox: a panel with a horizontal layout of it's children
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import fbgui

class HBox(fbgui.Box):
  """ Horizontal box """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=None,toplevel=False):
    """ constructor """

    super(HBox,self).__init__(id,settings=settings,toplevel=toplevel)

  # --- query minimum size   -------------------------------------------------

  def _minimum_size(self,w,h):
    """ query minimum size of widget """

    # minimum size is either absolute, relative to parent or
    #  - w_sum + (n-1)*padding + margins
    #  - h_max of childs + margins

    # size without children (panel size incl. margins)
    (w_min,h_min) = super(HBox,self)._minimum_size(w,h)

    n_childs = len(self._childs)
    if not n_childs:
      fbgui.App.logger.msg("DEBUG",
                           "min_size (%s): (%d,%d)" % (self._id,w_min,h_min))
      return (w_min,h_min)
      
    # child-dimensions
    self._get_sizes(w,h)
    w_min = max(w_min,self._child_w_sum +
                                      (n_childs-1)*self.padding[0] +
                                              self.margins[0]+self.margins[1])
    h_min = max(h_min,self._child_h_max + self.margins[2]+self.margins[3])

    fbgui.App.logger.msg("DEBUG",
                             "min_size (%s): (%d,%d)" % (self._id,w_min,h_min))
    return (w_min,h_min)

  # --- layout widget   ------------------------------------------------------

  def _layout(self,x,y,w,h):
    """ layout widget """

    if self._is_layout:
      return                                # layout already done

    # do default behaviour (sets self._is_layout to True)
    self._std_layout(x,y,w,h)

    # correct values for margins
    x = x + self.margins[0]
    y = y + self.margins[2]
    w = w - self.margins[0] - self.margins[1]
    h = h - self.margins[2] - self.margins[3]
    fbgui.App.logger.msg("DEBUG","x,y,w,h (%s childs): (%d,%d,%d,%d)" %
                         (self._id,x,y,w,h))
    
    # now layout children
    index = 0
    for child in self._childs:
      w_c, h_c = self._child_sizes[index]
      x_c      = x

      # vertical alignment
      if child.align[1] == fbgui.Widget.TOP:
        y_c = y
      elif child.align[1] == fbgui.Widget.BOTTOM:
        y_c = y + self._child_h_max - h_c
      else:
        y_c = y + int((self._child_h_max - h_c)/2)

      child._layout(x_c,y_c,w_c,h_c)
      x     += w_c + self.padding[0]
      index += 1

  # --- redraw widget   ------------------------------------------------------

  def draw(self):
    """ draw the widget """

    if not self._parent or self.theme.bg_color != self._parent.theme.bg_color:
      fbgui.App.display.screen.fill(self.theme.bg_color,
                rect=(self.screen.x,self.screen.y,self.screen.w,self.screen.h))

    for child in self._childs:
      child.draw()
