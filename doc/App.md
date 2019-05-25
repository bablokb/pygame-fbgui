App
===

This is the main application class. Only create a single instance of this
class (or a subclass of `App`).

Hierarchy
---------

  - App

Settings
--------

| Name          | Description        | Default                         |
|---------------|--------------------|---------------------------------|
| title         | X11 title          | "Application-Title"             |
| width         | X11 window-width   | 800                             |
| height        | X11 window-height  | 600                             |
| mouse_visible | show mouse         | True                            |
| fb_device     | framebuffer-device | usually auto-detected           |
| mouse_dev     | mouse-device       | usually auto-detected           |
| mouse_drv     | mouse-driver       | TSLIB                           |


Public Methods
--------------

| Name          | Description                                          |
|---------------|------------------------------------------------------|
| set_widget    | set toplevel-widget of application                   |
| on_start      | action just before starting main event-loop          |
| on_quit       | process quit event after termination of event-loop   |
| on_event      | process pygame-events                                |
| run           | start main event-loop                                |
|               |                                                      |

If you override a method, call the super method after your own processing.
If you feel the need to override `set_widget` or `run`, please open an
issue, since this should normally be not necessary and is either a sign
of something missing within the library or a wrong application design.
