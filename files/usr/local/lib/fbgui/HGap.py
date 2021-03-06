#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# A class for horizontal gaps.
#
# Additional settings:
#
#  - size: size of gap
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import fbgui

class HGap(fbgui.Gap):
  """ base class for all Gaps """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=fbgui.Settings(),toplevel=False,parent=None):
    """ constructor """

    settings.orientation = fbgui.HORIZONTAL
    super(HGap,self).__init__(id,settings=settings,
                             toplevel=toplevel,parent=parent)
