#!/usr/bin/python3

import fbgui

if __name__ == '__main__':

  config            = fbgui.Settings()
  config.msg_level  = "DEBUG"
  config.bg_color   = fbgui.Color.LIGHTBLUE
  config.fg_color   = fbgui.Color.WHITE
  config.font_size  = 40
  config.width      = 320
  config.height     = 240
  config.title      = "Hello World 2"

  app   = fbgui.App(config)
  label = fbgui.Label("id1","Hello World",
                      settings=fbgui.Settings({
                        'align': (fbgui.CENTER,fbgui.CENTER),
                        'fg_color': fbgui.Color.YELLOW
                      }),toplevel=True)
  label.pack()
  app.set_widget(label)
  app.run()
