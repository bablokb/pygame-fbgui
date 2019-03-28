#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Class VBox: a panel with a vertical layout of it's children
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import fbgui

class VBox(fbgui.Box):
  """ Horizontal box """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=fbgui.Settings(),toplevel=False,parent=None):
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
    if not self._h_from_parent or self.weight[1] > 0:
      # dynamic size
      self.h_min = (self._child_h_sum + (n_childs-1)*self.padding[1] +
                                         self.margins[2]+self.margins[3])
    if not self._w_from_parent:
      # dynamic size
      self.w_min = self._child_w_max + self.margins[0]+self.margins[1]

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
    w = w - self.margins[0] - self.margins[1]
    h = h - self.margins[2] - self.margins[3]
    fbgui.App.logger.msg("TRACE","x,y,w,h (%s childs): (%d,%d,%d,%d)" %
                         (self._id,x,y,w,h))

    # calculate additional size we have
    n_childs = len(self._childs)
    h_add = max(0,h-self._child_h_sum - (n_childs-1)*self.padding[1])
    fbgui.App.logger.msg("TRACE","h_add (%s): %d" % (self._id,h_add))

    if self.uniform[1]:
      weight_sum = n_childs
    else:
      weight_sum = self._child_h_weight_sum
    if not weight_sum:
      weight_sum = 1     # prevent devision by zero

    # now layout children
    index = 0
    for child in self._childs:
      child_w, child_h = self._child_sizes[index]
      if self.uniform[0]:
        child_w = self._child_w_max
      if self.uniform[1]:
        child_h = self._child_h_max

      weight = child.weight[1]
      child_add = int(h_add*weight/weight_sum)
      x_c      = x

      # horizontal alignment
      if child.align[0] == fbgui.LEFT:
        x_c = x
      elif child.align[0] == fbgui.RIGHT:
        x_c = x + w - child_w
      else:
        x_c = x + int((w - child_w)/2)

      child._layout(x_c,y,child_w,child_h+child_add)
      y += child_h+child_add + self.padding[1]
      index += 1
