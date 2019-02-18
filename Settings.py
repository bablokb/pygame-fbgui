#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# A simple value-holder class for settings.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

class Settings(object):
  """ Value-holder class for arbitrary settings """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,defaults=None):
    """ constructor:
        - pass a list of 'supported' keys in a dict with default values
        - or pass a Settings-object (copy-constructor)
    """
    if defaults:
      if isinstance(defaults,Settings):
        self._keys = defaults._keys
        self.copy(defaults)
      else:
        self._keys = defaults.keys()
        for key in self._keys:
          setattr(self,key,defaults[key])
    else:
      self._keys = None

  # --- copy keys from other settings-object   -------------------------------
  
  def copy(self,other):
    """ copy keys from other settings """

    # extract keys
    if self._keys:
      keys = self._keys
    else:
      keys = [d for d in other.__dict__
                             if not callable(d) and not d.startswith("_")]
    
    # copy relevant keys
    for key in keys:
      if hasattr(other,key):
        setattr(self,key,getattr(other,key))
