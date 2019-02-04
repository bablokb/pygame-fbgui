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

  # --- eq-operator   --------------------------------------------------------
  
  def __eq__(self, other):
    return self._id == other._id

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=None,toplevel=False,parent=None):
    """ constructor """

    self._id        = id
    self._parent    = parent
    self._toplevel  = toplevel

    # coordinates and size of widget (actually used during drawing)
    self.screen     = fbgui.Settings({'x': 0, 'y':0, 'w': 0, 'h': 0})

    # requested / default coordinates of widget
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

    # minimum sizes
    self._is_size_valid = False

    self.align   = getattr(settings,'align',(fbgui.LEFT,fbgui.BOTTOM))
    if not type(self.align) is tuple:
      self.align = (self.align,self.align)

    self.flex    = getattr(settings,'flex',0)

    if self._parent:
      self.theme = fbgui.Settings(self._parent.theme)
    else:
      self.theme = fbgui.Settings(fbgui.App.theme)
    self.theme.copy(settings)

    if self._parent:
      self._parent.add(self)

  # --- set parent   ---------------------------------------------------------

  def _set_parent(self,parent):
    """ set parent of this widget """

    self._parent = parent

  # --- layout widget and children   -----------------------------------------

  def pack(self):
    """ layout widget and children (for toplevel widgets) """

    assert self._toplevel, "pack() is only valid for toplevel widgets!"
    self._invalidate()
    self._layout(self.x,self.y,self.w,self.h)

  # --- invalidate size information   ----------------------------------------

  def _invalidate(self):
    """ (recursively) invalidate size-information """

    self._is_size_valid = False

  # --- layout widget   ------------------------------------------------------

  def _layout(self,x,y,w,h):
    """ layout widget:
          x,y: target-position as defined by the parent
          w,h: width and height of parent (adapted by e.g. margins)
    """

    # just call the standard-layout mechanism here
    self._std_layout(x,y,w,h)

  # --- standard layout widget   ---------------------------------------------

  def _std_layout(self,x,y,w,h):
    """ layout widget:
          x,y: target-position as defined by the parent
          w,h: width and height of parent (adapted by e.g. margins)
    """

    fbgui.App.logger.msg("DEBUG","std-layout-in  (%s): (%d,%d,%d,%d)" %
                         (self._id,x,y,w,h))

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
      self.screen.w = int(self.w * w)
    else:
      # default is minimum size
      w_min, h_min = self._minimum_size(w,h)
      self.screen.w = w_min

    if self.h > 1 or self.h == 1 and type(self.h) is int:
      # absolute size
      self.screen.h = self.h
    elif 0 < self.h and self.h <= 1.0:
      # relative size
      self.screen.h = int(self.h * h)
    else:
      # default is minimum size
      if h_min == -1:
        w_min, h_min = self._minimum_size(w,h)
      self.screen.h = h_min

    fbgui.App.logger.msg("DEBUG","std-layout-out (%s): (%d,%d,%d,%d)" %
           (self._id,self.screen.x,self.screen.y,self.screen.w,self.screen.h))

  # --- query minimum size   -------------------------------------------------

  def _minimum_size(self,w,h):
    """ query minimum size of widget """

    # note that this also works for toplevel-widgets, since
    # these widgets always have absolute size

    if self.w_min  > 0 and self.h_min > 0:
      return (self.w_min,self.h_min)

    if self.w > 1 or self.w == 1 and type(self.w) is int:
      # absolute size
      self.w_min = self.w
    elif 0 < self.w and self.w <= 1.0:
      # relative size
      self.w_min = int(self.w * w)
    else:
      # default is no size (subclasses will change this)
      self.w_min = 0

    if self.h > 1 or self.h == 1 and type(self.h) is int:
      # absolute size
      self.h_min = self.h
    elif 0 < self.h and self.h <= 1.0:
      # relative size
      self.h_min = int(self.h * h)
    else:
      # default is no size (subclasses will change this)
      self.h_min = 0

    fbgui.App.logger.msg("DEBUG",
           "min_size default (%s): (%d,%d)" % (self._id,self.w_min,self.h_min))
    return (self.w_min,self.h_min)

  # --- redraw widget   ------------------------------------------------------

  def draw(self):
    """ draw the widget """

    # subclasses must implement their own logic here
    pass
