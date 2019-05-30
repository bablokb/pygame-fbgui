#!/usr/bin/python3

import fbgui
import time, datetime, threading, locale

class Clock(fbgui.App):
  def __init__(self,settings=fbgui.Settings()):
    super(Clock,self).__init__(settings=settings)
    self._create_widgets()
    self._main.pack()
    self.set_widget(self._main)

  def _create_widgets(self):
    self._main = fbgui.Panel("main",
                             settings=fbgui.Settings({
                             }),toplevel=True)
    self._vbox = fbgui.VBox("vbox",
                            settings=fbgui.Settings({
                             'margins': 20,
                             'radius': 0.2,
                             'align': fbgui.CENTER,
                             'bg_color': fbgui.Color.SILVER,
                             'padding': 10
                            }),parent=self._main)
    self._dlabel = fbgui.Label("dlabel","Sa 04.05.2019",
                               settings=fbgui.Settings({
                                 'font_size': self.theme.font_size_s,
                                 'align': fbgui.CENTER
                               }),parent=self._vbox)
    self._tlabel = fbgui.Label("tlabel","14:23:12",
                               settings=fbgui.Settings({
                                 'font_name': "DSEG7Classic-Bold.ttf",
                                 'font_size': self.theme.font_size_xxl,
                                 'align': fbgui.CENTER
                               }),parent=self._vbox)

  def _update(self):
    locale.setlocale(locale.LC_ALL, '')
    delay = 0.5
    while True:
      time.sleep(delay)
      now = datetime.datetime.now()
      try:
        self._dlabel.set_text(now.strftime("%a %x"))
        self._tlabel.set_text(now.strftime("%H:%M:%S"))
      except:
        break

  def on_start(self):
    threading.Thread(target=self._update).start()

if __name__ == '__main__':
  config               = fbgui.Settings()
  config.msg_level     = "DEBUG"
  config.font_size     = 40
  config.width         = 320
  config.height        = 240
  config.font_size_s   = 24
  config.font_size_xxl = 52
  config.title         = "Clock v3"

  app   = Clock(config)
  app.run()
