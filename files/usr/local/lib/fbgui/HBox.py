#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Class HBox: a panel with a horizontal layout of it's children
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import fbgui

class HBox(fbgui.Box):
  """ Horizontal box """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=fbgui.Settings(),toplevel=False,parent=None):
    """ constructor """

    super(HBox,self).__init__(id,settings=settings,
                              toplevel=toplevel,parent=parent)

  # --- query minimum size   -------------------------------------------------

  def _calc_minimum_size(self,w,h):
    """ query minimum size of widget """

    if self._is_size_valid:
      return

    # minimum size is either absolute, relative to parent or
    #  - w_sum + (n-1)*padding + margins
    #  - h_max of childs + margins

    # size without children (panel size incl. margins)
    # N.B.: Box._calc_minimum_size() will also calculate child-sizes
    super(HBox,self)._calc_minimum_size(w,h)

    n_childs = len(self._childs)
    if not n_childs:
      fbgui.App.logger.msg("TRACE",
                  "min_size (%s): (%d,%d)" % (self._id,self.w_min,self.h_min))
      return (self.w_min,self.h_min)
      
    # now take maximum of size without children and total width/height of children
    if not self._w_from_parent or self.weight[0] > 0:
      # dynamic size
      self.w_min = (self._child_w_sum + (n_childs-1)*self.padding[0] +
                                         self.margins[0]+self.margins[1])
    if not self._h_from_parent:
      # dynamic size
      self.h_min = self._child_h_max + self.margins[2]+self.margins[3]

    fbgui.App.logger.msg("TRACE",
              "min_size after childs (%s): (%d,%d)" % (self._id,self.w_min,self.h_min))

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
    w_add = max(0,w-self._child_w_sum - (n_childs-1)*self.padding[0])
    fbgui.App.logger.msg("TRACE","w_add (%s): %d" % (self._id,w_add))

    if self.uniform[0]:
      weight_sum = n_childs
    else:
      weight_sum = self._child_w_weight_sum
    if not weight_sum:
      weight_sum = 1     # prevent devision by zero

    # now layout children
    index = 0
    for child in self._childs:
      child_w, child_h = self._child_sizes[index]
      if self.uniform[1]:
        child_h = self._child_h_max
      if self.uniform[0]:
        weight = 1.0
      else:
        weight = child.weight[0]

      child_add = int(w_add*weight/weight_sum)
      y_c       = y

      # vertical alignment
      if child.align[1] == fbgui.TOP:
        y_c = y
      elif child.align[1] == fbgui.BOTTOM:
        y_c = y + h - child_h
      else:
        y_c = y + int((h - child_h)/2)

      if self.uniform[0]:
        child._layout(x,y_c,self._child_w_max+child_add,child_h)
        x += self._child_w_max+child_add + self.padding[0]
      else:
        child._layout(x,y_c,child_w+child_add,child_h)
        x += child_w+child_add + self.padding[0]
      index += 1
