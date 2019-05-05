#!/usr/bin/python3

import fbgui

if __name__ == '__main__':

  config            = fbgui.Settings()
  config.msg_level  = "DEBUG"
  config.font_size  = 40
  config.width      = 320
  config.height     = 240
  config.title      = "Hello World 1"

  app   = fbgui.App(config)
  label = fbgui.Label("id1","Hello World",toplevel=True)
  label.pack()
  app.set_widget(label)
  app.run()
