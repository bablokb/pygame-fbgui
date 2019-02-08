#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Package fbgui with basic GUI-elements for a simple framebuffer application.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import pygame

# --- constants   ------------------------------------------------------------

# layout
HORIZONTAL =   1
VERTICAL   =   2
TOP        =   3
BOTTOM     =   4
LEFT       =   5
RIGHT      =   6
CENTER     =   7

# internal event
EVENT             = pygame.NUMEVENTS
EVENT_CODE_LAYOUT = 0
EVENT_CODE_REDRAW = 1

from . Msg      import Msg      as Msg
from . Settings import Settings as Settings
from . Color    import Color    as Color

from . App      import App      as App
from . Widget   import Widget   as Widget
from . Panel    import Panel    as Panel
from . Box      import Box      as Box
from . HBox     import HBox     as HBox
from . VBox     import VBox     as VBox
from . Gap      import Gap      as Gap
from . HGap     import HGap     as HGap
from . VGap     import VGap     as VGap

from . Line     import Line     as Line
from . Label    import Label    as Label
