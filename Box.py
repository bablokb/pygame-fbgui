#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# The base class for all Boxes. Don't instantiate directly.
#
# Additional settings:
#
#  - padding: single value or (horizontal,vertical)    (used by subclasses)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import fbgui

class Box(fbgui.Panel):
  """ base class for all Boxes """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=None,toplevel=False):
    """ constructor """

    super(Box,self).__init__(id,settings=settings,toplevel=toplevel)

    self.padding = getattr(settings,'padding',(0,0))
    if not type(self.padding) is tuple:
      self.padding = (self.padding,self.padding)

    self._child_w_max = 0
    self._child_h_max = 0
    self._child_w_sum = 0
    self._child_h_sum = 0
    self._child_sizes = []

  # --- query maximum size of children   -------------------------------------

  def _get_sizes(self,w,h):
    """ query sizes of children """

    self._child_w_max = 0
    self._child_h_max = 0
    self._child_w_sum = 0
    self._child_h_sum = 0
    self._child_sizes = []

    for child in self._childs:
      (c_w,c_h) = child._minimum_size(w,h)
      self._child_w_max  = max(c_w,self._child_w_max)
      self._child_h_max  = max(c_h,self._child_h_max)
      self._child_w_sum += c_w
      self._child_h_sum += c_h
      self._child_sizes.append((c_w,c_h))

    fbgui.App.logger.msg("DEBUG",
        "child-sizes of (%s): (w_max,h_max)=(%d,%d)" %
                         (self._id,self._child_w_max, self._child_h_max))
    fbgui.App.logger.msg("DEBUG",
        "child-sizes of (%s): (w_sum,h_sum)=(%d,%d)" %
                         (self._id,self._child_w_sum, self._child_h_sum))
