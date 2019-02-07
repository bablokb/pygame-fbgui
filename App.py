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

import fbgui

class App(object):
  """ Application based on pygame """

  display = None
  theme   = None
  logger  = None

  # --- create font   ---------------------------------------------------------

  @staticmethod
  def create_font(name,size,path='.'):
    """ create font (either systemfont from name or font from file """

    App.logger.msg("DEBUG","creating font: %s (%dpt)" % (name,size))
    if name.find('.') > -1:
      # name is path to font-file
      try:
        if name.find(os.sep) > -1:
          return pygame.freetype.Font(name,size)
        else:
          return pygame.freetype.Font(os.path.join(path,name),size)
      except:
        App.logger.msg("ERROR", "could not create font for: %s" % name)
        App.logger.msg("INFO",  "using fallback-font FreeSans")
        # use fallback
        return pygame.freetype.SysFont("freesansbold",size)
    else:
      return pygame.freetype.SysFont(name,size)

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,settings=fbgui.Settings()):
    "Ininitializes the pygame display using the framebuffer"

    self._widget = None

    # create global message-logger
    App.logger      = fbgui.Msg()
    fbgui.Msg.level = getattr(settings,"msg_level","INFO")

    # global display object
    App.display = fbgui.Settings({
      'screen':    None,
      'title':     "Application-Title",
      'width':     800,
      'height':    600,
      'size':      (800,600)
      })
    App.display.copy(settings)

    # global theme settings
    App.theme = fbgui.Settings({
      'bg_color':     fbgui.Color.WHITE,
      'fg_color':     fbgui.Color.BLACK,
      'default_font': None,
      'font_path':    ".",
      'font_name':    "FreeSans",
      'font_size':     12,
      'font_size_s':    8,
      'font_size_m':   12,
      'font_size_l':   16,
      'font_size_xl':  20,
      'font_size_xxl': 24
    })
    App.theme.copy(settings)

    # initialize physical display, fonts and event-system
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
      App.display.size    = (App.display.width,App.display.height)
      App.display.screen  = pygame.display.set_mode(App.display.size)
      if App.display.title:
        pygame.display.set_caption(App.display.title)
      App.logger.msg("DEBUG",
                  "created X-based display with size: %d,%d" % App.display.size)
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
        
      App.display.size   = (pygame.display.Info().current_w,
                               pygame.display.Info().current_h)
      App.display.width  = App.display.size[0]
      App.display.height = App.display.size[1]
      App.display.screen = pygame.display.set_mode(App.display.size,
                                              pygame.FULLSCREEN)
      App.logger.msg("DEBUG",
                "created fullscreen display with size: %r" % App.display.size)

  # --- initialize font support   --------------------------------------------

  def _init_font(self):
    """ initialize font support """

    pygame.freetype.init()
    if not App.theme.default_font:
      App.theme.default_font = App.create_font(App.theme.font_name,
                                                App.theme.font_size)

  # --- process internal event   ----------------------------------------------

  def _process_internal_event(self,event):
    """ process internal event """

    App.logger.msg("DEBUG", "processing event with code %d" % event.code)

    if event.code == fbgui.EVENT_CODE_LAYOUT:
      App.logger.msg("DEBUG", "layout event from widget %s" % event.widget._id)
      if self._widget:
        self._widget.pack()
        self._widget.draw()
        pygame.display.flip()
    elif event.code == fbgui.EVENT_CODE_REDRAW:
      App.logger.msg("DEBUG", "redraw event for widget %s" % event.widget._id)
      event.widget.draw()
      pygame.display.flip()
    else:
      # no other internal events are supported yet
      assert False, "undefined event-code: %d" % event.code

  # --- set top-level widget   ------------------------------------------------

  def set_widget(self,widget):
    """ set top-level widget """

    self._widget = widget

  # --- process quit-event   --------------------------------------------------

  def on_quit(self):
    """ process quit """

    # the default implementation just quits pygame
    pygame.quit()

  # --- process generic event   -----------------------------------------------

  def on_event(self):
    """ process event """

    if self._widget:
      self._widget.draw()
      pygame.display.flip()

  # --- main event loop   -----------------------------------------------------

  def run(self):
    """ main event loop """
    
    while True:
      event = pygame.fastevent.wait()
      if event.type == pygame.QUIT:
        self.on_quit()
        return
      elif event.type == fbgui.EVENT:
        self._process_internal_event(event)
      else:
        self.on_event()
