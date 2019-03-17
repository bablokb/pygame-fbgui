#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# The base class for all Boxes. Don't instantiate directly.
#
# Additional settings:
#
#  - padding: single value or (horizontal,vertical)    (used by subclasses)
#  - uniform: all childs have equal size (False,True)  (used by subclasses)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import fbgui

class Box(fbgui.Panel):
  """ base class for all Boxes """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=fbgui.Settings(),toplevel=False,parent=None):
    """ constructor """

    super(Box,self).__init__(id,settings=settings,
                             toplevel=toplevel,parent=parent)

    self.padding = getattr(settings,'padding',(0,0))
    if not type(self.padding) is tuple:
      self.padding = (self.padding,self.padding)

    self.uniform = getattr(settings,'uniform',(False,False))
    if not type(self.uniform) is tuple:
      self.uniform = (self.uniform,self.uniform)

    self._child_w_max = 0
    self._child_h_max = 0
    self._child_w_sum = 0
    self._child_h_sum = 0
    self._child_sizes = []

  # --- query minimum size   -------------------------------------------------

  def _calc_minimum_size(self,w,h):
    """ query minimum size of widget
        Note: this is incomplete, rest of logic is within VBox and HBox
    """

    if self._is_size_valid:
      return

    self._child_w_max = 0
    self._child_h_max = 0
    self._child_w_sum = 0
    self._child_h_sum = 0
    self._child_sizes = []

    # calculate size of panel
    self._w_from_parent,self._h_from_parent = self._set_size_from_parent(w,h)
    self.w_min = max(self.w_min,self.margins[0]+self.margins[1])
    self.h_min = max(self.h_min,self.margins[2]+self.margins[3])
    fbgui.App.logger.msg("TRACE",
                 "min_size (%s): (%d,%d)" % (self._id,self.w_min,self.h_min))

    # calculate size of all children
    self._child_w_weight_sum = 0.0
    self._child_h_weight_sum = 0.0
    for child in self._childs:
      child._calc_minimum_size(self.w_min-self.margins[0]-self.margins[1],
                               self.h_min-self.margins[2]-self.margins[3])
      (c_w,c_h) = child.w_min, child.h_min
      self._child_w_max  = max(c_w,self._child_w_max)
      self._child_h_max  = max(c_h,self._child_h_max)
      self._child_w_sum += c_w
      self._child_h_sum += c_h
      self._child_w_weight_sum      += child.weight[0]
      self._child_h_weight_sum      += child.weight[1]
      self._child_sizes.append((c_w,c_h))

    # when all childs have equal size, use largest size to calculate sum
    n_childs = len(self._childs)
    if self.uniform[0]:
      self._child_w_sum = n_childs*self._child_w_max
    if self.uniform[1]:
      self._child_h_sum = n_childs*self._child_h_max

    fbgui.App.logger.msg("TRACE",
        "child-sizes of (%s): (w_max,h_max)=(%d,%d)" %
                         (self._id,self._child_w_max, self._child_h_max))
    fbgui.App.logger.msg("TRACE",
        "child-sizes of (%s): (w_sum,h_sum)=(%d,%d)" %
                         (self._id,self._child_w_sum, self._child_h_sum))

    self._is_size_valid = True
