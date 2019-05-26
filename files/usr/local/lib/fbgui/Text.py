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

import pygame

import fbgui

class Text(fbgui.VBox):
  """ Text box """

  EVENT_SET_TEXT = 0
  EVENT_CLEAR    = 1

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,text=None,
               settings=fbgui.Settings(),toplevel=False,parent=None):
    """ constructor """

    settings.padding = getattr(settings,'padding',3)
    settings.uniform = True
    super(Text,self).__init__(id,settings=settings,
                              toplevel=toplevel,parent=parent)

    self._rows   = getattr(settings,'rows',0)
    self._text   = None   # text (complete)
    self._lines  = []     # text (split at \n)

    self._set_text(text,refresh=False)

  # --- set the text of this Text (internal)   -----------------------------

  def _set_text(self,text,refresh=True):
    """ set the text of the widget (internal method) """

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
    settings.weight = 0
    settings.align  = fbgui.LEFT
    for n in range(n_labels):
      label = fbgui.Label("%s_line_%d" % (self._id,n),"",
                                  settings=settings,parent=self)
      label.set_text(self._lines[n],refresh=False)

    if refresh:
      self.post_layout()

  # --- set the text of this Text   ----------------------------------------

  def set_text(self,text,refresh=True):
    """ set the text of this widget (public method) """

    # N.B.: we just post a suitable event, since _set_text should only be
    #       called from the main-thread

    fbgui.App.logger.msg("TRACE","posting set_text-event from %s" % self._id)
    event = pygame.fastevent.Event(fbgui.EVENT,
                                   code=fbgui.EVENT_CODE_WIDGET,
                                   widget=self)

    event.method = Text.EVENT_SET_TEXT
    event.text = text
    event.refresh = refresh
    pygame.fastevent.post(event)

  # --- clear the text of this Text (internal)   ---------------------------
  def _clear(self,refresh=True):
    """ clear the text of the button """

    if self._lines:
      del self._lines[:]
      self.remove_all()
    self._text = None

    if refresh:
      self.post_layout()

  # --- clear the text of this Text   --------------------------------------

  def clear(self,refresh=True):
    """ clear the text of the button """

    # N.B.: we just post a suitable event, since _clear should only be
    #       called from the main-thread

    fbgui.App.logger.msg("TRACE","posting clear-event from %s" % self._id)
    event = pygame.fastevent.Event(fbgui.EVENT,
                                   code=fbgui.EVENT_CODE_WIDGET,
                                   widget=self)

    event.method = Text.EVENT_CLEAR
    event.refresh = refresh
    pygame.fastevent.post(event)

  # --- handle internal event   ----------------------------------------------

  def _handle_internal_event(self,event):
    """ handle internal events """

    if event.method == Text.EVENT_SET_TEXT:
      self._set_text(event.text,refresh=event.refresh)
    elif event.method == Text.EVENT_CLEAR:
      self._clear(refresh=event.refresh)
    else:
      assert False, "ERROR: illegal event-method: %d" % event.method
