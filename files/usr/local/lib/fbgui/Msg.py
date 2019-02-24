#!/usr/bin/python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# Definition of class Msg
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import datetime, sys

class Msg(object):
  """ simple class for messages """

  MSG_LEVELS={
    "TRACE":0,
    "DEBUG":1,
    "INFO":2,
    "WARN":3,
    "ERROR":4,
    "NONE": 5
    }

  level = "INFO"    # override during initialization

  # --- print a message   ---------------------------------------------------
  
  def msg(self,msg_level,text,nl=True):
    """print a message"""
    if Msg.MSG_LEVELS[msg_level] >= Msg.MSG_LEVELS[Msg.level]:
      if nl:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stderr.write("[" + msg_level + "] " + "[" + now + "] " + text + "\n")
      else:
        sys.stderr.write(text)
        sys.stderr.flush()
