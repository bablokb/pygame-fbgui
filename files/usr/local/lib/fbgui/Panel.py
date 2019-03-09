#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# The base class for all Panels: panels are widget-collections and don't
#                                draw anything themselves (except background)
#
# Additional settings:
#
#  - margins: single value or (left,right,top,bottom)
#  - radius: radius of rounded corners (default: 0.0)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import pygame
import fbgui.Widget

class Panel(fbgui.Widget):
  """ base class for all Panels """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,settings=fbgui.Settings(),toplevel=False,parent=None):
    """ constructor """

    super(Panel,self).__init__(id,settings=settings,
                               toplevel=toplevel,parent=parent)

    self.margins = getattr(settings,'margins',(0,0,0,0))
    self._radius = getattr(settings,'radius',0.0)
    if not type(self.margins) is tuple:
      self.margins = (self.margins,self.margins,self.margins,self.margins)

    self._childs    = []

  # --- add child   ----------------------------------------------------------

  def add(self,widget):
    """ add a child widget """

    self._childs.append(widget)
    widget._set_parent(self)

  # --- remove child   -------------------------------------------------------

  def remove(self,widget,refresh=False):
    """ remove a child widget """

    self._childs.remove(widget)
    if refresh:
      self.post_layout()

  # --- remove all child   ---------------------------------------------------

  def remove_all(self,refresh=False):
    """ remove all child widgets """

    del self._childs[:]
    if refresh:
      self.post_layout()

  # --- invalidate size information   ----------------------------------------

  def _invalidate(self):
    """ (recursively) invalidate size-information """

    super(Panel,self)._invalidate()
    for child in self._childs:
      child._invalidate()

  # --- query minimum size   -------------------------------------------------

  def _calc_minimum_size(self,w,h):
    """ query minimum size of widget """

    if self._is_size_valid:
      return

    # calculate size of panel
    from_parent_w,from_parent_h = self._set_size_from_parent(w,h)
    self.w_min = max(self.w_min,self.margins[0]+self.margins[1])
    self.h_min = max(self.h_min,self.margins[2]+self.margins[3])

    # calculate size of all children
    w_min = 0
    h_min = 0
    for child in self._childs:
      child._calc_minimum_size(self.w,self.h)
      w_min = max(w_min,child.w_min)
      h_min = max(h_min,child.h_min)

    if not from_parent_w:
      self.w_min = max(self.w_min,w_min)
    if not from_parent_h:
      self.h_min = max(self.h_min,h_min)
    fbgui.App.logger.msg("TRACE",
                 "min_size (%s): (%d,%d)" % (self._id,self.w_min,self.h_min))
    self._is_size_valid = True

  # --- layout widget   ------------------------------------------------------

  def _layout(self,x,y,w,h):
    """ layout widget """

    self._std_layout(x,y,w,h)

    # correct values for margins
    x = x + self.margins[0]
    y = y + self.margins[2]
    w = w - self.margins[0] - self.margins[1]
    h = h - self.margins[2] - self.margins[3]
    fbgui.App.logger.msg("TRACE","x,y,w,h (%s childs): (%d,%d,%d,%d)" %
                         (self._id,x,y,w,h))
    
    # now layout children
    for child in self._childs:

      # horizontal alignment
      if child.align[0] == fbgui.LEFT:
        x_c = x
      elif child.align[0] == fbgui.RIGHT:
        x_c = x + w - child.w_min
      else:
        x_c = x + int((w - child.w_min)/2)

      # vertical alignment
      if child.align[1] == fbgui.TOP:
        y_c = y
      elif child.align[1] == fbgui.BOTTOM:
        y_c = y + h - child.h_min
      else:
        y_c = y + int((h - child.h_min)/2)

      child._layout(x_c,y_c,child.w_min,child.h_min)

  # --- handle event   -------------------------------------------------------

  def handle_event(self,event):
    """ handle events """

    # either one of our childs handles the event, or we do it ourselves
    # we iterate the reversed list, since last added child is on top (drawn last)
    for child in reversed(self._childs):
      if child.handle_event(event):
        return True
    return super(Panel,self).handle_event(event)

  # --- draw rounded rectangle   ---------------------------------------------

  def _draw_rounded(self,color):
    """ draw rectangle with rounded corners """

    rect           = pygame.Rect(self._draw_rect)
    draw_color     = pygame.Color(color.r,color.g,color.b,0)
    alpha          = color.a
    pos            = rect.topleft
    rect.topleft   = (0,0)
    surface        = pygame.Surface(rect.size,pygame.SRCALPHA)
    circle_surface = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)

    # create ellipse
    pygame.draw.ellipse(circle_surface,(0,0,0),circle_surface.get_rect(),0)
    circle_surface = pygame.transform.smoothscale(circle_surface,
                                       [int(min(rect.size)*self._radius)]*2)

    # blit topleft (dest is rectangle with size of circle_surface)
    dest = surface.blit(circle_surface,(0,0))

    # move to bottom-right and blit
    dest.bottomright = rect.bottomright
    surface.blit(circle_surface,dest)

    # move to top-right and blit
    dest.topright = rect.topright
    surface.blit(circle_surface,dest)

    # move to bottom-left and blit
    dest.bottomleft = rect.bottomleft
    surface.blit(circle_surface,dest)

    # fill target surface with black
    surface.fill(fbgui.Color.BLACK,rect.inflate(-dest.w,0))
    surface.fill(fbgui.Color.BLACK,rect.inflate(0,-dest.h))

    # now fill with target color, recovering color and alpha
    surface.fill(draw_color,special_flags=pygame.BLEND_RGBA_MAX)
    surface.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)

    fbgui.App.display.screen.blit(surface,(self.screen.x,self.screen.y))

  # --- redraw widget   ------------------------------------------------------

  def draw(self):
    """ draw the widget """

    color = self._get_bg_color()

    if not self._parent or not fbgui.Color.eq(color,self._parent.theme.bg_color):
      if self._radius == 0.0:
        fbgui.App.display.screen.fill(color,rect=self._draw_rect)
      else:
        self._draw_rounded(color)

    for child in self._childs:
      child.draw()
