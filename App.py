#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Application based on pygame.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import os

import pygame
import pygame.freetype

import fbgui.Settings as Settings
import fbgui.Color    as Color

class App(object):
  """ Application based on pygame """

  display = None
  theme   = None

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,settings=Settings()):
    "Ininitializes the pygame display using the framebuffer"

    App.app        = self
    self.display   = Settings({
      'title':     "Application-Title",
      'width':     800,
      'height':    600,
      'size':      (800,600)
      })
    self.display.copy(settings)

    App.theme = Settings({
      'bg_color':     Color.WHITE,
      'fg_color':     Color.BLACK,
      'default_font': None,
      'font_name':    "FreeSans.ttf",
      'font_size':    12
    })
    App.theme.copy(settings)

    self._init_display(settings)
    self._init_font()
    pygame.fastevent.init()

  # --- initialize pygame display   ------------------------------------------
  
  def _init_display(self,settings):
    """ initialize pygame display

      Based on 'Python GUI in Linux frame buffer'
      http://www.karoltomala.com/blog/?p=679
    """
    
    if hasattr(settings,"fb_device"):
      os.environ["SDL_FBDEV"] = settings.fb_device
    else:
      os.environ["SDL_FBDEV"] = "/dev/fb1"
    have_X = os.getenv("DISPLAY")

    if have_X:
      pygame.display.init()
      self.display.size   = (self.display.width,self.display.height)
      App.display         = pygame.display.set_mode(self.display.size)
      if self.display.title:
        pygame.display.set_caption(self.display.title)
    else:
      # Check which frame buffer drivers are available
      # Start with fbcon since directfb hangs with composite output
      drivers = ['fbcon', 'directfb', 'svgalib']
      found = False
      for driver in drivers:
        # Make sure that SDL_VIDEODRIVER is set
        if not os.getenv('SDL_VIDEODRIVER'):
          os.putenv('SDL_VIDEODRIVER', driver)
          try:
            pygame.display.init()
            found = True
            break
          except pygame.error:
            print 'Driver: {0} failed.'.format(driver)
    
        if not found:
          raise Exception('No suitable video driver found!')
        
        self.display.size   = (pygame.display.Info().current_w,
                               pygame.display.Info().current_h)
        self.display.width  = self.display.size[0]
        self.display.height = self.display.size[1]
        App.display         = pygame.display.set_mode(self.display.size,
                                              pygame.FULLSCREEN)

  # --- initialize font support   --------------------------------------------

  def _init_font(self):
    """ initialize font support """

    pygame.freetype.init()
    if not App.theme.default_font:
      App.theme.default_font = pygame.freetype.SysFont(App.theme.font_name,
                                                App.theme.font_size)

  # --- main event loop   -----------------------------------------------------

  def run(self):
    """ main event loop """
    
    while True:
      event = pygame.fastevent.wait()
      if event.type == pygame.QUIT:
        return

      App.display.fill(App.theme.bg_color)
      pygame.display.flip()

  # --- terminate application   ----------------------------------------------

  def quit(self):
    """ terminate application """
    pygame.quit()
