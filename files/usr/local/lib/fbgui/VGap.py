#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# A class for vertical gaps.
#
# Additional settings:
#
#  - size: size of gap
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import fbgui

class VGap(fbgui.Gap):
  """ base class for all Gaps """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=None,toplevel=False,parent=None):
    """ constructor """

    settings.orientation = fbgui.HORIZONTAL
    super(VGap,self).__init__(id,settings=settings,
                             toplevel=toplevel,parent=parent)
