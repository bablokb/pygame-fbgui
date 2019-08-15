#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# An image widget. The image is automatcally scaled to the requested size.
#
# Additional settings:
#   - scale:    scale image:  False (default) or True
#   - min_size: minimum size if scaled: native size (default) or (w,h)
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
  
  def __init__(self,id,img=None,settings=fbgui.Settings(),
                                                  toplevel=False,parent=None):
    """ constructor """

    super(Image,self).__init__(id,settings=settings,
                              toplevel=toplevel,parent=parent)
    self._scale = getattr(settings,'scale',False)
    self._min_size = getattr(settings,'min_size',(-1,-1))
    if not type(self._min_size) is tuple:
      self._min_size = (self._min_size,self._min_size)
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
        self.post_layout()
      else:
        # only content changed, so post a redraw-event
        self.post_redraw()
      
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
      if self._min_size[0] == -1:
        self.w_min = self._rect.w
      else:
        self.w_min = self._min_size[0]
      if self._min_size[1] == -1:
        self.h_min = self._rect.h
      else:
        self.h_min = self._min_size[1]
      self._is_size_valid = True
      return
      
    if not from_parent_w:
      self.w_min = self._rect.w
    if not from_parent_h:
      self.h_min = self._rect.h

    fbgui.App.logger.msg("TRACE","min_size (%s): (%d,%d)" %
                                             (self._id,self.w_min,self.h_min))
    self._is_size_valid = True

  # --- redraw widget   ------------------------------------------------------

  def draw(self,surface=None):
    """ draw the widget """

    # surface is None for redraw events, so save surface
    if surface is not None:
      self._surface = surface

    if not self._img:
      return

    # scale image to new dimension if necessary
    if self._scale and not (self.screen.w == self._scaled_rect.w and
        self.screen.h == self._scaled_rect.h):
      self._scaled_surface = (
        pygame.transform.scale(self._raw_surface,(self.screen.w,self.screen.h)))
      self._scaled_rect = self._scaled_surface.get_rect()

    # blit the image to the target position
    pos = self._align(self._scaled_rect)

    # implement clipping
    self._clip_push()
    self._surface.blit(self._scaled_surface,pos)
    self._clip_pop()
