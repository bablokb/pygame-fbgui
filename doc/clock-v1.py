#!/usr/bin/python3

import fbgui

class Clock(fbgui.App):
  def __init__(self,settings=fbgui.Settings()):
    super(Clock,self).__init__(settings=settings)
    self._create_widgets()
    self._main.pack()
    self.set_widget(self._main)

  def _create_widgets(self):
    self._main = fbgui.VBox("main",
                      settings=fbgui.Settings({
                        'padding': 5
                      }),toplevel=True)
    fbgui.VGap("gap1",
               settings=fbgui.Settings({
                 'width': 10,
                 'weight': 1
               }),parent=self._main)
    self._dlabel = fbgui.Label("dlabel","Sa 04.05.2019",
                               settings=fbgui.Settings({
                                 'font_size': self.theme.font_size_s,
                                 'align': fbgui.CENTER
                               }),parent=self._main)
    self._tlabel = fbgui.Label("tlabel","14:23:12",
                               settings=fbgui.Settings({
                                 'font_size': self.theme.font_size_xxl,
                                 'align': fbgui.CENTER
                               }),parent=self._main)
    fbgui.VGap("gap2",
               settings=fbgui.Settings({
                 'width': 10,
                 'weight': 1
               }),parent=self._main)

if __name__ == '__main__':

  config               = fbgui.Settings()
  config.msg_level     = "DEBUG"
  config.font_size     = 40
  config.width         = 320
  config.height        = 240
  config.font_size_s   = 24
  config.font_size_xxl = 60
  config.title         = "Clock v1"

  app   = Clock(config)
  app.run()
