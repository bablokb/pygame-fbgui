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
#  - weight: weight for additional space:
#       0: widget uses it's minimal size
#      >0: relative weight
#  - show_hover: change color of widget while mouse is over widget (def: False)
#  - show_down: change color of widget while mouse is down (def: False)
#
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import pygame

import fbgui

class Widget(object):
  """ base class for all Widgets """

  MOUSE_NORMAL = 0
  MOUSE_HOVER  = 1
  MOUSE_DOWN   = 2

  # --- eq-operator   --------------------------------------------------------
  
  def __eq__(self, other):
    return self._id == other._id

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=fbgui.Settings(),toplevel=False,parent=None):
    """ constructor """

    self._id        = id
    self._parent    = parent
    self._toplevel  = toplevel
    self._settings  = settings
    self._selected  = False

    # state of mouse
    self._state     = Widget.MOUSE_NORMAL
    self._draw_rect = pygame.Rect(0,0,0,0)

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

    # save settings
    self.align   = getattr(settings,'align',(fbgui.LEFT,fbgui.BOTTOM))
    if not type(self.align) is tuple:
      self.align = (self.align,self.align)

    self.weight  = getattr(settings,'weight',(0,0))
    if not type(self.weight) is tuple:
      self.weight = (self.weight,self.weight)

    # theming support
    self.show_hover = getattr(settings,'show_hover',False)
    self.show_down  = getattr(settings,'show_down',False)

    if self._parent:
      fbgui.App.logger.msg("TRACE","%s: copying theme from %s" %
                           (self._id,self._parent._id))
      self.theme = fbgui.Settings(self._parent.theme)
    else:
      fbgui.App.logger.msg("TRACE","%s: copying theme from App" % self._id)
      self.theme = fbgui.Settings(fbgui.App.theme)
    self.theme.copy(settings)

    # keep track of fg/bg-color
    self._set_colors()

    if self._parent:
      self._parent.add(self)

  # --- set parent   ---------------------------------------------------------

  def _set_parent(self,parent):
    """ set parent of this widget """

    self._parent = parent

  # --- invalidate size information   ----------------------------------------

  def _invalidate(self):
    """ (recursively) invalidate size-information """

    self._is_size_valid = False

  # --- calculate minimum size based on parent   -----------------------------

  def _set_size_from_parent(self,w,h):
    """ try to calculate the widget-size from parent """

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

    fbgui.App.logger.msg("TRACE",
       "min_size from parent (%s): (%d,%d)" % (self._id,self.w_min,self.h_min))

    # return True if size is defined
    return (self.w_min>0, self.h_min>0)

  # --- query minimum size   -------------------------------------------------

  def _calc_minimum_size(self,w,h):
    """ query minimum size of widget """

    if not self._is_size_valid:
      self._set_size_from_parent(w,h)
      self._is_size_valid = True

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

    assert self._is_size_valid, "ERROR: minimum size not available"

    fbgui.App.logger.msg("TRACE","std-layout-in  (%s): (%d,%d,%d,%d)" %
                         (self._id,x,y,w,h))

    self.screen = fbgui.Settings({'x': 0, 'y':0, 'w': 0, 'h': 0})

    # implement default behaviour
    #  - x,y absolute -> save widget x,y
    #        else     -> use argument x,y
    self.screen.x = self.x if self.x >= 0 else x
    self.screen.y = self.y if self.y >= 0 else y

    self.screen.w = w
    self.screen.h = h

    self._draw_rect=pygame.Rect(self.screen.x,self.screen.y,
                                self.screen.w,self.screen.h)

    fbgui.App.logger.msg("TRACE","std-layout-out (%s): (%d,%d,%d,%d)" %
           (self._id,self.screen.x,self.screen.y,self.screen.w,self.screen.h))

  # --- align the widget   ---------------------------------------------------

  def _align(self,rect):
    """ align the widget on it's drawing area """

    # horizontal alignment
    if self.align[0] == fbgui.LEFT:
      x_c = self.screen.x
    elif self.align[0] == fbgui.RIGHT:
      x_c = self.screen.x + self.screen.w - rect.w
    else:
      x_c = self.screen.x + int((self.screen.w - rect.w)/2)

    # vertical alignment
    if self.align[1] == fbgui.TOP:
      y_c = self.screen.y
    elif self.align[1] == fbgui.BOTTOM:
      y_c = self.screen.y + self.screen.h - rect.h
    else:
      y_c = self.screen.y + int((self.screen.h - rect.h)/2)

    return (x_c,y_c)

  # --- set colors depending on state   --------------------------------------

  def _set_colors(self):
    """ set bg/fg-color depending on state """

    if self._selected:
      self.bg_color = self.theme.bg_color_selected
      self.fg_color = self.theme.fg_color_selected
    else:
      self.fg_color = self.theme.fg_color
      if self._state == Widget.MOUSE_HOVER and self.show_hover:
        self.bg_color = self.theme.bg_color_hover
      elif self._state == Widget.MOUSE_DOWN and self.show_down:
        self.bg_color = self.theme.bg_color_down
      else:
        self.bg_color = self.theme.bg_color

  # --- return id of widget   ------------------------------------------------

  def id(self):
    """ get id of widget """
    return self._id

  # --- return selection status   --------------------------------------------

  def is_selected(self):
    """ return selection status """
    return self._selected

  # --- set selection status   -----------------------------------------------

  def set_selected(self,new_state):
    """ set selection status """
    old_state = self._selected
    self._selected = new_state
    self._set_colors()
    return old_state

  # --- toggle selection status   --------------------------------------------

  def toggle_selected(self):
    """ toggle selection status """
    return self.set_selected(not self._selected)

  # --- layout widget and children   -----------------------------------------

  def pack(self):
    """ layout widget and children (for toplevel widgets) """

    assert self._toplevel, "pack() is only valid for toplevel widgets!"
    self._invalidate()
    self._calc_minimum_size(self.w,self.h)
    self._layout(self.x,self.y,self.w,self.h)

  # --- post layout event   --------------------------------------------------

  def post_layout(self):
    """ post layout event """

    fbgui.App.logger.msg("TRACE","posting layout-event from %s" % self._id)
    event = pygame.fastevent.Event(fbgui.EVENT,
                                   code=fbgui.EVENT_CODE_LAYOUT,
                                   widget=self)
    pygame.fastevent.post(event)

  # --- handle internal event   ----------------------------------------------

  def _handle_internal_event(self,event):
    """ handle internal event (subclasses must override this method) """
    pass

  # --- post redraw event   --------------------------------------------------

  def post_redraw(self):
    """ post redraw event """

    fbgui.App.logger.msg("TRACE","posting redraw-event from %s" % self._id)
    event = pygame.fastevent.Event(fbgui.EVENT,
                                   code=fbgui.EVENT_CODE_REDRAW,
                                   widget=self)
    pygame.fastevent.post(event)

  # --- handle event   -------------------------------------------------------

  def handle_event(self,event):
    """ handle events """

    # multiplex events
    if event.type == pygame.MOUSEMOTION:
      return self.on_mouse_motion(event)
    elif event.type == pygame.MOUSEBUTTONUP:
      return self.on_mouse_btn_up(event)
    elif event.type == pygame.MOUSEBUTTONDOWN:
      return self.on_mouse_btn_down(event)
    elif event.type == fbgui.EVENT:
      return self._handle_internal_event(event)
    else:
      return False

  # --- handle mouse-motion events    ----------------------------------------

  def on_mouse_motion(self,event):
    """ handle mouse-motion events """

    if self._draw_rect.collidepoint(event.pos):
      fbgui.App.logger.msg("TRACE","on_mouse_motion for %s" % self._id)
      self._state = Widget.MOUSE_HOVER
    else:
      self._state = Widget.MOUSE_NORMAL
    self._set_colors()
    return False

  # --- handle mouse-button down events    ----------------------------------

  def on_mouse_btn_down(self,event):
    """ handle mouse-button down events """

    if self._draw_rect.collidepoint(event.pos):
      fbgui.App.logger.msg("TRACE",
                    "on_mouse_btn_down for %s: %r" % (self._id,event.pos))
      self._state = Widget.MOUSE_DOWN
      self._set_colors()
      if hasattr(self,'on_click'):
        fbgui.App.logger.msg("TRACE","delegate to on_click of %s" % self._id)
        return getattr(self,'on_click')(self,event)
    return False

  # --- handle mouse-button up events    ------------------------------------

  def on_mouse_btn_up(self,event):
    """ handle mouse-button up events """

    if self._draw_rect.collidepoint(event.pos):
      fbgui.App.logger.msg("TRACE","on_mouse_btn_up for %s" % self._id)
      self._state = Widget.MOUSE_HOVER
      self._set_colors()
    return False

  # --- redraw widget   ------------------------------------------------------

  def draw(self):
    """ draw the widget """

    # subclasses must implement their own logic here
    pass

  # --- set clipping area   ---------------------------------------------------

  def _clip_push(self):
    """ set the clipping area to the current drawing-rectangle """

    self._old_clip = fbgui.App.display.screen.get_clip()
    new_clip       = self._draw_rect.clip(self._old_clip)
    fbgui.App.display.screen.set_clip(new_clip)

  # --- restore clipping area   -----------------------------------------------

  def _clip_pop(self):
    """ restore the clipping area to the old state """

    if hasattr(self,'_old_clip'):
      fbgui.App.display.screen.set_clip(self._old_clip)
    else:
      assert False, "ERROR: invalid clip_pop"
