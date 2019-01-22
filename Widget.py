#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# The base class for all Widgets.
#
# Settings:
#  - theme-settings
#  - toplevel (default: False)
#  - x,y:
#      -1: layout determines screen-position
#     >=0: absolute position
#  - width, height:
#                 0: layout determines size, but at least minimum size 
#    0 < w,h <= 1.0: size relative to parent (float!)
#          1 <= w,h: absolute size (int!)
#  - align  : single value or (horizontal,vertical)
#             values: TOP/BOTTOM/LEFT/RIGHT
#  - margins: single value or (left,right,top,bottom)
#  - flex: weight for additional space:
#       0: widget uses it's minimal size
#      >0: relative weight
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import fbgui

class Widget(object):
  """ base class for all Widgets """

  HORIZONTAL =   1
  VERTICAL   =   2
  TOP        =   3
  BOTTOM     =   4
  LEFT       =   5
  RIGHT      =   6
  CENTER     =   7
  
  # --- eq-operator   --------------------------------------------------------
  
  def __eq__(self, other):
    return self._id == other._id

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,parent=None,settings=None,toplevel=False):
    """ constructor """

    self._id       = id
    self._parent   = parent
    self._toplevel = toplevel
    self._dirty    = True                     # initial state is always dirty

    if toplevel:
      self.x       = 0
      self.y       = 0
      self.w       = fbgui.App.display.width
      self.h       = fbgui.App.display.height
    else:
      self.x       = getattr(settings,'x',-1)
      self.y       = getattr(settings,'y',-1)
      self.w       = getattr(settings,'width',0)
      self.h       = getattr(settings,'height',0)

    self.align   = getattr(settings,'align',(Widget.LEFT,Widget.BOTTOM))
    if not type(self.align) is tuple:
      self.align = (self.align,self.align)

    self.flex    = getattr(settings,'flex',0)

    self.theme   = fbgui.Settings(fbgui.App.theme)
    self.theme.copy(settings)

  # --- force redraw   -------------------------------------------------------
  
  def invalidate(self,redraw=False):
    """ force redraw """

    self._dirty = True
    if redraw:
      # post pygame redraw event
      pass

  # --- layout widget and children   -----------------------------------------

  def pack(self):
    """ layout widget and children (for toplevel widgets) """

    assert self._toplevel, "pack() is only valid for toplevel widgets!"
    self._layout(self.x,self.y,self.w,self.h)

  # --- layout widget   ------------------------------------------------------

  def _layout(self,x,y,w,h):
    """ layout widget:
          x,y: target-position as defined by the parent
          w,h: width and height of parent (adapted by e.g. margins)
    """

    fbgui.App.logger.msg("DEBUG","layout-in (%s): (%d,%d,%d,%d)" %
                         (self._id,x,y,w,h))

    if self._is_layout:
      return                                # layout already done

    self.screen = fbgui.Settings({'x': 0, 'y':0, 'w': 0, 'h': 0})

    # implement default behaviour
    #  - x,y absolute -> save widget x,y
    #        else     -> use argument x,y
    self.screen.x = self.x if self.x >= 0 else x
    self.screen.y = self.y if self.y >= 0 else y

    #  - w,h absolute -> save widget w,h
    #        relative -> calc from parent w,h
    #        0        -> use my minimum size
    w_min, h_min = (-1,-1)
    if self.w > 1 or self.w == 1 and type(self.w) is int:
      # absolute size
      self.screen.w = self.w
    elif 0 < self.w and self.w <= 1.0:
      # relative size
      self.screen.w = self.w * w
    else:
      # default is minimum size
      w_min, h_min = self._minimum_size()
      self.screen.w = w_min

    if self.h > 1 or self.h == 1 and type(self.h) is int:
      # absolute size
      self.screen.h = self.h
    elif 0 < self.h and self.h <= 1.0:
      # relative size
      self.screen.h = self.h * self._parent.screen.h
    else:
      # default is minimum size
      if h_min == -1:
        w_min, h_min = self._minimum_size()
      self.screen.h = h_min

    fbgui.App.logger.msg("DEBUG","layout (%s): (%d,%d,%d,%d)" %
           (self._id,self.screen.x,self.screen.y,self.screen.w,self.screen.h))
    self._is_layout = True

  # --- query minimum size   -------------------------------------------------

  def _minimum_size(self):
    """ query minimum size of widget """

    # note that this also works for toplevel-widgets, since
    # these widgets always have absolute size

    if self.w > 1 or self.w == 1 and type(self.w) is int:
      # absolute size
      w_min = self.w
    elif 0 < self.w and self.w <= 1.0:
      # relative size
      w_min = self.w * self._parent.w
    else:
      # default is no size (subclasses will change this)
      w_min = 0

    if self.h > 1 or self.h == 1 and type(self.h) is int:
      # absolute size
      h_min = self.h
    elif 0 < self.h and self.h <= 1.0:
      # relative size
      h_min = self.h * self._parent.screen.h
    else:
      # default is no size (subclasses will change this)
      h_min = 0

    fbgui.App.logger.msg("DEBUG","min_size (%s): (%d,%d)" % self._id,w_min,h_min)
    return (w_min,h_min)

  # --- redraw widget   ------------------------------------------------------

  def draw(self):
    """ draw the widget """

    if not self._dirty:
      return

    # subclasses must implement their own logic here

    self._dirty = False
