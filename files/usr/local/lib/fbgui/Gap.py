#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# The base class for all Gaps. This just represents empty space.
#
# Additional settings:
#
#  - orientation: horizontal|vertical
#  - size: size of gap
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import fbgui

class Gap(fbgui.Panel):
  """ base class for all Gaps """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=fbgui.Settings(),toplevel=False,parent=None):
    """ constructor """

    super(Gap,self).__init__(id,settings=settings,
                             toplevel=toplevel,parent=parent)
    self.orientation = getattr(settings,'orientation',None)
    assert self.orientation, "ERROR: orientation not specified"

    size = getattr(settings,'size',0)
    if self.orientation == fbgui.HORIZONTAL:
      self.w = size
    else:
      self.h = size

  # --- redraw widget   ------------------------------------------------------

  def draw(self,surface=None):
    """ draw the widget """

    # do nothing!
    pass
