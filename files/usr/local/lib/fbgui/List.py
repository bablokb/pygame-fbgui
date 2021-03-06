#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Class List: display a list of widgets
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import pygame

import fbgui

class List(fbgui.VBox):
  """ List box """

  EVENT_ADD_ITEMS = 0
  EVENT_CLEAR     = 1

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,items=None,
               settings=fbgui.Settings(),toplevel=False,parent=None):
    """ constructor """

    settings.padding = getattr(settings,'padding',3)
    settings.uniform = True
    super(List,self).__init__(id,settings=settings,
                              toplevel=toplevel,parent=parent)
    
    self.multiselect      = getattr(settings,'multiselect',False)
    self._selected_widget = None
    self._inherit_select  = False
    self._add_items(items,refresh=False)

  # --- set the items of this List (internal)   ----------------------------

  def _add_items(self,items,refresh=True):
    """ set the items of this widget """

    fbgui.App.logger.msg("TRACE","%s: _add_items()" % self._id)

    if not items:
      fbgui.App.logger.msg("TRACE","no items to add for %s" % self._id)
      return

    # add new content
    for item in items:
      # add our own on_click-handler to the item
      if hasattr(item,'on_click'):
        item._on_click_original = item.on_click
      item.on_click = lambda widget,event: self._on_child_clicked(widget,event)
      if item._parent is None or item._parent.id() != self._id:
        self.add(item)

    if refresh:
      self.post_layout()

  # --- add items to this List   -------------------------------------------

  def add_items(self,items,refresh=True):
    """ add items to the list """

    # N.B.: we just post a suitable event, since _add_items should only be
    #       called from the main-thread

    fbgui.App.logger.msg("TRACE","posting ADD_ITEMS-event from %s" % self._id)
    event = pygame.fastevent.Event(fbgui.EVENT,
                                   code=fbgui.EVENT_CODE_WIDGET,
                                   widget=self)

    event.method  = List.EVENT_ADD_ITEMS
    event.items   = items
    event.refresh = refresh
    pygame.fastevent.post(event)

  # --- clear the content of this List (internal)   ----------------------

  def _clear(self,refresh=True):
    """ clear the content of the List (internal method) """

    fbgui.App.logger.msg("TRACE","%s: _clear()" % self._id)
    if len(self._childs):
      self.remove_all()
    if refresh:
      self.post_layout()

  # --- clear the text of this List   --------------------------------------

  def clear(self,refresh=True):
    """ clear the content of the List (public method) """

    # N.B.: we just post a suitable event, since _clear should only be
    #       called from the main-thread

    fbgui.App.logger.msg("TRACE","posting clear-event from %s" % self._id)
    event = pygame.fastevent.Event(fbgui.EVENT,
                                   code=fbgui.EVENT_CODE_WIDGET,
                                   widget=self)

    event.method  = List.EVENT_CLEAR
    event.refresh = refresh
    pygame.fastevent.post(event)

  # --- handle internal event   ----------------------------------------------

  def _handle_internal_event(self,event):
    """ handle internal events """

    if event.method == List.EVENT_ADD_ITEMS:
      self._add_items(event.items,refresh=event.refresh)
    elif event.method == List.EVENT_CLEAR:
      self._clear(refresh=event.refresh)
    else:
      assert False, "ERROR: illegal event-method: %d" % event.method

  # --- return selected widgets   --------------------------------------------

  def get_selected(self):
    """ return selected widgets or None (multiselect will return list) """

    if self.multiselect:
      return [w for w in self._childs[self._offset:] if w.is_selected()]
    else:
      return self._selected_widget
    
  # --- intercept on_click of childs   ---------------------------------------

  def _on_child_clicked(self,widget,event):
    """ intercept on_click of childs """

    fbgui.App.logger.msg("TRACE","list-item %s of %s clicked!" %
                                                        (widget.id(),self._id))

    # update selection state
    widget.toggle_selected()
    if not self.multiselect:
      if self._selected_widget and self._selected_widget.id() != widget.id():
        self._selected_widget.set_selected(False)
      if widget.is_selected():
        self._selected_widget = widget
      else:
        self._selected_widget = None

    # check for registered on_selection_changed event
    sc_handler = getattr(self,'on_selection_changed',None)
    if sc_handler:
      sc_handler(self.get_selected())

    _on_click_original = getattr(widget,'_on_click_original',None)
    if _on_click_original:
      fbgui.App.logger.msg("TRACE","calling _on_click_original for %s of %s" %
                                                        (widget.id(),self._id))
      return _on_click_original(widget,event)
    else:
      return True
