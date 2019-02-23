#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Class VBox: a panel with a vertical layout of it's children
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import fbgui

class VBox(fbgui.Box):
  """ Horizontal box """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=None,toplevel=False,parent=None):
    """ constructor """

    super(VBox,self).__init__(id,settings=settings,
                              toplevel=toplevel,parent=parent)

  # --- query minimum size   -------------------------------------------------

  def _calc_minimum_size(self,w,h):
    """ query minimum size of widget """

    if self._is_size_valid:
      return

    # minimum size is either absolute, relative to parent or
    #  - w_max of childs + margins
    #  - h_sum + (n-1)*padding + margins

    # size without children (panel size incl. margins)
    # N.B.: Box._calc_minimum_size() will also calculate child-sizes
    super(VBox,self)._calc_minimum_size(w,h)

    n_childs = len(self._childs)
    if not n_childs:
      fbgui.App.logger.msg("TRACE",
                  "min_size (%s): (%d,%d)" % (self._id,self.w_min,self.h_min))
      return (self.w_min,self.h_min)
      
    # now take maximum of size without children and total width/height of children
    self.h_min = max(self.h_min,self._child_h_sum +
                              (n_childs-1)*self.padding[0] +
                                         self.margins[2]+self.margins[3])
    self.w_min = max(self.w_min,
                     self._child_w_max + self.margins[0]+self.margins[1])

    fbgui.App.logger.msg("TRACE",
              "min_size (%s): (%d,%d)" % (self._id,self.w_min,self.h_min))

    self._is_size_valid = True

  # --- layout widget   ------------------------------------------------------

  def _layout(self,x,y,w,h):
    """ layout widget """

    self._std_layout(x,y,w,h)

    # correct values for margins
    x = x + self.margins[0]
    y = y + self.margins[2]
    w = self.w_min - self.margins[0] - self.margins[1]
    h = self.h_min - self.margins[2] - self.margins[3]
    fbgui.App.logger.msg("TRACE","x,y,w,h (%s childs): (%d,%d,%d,%d)" %
                         (self._id,x,y,w,h))
    
    # now layout children
    index = 0
    for child in self._childs:
      w_c, h_c = self._child_sizes[index]
      y_c      = y

      # horizontal alignment
      if child.align[0] == fbgui.LEFT:
        x_c = x
      elif child.align[0] == fbgui.RIGHT:
        x_c = x + w - w_c
      else:
        x_c = x + int((w - w_c)/2)

      child._layout(x_c,y_c,w_c,h_c)
      y     += h_c + self.padding[1]
      index += 1
