#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# An image widget. The image is automatcally scaled to the requested size.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import pygame

import fbgui

class Image(fbgui.Widget):
  """ draw an image """

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,id,img,settings=None,toplevel=False,parent=None):
    """ constructor """

    super(Image,self).__init__(id,settings=settings,
                              toplevel=toplevel,parent=parent)
    self._scale = getattr(settings,'scale',False)
    self._img = None
    self.set_image(img,refresh=False)

  # --- set the image of this Image   ----------------------------------------

  def set_image(self,img,refresh=True):
    """ set the image of the Image """

    if img == self._img:
      return
    fbgui.App.logger.msg("TRACE","changing image of Image %s" % self._id)

    if img:
      self._raw_surface = pygame.image.load(img).convert()
      self._rect = self._raw_surface.get_rect()
    else:
      self._raw_surface = None
      self._rect        = None

    self._scaled_surface = self._raw_surface
    self._scaled_rect    = self._rect
    self._img = img

    if refresh:
      if not self._scale:
        # post a layout-event
        fbgui.App.logger.msg("TRACE","posting layout-event from %s" % self._id)
        event = pygame.fastevent.Event(fbgui.EVENT,
                                       code=fbgui.EVENT_CODE_LAYOUT,
                                       widget=self)
        pygame.fastevent.post(event)
      else:
        # only content changed, so post a redraw-event
        fbgui.App.logger.msg("TRACE","posting redraw-event from %s" % self._id)
        event = pygame.fastevent.Event(fbgui.EVENT,
                                       code=fbgui.EVENT_CODE_REDRAW,
                                       widget=self)
        pygame.fastevent.post(event)
      
  # --- query minimum size   -------------------------------------------------

  def _calc_minimum_size(self,w,h):
    """ query minimum size of widget """

    if self._is_size_valid:
      return

    from_parent_w,from_parent_h = self._set_size_from_parent(w,h)
    if not self._img:
      self._is_size_valid = True
      return
    elif self._scale:
      self.w_min = 1
      self.h_min = 1
      self._is_size_valid = True
      return
      
    if not from_parent_w:
      self.w_min = self._rect.w
    if not from_parent_h:
      self.h_min = self._rect.h

    fbgui.App.logger.msg("TRACE","min_size (%s): (%d,%d)" %
                                             (self._id,self.w_min,self.h_min))
    self._is_size_valid = True

  # --- layout widget   ------------------------------------------------------

  def _layout(self,x,y,w,h):
    """ layout widget:
          x,y: target-position as defined by the parent
          w,h: width and height of parent (adapted by e.g. margins)
    """

    # call the standard-layout mechanism
    self._std_layout(x,y,w,h)

    # if we are scalable, use argument w,h
    if self._scale:
      self.screen.w = w
      self.screen.h = h
    else:
      self.screen.w = self.w_min
      self.screen.h = self.h_min

    fbgui.App.logger.msg("TRACE","layout (%s): (%d,%d,%d,%d)" %
           (self._id,self.screen.x,self.screen.y,self.screen.w,self.screen.h))

  # --- redraw widget   ------------------------------------------------------

  def draw(self):
    """ draw the widget """

    if not self._img:
      return

    # scale image to new dimension if necessary
    if not (self.screen.w == self._scaled_rect.w and
        self.screen.h == self._scaled_rect.h):
      self._scaled_surface = (
        pygame.transform.scale(self._raw_surface,(self.screen.w,self.screen.h)))
      self._scaled_rect = self._scaled_surface.get_rect()

    # blit the image to the target position
    fbgui.App.display.screen.blit(self._scaled_surface,
                                    (self.screen.x,self.screen.y))
