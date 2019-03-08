#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Class Text: a VBox with multiple lines of text
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import fbgui

class Text(fbgui.VBox):
  """ Text box """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,text=None,
               settings=fbgui.Settings(),toplevel=False,parent=None):
    """ constructor """

    settings.padding = getattr(settings,'padding',3)
    super(Text,self).__init__(id,settings=settings,
                              toplevel=toplevel,parent=parent)

    self._rows   = getattr(settings,'rows',0)
    self._text   = None   # text (complete)
    self._lines  = []     # text (split at \n)

    self.set_text(text,refresh=False)

  # --- set the text of this Text   ----------------------------------------

  def set_text(self,text,refresh=True):
    """ set the text of the button """

    if text == self._text:
      return
    fbgui.App.logger.msg("TRACE","changing text of %s" % self._id)

    self._text = text
    if not text:
      self.clear(refresh=refresh)
      return
    
    # cleanup of old state
    if self._lines:
      del self._lines[:]
      self.remove_all()

    # split text and create labels
    self._lines = text.split('\n')
    n_labels = self._rows if self._rows > 0 else len(self._lines)

    settings = fbgui.Settings(self._settings)
    settings.width  = 0
    settings.height = 0
    settings.align  = fbgui.LEFT
    for n in range(n_labels):
      label = fbgui.Label("%s_line_%d" % (self._id,n),"",
                                  settings=settings,parent=self)
      label.set_text(self._lines[n])

    if refresh:
      self.post_layout()

  # --- clear the text of this Text   --------------------------------------

  def clear(self,refresh=True):
    """ clear the text of the button """

    if self._lines:
      del self._lines[:]
      self.remove_all()
    self._text = None

    if refresh:
      self.post_layout()
