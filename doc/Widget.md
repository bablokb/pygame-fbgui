Widget
======

This is the common base class of all widgets and contains common settings
and methods shared by all widget-classes. This class should not be
instantiated directly.


Hierarchy
---------

  - Widget


Settings
--------

| Name          | Description           | Default                         |
|---------------|-----------------------|---------------------------------|
| x             | x-coordinate          | -1 or 0 (toplevel)              |
| y             | y-coordinate          | -1 or 0 (toplevel)              |
| width         | width                 | 0 or display-width (toplevel)   |
| height        | height                | 0 or display-height (toplevel)  |
| weight        | share of free space   | 0                               |
| align         | alignment             | (LEFT,BOTTOM)                   |

Toplevel widgets always have `(x,y) = (0,0)` and `width` and `height` are
automatically set to the display width and heigt.

If `x` or `y` is `-1`, then the layout determinates the position of the
widget on the screen.

If `width` or `height` are `0`, the size in the respective dimension
is determined by the layout. If the widget defines a minimum size, the
layout at least reserves this size for the widget.

If `0 <= width,height <= 1.0`, the size of the widget is relative to
the size of the parent. If `1 <= width, height`, the size is abslute.

**Note that there is a subtle difference between `width=1.0` and `width=1`.
The former sets the width to 100% of the parent width, the latter sets
the width to one pixel.**


Public Methods
--------------

| Name                       | Description                                      |
|--------------------- ------|--------------------------------------------------|
| id()                       | return the id of the widget                      |
| pack()                     | trigger layout of widget tree (only toplevel)    |
| post_layout()              | trigger layout (including redraw)                |
| post_redraw()              | trigger redraw of widget                         |
| handle_event(event)        | process pygame-events for this widget            |
| on_mouse_motion(event)     | process mouse-motion event                       |
| on_mouse_btn_down(event)   | process mouse-button down event                  |
| on_mouse_btn_up(event)     | process mouse-button up event                    |
| is_selected()              | return selection-state of widget                 |
| set_selected(state)        | set selection-state of widget                    |
| toggle_selected()          | toggle selection-state of widget                 |


You should call `post_layout()` or `post_redraw()` if you change the state of
a widget and want to request a complete redraw of the GUI or only want to
redraw the given widget. This also works from other threads.

Note that you usually don't have to override the `on_mouse_xxx` methods.

To receive click-events, simply add a `on_click`-method to your widget
instance, e.g.

    def run_action(widget,event):
      fbgui.App.logger.msg("INFO","click for %s" % widget.id())

    clickable_text = fbgui.Label("click me")
    clickable_text.on_click = lambda widget,event: run_action(widget,event)

You could also subclass `Label` and add a `on_click`-method to the subclass.
