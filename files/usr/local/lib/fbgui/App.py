#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Application based on pygame.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pygame-fbgui
#
# ----------------------------------------------------------------------------

import os, glob

import pygame
import pygame.freetype

import fbgui

class App(object):
  """ Application based on pygame """

  display    = None
  theme      = None
  logger     = None
  font_cache = {}

  # --- find font relative to a basedir   -------------------------------------

  @staticmethod
  def find_font(name,path='.'):
    """ find font-file relative to a directory """

    if os.path.isabs(name):
      return name
    else:
      font = glob.glob(os.path.join(path,"**",name),recursive=True)
      if len(font):
        return font[0]
      else:
        return None

  # --- create font   ---------------------------------------------------------

  @staticmethod
  def create_font(name,size,path='.'):
    """ create font (either systemfont from name or font from file """

    font = App.font_cache.get((name,size))
    if font:
      App.logger.msg("TRACE","reusing font: %s (%dpt)" % (name,size))
      return font

    App.logger.msg("TRACE","creating font: %s (%dpt)" % (name,size))
    if name.find('.') > -1:
      # name is path to font-file
      fname = App.find_font(name,path)
      if fname:
        App.font_cache[(name,size)] = pygame.freetype.Font(fname,size)
      else:
        App.logger.msg("ERROR", "could not create font for: %s" % name)
        App.logger.msg("INFO",  "using fallback-font FreeSansBold")
        # use fallback
        App.font_cache[(name,size)] = pygame.freetype.SysFont("freesansbold",size)
    else:
      # name is a sysfont-name
      App.font_cache[(name,size)] = pygame.freetype.SysFont(name,size)
    return App.font_cache[(name,size)]

  # --- constructor   --------------------------------------------------------
  
  def __init__(self,settings=fbgui.Settings()):
    "Ininitializes the pygame display using the framebuffer"

    self._widget = None

    # create global message-logger
    App.logger = fbgui.Msg(getattr(settings,"msg_level","INFO"),
                           getattr(settings,"msg_syslog",False))

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
    fpath = os.getenv('FONTPATH')
    if not fpath:
      fpath = '/usr/share/fonts'
    App.theme = fbgui.Settings({
      'bg_color':       fbgui.Color.WHITE,
      'bg_color_down':  None,
      'bg_color_hover': None,
      'fg_color':       fbgui.Color.BLACK,
      'default_font':   None,
      'font_path':      fpath,
      'font_name':      "FreeSans",
      'font_size':      12,
      'font_size_s':     8,
      'font_size_m':    12,
      'font_size_l':    16,
      'font_size_xl':   20,
      'font_size_xxl':  24
    })
    App.theme.copy(settings)

    # define default (do-nothing) colors for hover/down
    if not App.theme.bg_color_down:
      App.theme.bg_color_down = App.theme.bg_color
    if not App.theme.bg_color_hover:
      App.theme.bg_color_hover = App.theme.bg_color

    # define color for selections
    if not App.theme.fg_color_selected:
      App.theme.fg_color_selected = App.theme.bg_color
    if not App.theme.bg_color_selected:
      App.theme.bg_color_selected = App.theme.fg_color

    # initialize physical display, fonts and event-system
    self._init_display(settings)
    self._init_font()
    pygame.fastevent.init()

    # change visibility of mouse
    pygame.mouse.set_visible(getattr(settings,'mouse_visible',True))

  # --- initialize pygame display   ------------------------------------------
  
  def _init_display(self,settings):
    """ initialize pygame display

      Based on 'Python GUI in Linux frame buffer'
      http://www.karoltomala.com/blog/?p=679
    """

    # query and set framebuffer-device
    if hasattr(settings,"fb_device"):
      os.environ["SDL_FBDEV"] = settings.fb_device
    elif os.path.exists("/dev/fb1"):
      os.environ["SDL_FBDEV"] = "/dev/fb1"
    else:
      os.environ["SDL_FBDEV"] = "/dev/fb0"
    App.logger.msg("TRACE","SDL_FBDEV: %s" % os.environ["SDL_FBDEV"])

    # check for X-environment
    have_X = os.getenv("DISPLAY")
    App.logger.msg("TRACE","have X: %r" % have_X)

    # query mouse-device and driver
    if not have_X:
      if hasattr(settings,'mouse_dev'):
        dev_file = getattr(settings,'mouse_dev')
      else:
        for dev in ['touchscreen','ts_uinput','ts','event0']:
          dev_file = os.path.join('/dev/input',dev)
          if os.path.exists(dev_file):
            break
      if dev_file:
        App.logger.msg("TRACE","SDL_MOUSEDEV: %s" % dev_file)
        os.environ["SDL_MOUSEDEV"] = dev_file
        mouse_drv = getattr(settings,'mouse_drv','TSLIB')
        if mouse_drv:
          App.logger.msg("TRACE","SDL_MOUSEDRV: %s" % mouse_drv)
          os.environ["SDL_MOUSEDRV"] = mouse_drv

    # initilize display
    if have_X:
      pygame.display.init()
      App.display.size    = (App.display.width,App.display.height)
      App.display.screen  = pygame.display.set_mode(App.display.size)
      if App.display.title:
        pygame.display.set_caption(App.display.title)
      App.logger.msg("TRACE",
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
            App.logger.msg("TRACE","using SDL-driver: %s" % driver)
            found = True
            break
          except pygame.error:
            App.logger.msg("TRACE","Driver: %s failed." % driver)

      if not found:
        raise Exception('No suitable video driver found!')

      d_info = pygame.display.Info()
      App.logger.msg("TRACE",
                     "bits per pixel: %d, bytes per pixel: %d" %
                     (d_info.bitsize,d_info.bytesize))
      App.display.size   = (d_info.current_w,d_info.current_h)
      App.display.width  = App.display.size[0]
      App.display.height = App.display.size[1]
      App.display.screen = pygame.display.set_mode(App.display.size,
                                              pygame.FULLSCREEN)
      App.logger.msg("TRACE",
             "created fullscreen display with size: %d,%d" % App.display.size)

  # --- initialize font support   --------------------------------------------

  def _init_font(self):
    """ initialize font support """

    pygame.freetype.init()
    if not App.theme.default_font:
      App.theme.default_font = App.create_font(App.theme.font_name,
                                                App.theme.font_size,App.theme.font_path)

  # --- process internal event   ----------------------------------------------

  def _process_internal_event(self,event):
    """ process internal event """

    App.logger.msg("TRACE", "processing event with code %d" % event.code)

    if event.code == fbgui.EVENT_CODE_LAYOUT:
      App.logger.msg("TRACE", "layout event from widget %s" % event.widget._id)
      self._draw_widget(True)
    elif event.code == fbgui.EVENT_CODE_REDRAW:
      App.logger.msg("TRACE", "redraw event for widget %s" % event.widget._id)
      event.widget.draw()
      pygame.display.flip()
    elif event.code == fbgui.EVENT_CODE_WIDGET:
      App.logger.msg("TRACE", "widget event for widget %s" % event.widget._id)
      event.widget.handle_event(event)
    else:
      # no other internal events are supported yet
      assert False, "undefined event-code: %d" % event.code

  # --- draw top-level widget   -----------------------------------------------

  def _draw_widget(self,pack=False):
    """ draw top-level widget """

    App.display.screen.fill(App.theme.bg_color)
    if self._widget:
      if pack:
        self._widget.pack()
      self._widget.draw()
    pygame.display.flip()

  # --- set top-level widget   ------------------------------------------------

  def set_widget(self,widget):
    """ set top-level widget """

    self._widget = widget

  # --- process start-event   -------------------------------------------------

  def on_start(self):
    """ actions just before starting main-event loop """

    pass

  # --- process quit-event   --------------------------------------------------

  def on_quit(self,rc=0):
    """ process quit """

    # the default implementation just quits pygame
    pygame.quit()
    return rc

  # --- process generic event   -----------------------------------------------

  def on_event(self,event):
    """ process event """

    if self._widget:
      etype = event.type
      if etype in (pygame.MOUSEMOTION,
                   pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
        self._widget.handle_event(event)
    self._draw_widget()

  # --- main event loop   -----------------------------------------------------

  def run(self):
    """ main event loop """

    self._draw_widget()
    self.on_start()
    while True:
      event = pygame.fastevent.wait()
      App.logger.msg("TRACE", "processing event %d" % event.type)
      if event.type == pygame.QUIT:
        if hasattr(event,'rc'):
          rc = event.rc
        else:
          rc = 0
        return self.on_quit(rc)
      elif event.type == fbgui.EVENT:
        self._process_internal_event(event)
      else:
        self.on_event(event)
