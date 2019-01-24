#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# A class for color-constants
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-wstation
#
# ----------------------------------------------------------------------------

import pygame

class Color(object):
  """ Color constants """

  WHITE = pygame.Color("white")
  BLACK = pygame.Color("black")

  GRAY00  = pygame.Color(0,0,0)
  GRAY10  = pygame.Color(25,25,25)
  GRAY20  = pygame.Color(50,50,50)
  GRAY30  = pygame.Color(75,75,75)
  GRAY40  = pygame.Color(100,100,100)
  GRAY50  = pygame.Color(125,125,125)
  GRAY60  = pygame.Color(150,150,150)
  GRAY70  = pygame.Color(175,175,175)
  GRAY80  = pygame.Color(200,200,200)
  GRAY90  = pygame.Color(225,225,225)
  GRAY100 = pygame.Color(255,255,255)

  RED   = pygame.Color("red")
  GREEN = pygame.Color("green")
  BLUE  = pygame.Color("blue")

  RED25   = pygame.Color(64,0,0)
  GREEN25 = pygame.Color(0,64,0)
  BLUE25  = pygame.Color(0,0,64)

  RED50   = pygame.Color(128,0,0)
  GREEN50 = pygame.Color(0,128,0)
  BLUE50  = pygame.Color(0,0,128)

  RED75   = pygame.Color(192,0,0)
  GREEN75 = pygame.Color(0,192,0)
  BLUE75  = pygame.Color(0,0,192)
