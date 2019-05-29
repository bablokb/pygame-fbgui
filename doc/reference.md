Pygame-fbgui Reference
======================

Table of Contents
-----------------

  1. [Architecture](#architecture "Architecture")
  2. [Settings](#settings "Settings")
  3. [Pygame Environment](#pygame-environment "Pygame Environment")
  4. [Events](#events "Events")
  5. [Colors](#colors "Colors")
  6. [Theming](#theming "Theming")
  7. [Fonts](#fonts "Fonts")
  8. [Logging](#logging "Logging")
  9. [Layouts](#layouts "Layouts")
 10. [Class Reference](#class-reference "Class Reference")


Architecture
------------

The library pygame-fbgui is a collection of classes:

  - `App`: For every application there is only one instance of this
    class. The class (or a subclass) runs the event-loop and is owner
    of the physical screen.
  - `Widgets`: This is a tree of classes implementing the user-interface
  - `Settings`: A value-holder class used to configure applications and
    widgets.
  - Some support classes

In contrast to most pygame-examples, the event-loop uses
`pygame.fastevent.wait()' instead of `pygame.event.get()`. The latter is
optimzed for games and puts the system under heavy load.

Another reason for using the `fastevent`-package instead of the `event`-package
is that `fastevent` supports multithreading. This enables posting events
from other threads to the main-eventloop e.g. to update the gui after
a long running process has finished.


Settings
--------

Almost all objects of the pygame-fbgui class-hierarchy accept a
[Settings](./Settings.md)-object in the constructor. `Settings` is mainly
a value-holder class. To initialize a `Settings`-object, you either pass
a dictionary, or you create the object and add the settings afterwards:

    settings = fbgui.Settings({'a': 1, 'b': 2, 'foo': 'bar'})

is equivalent to

    settings = fbgui.Settings()
    settings.a = 1
    settings.b = 2
    settings.foo = 'bar'


Pygame-Environment
------------------

Usually, the library takes care of the configuration of the pygame-environment
(display-device, mouse-device). You don't have to set the usual `SDL*`
variables yourself, instead pass the correct settings to the application class
(see class [App](./App.md) for details).


Events
------

The library uses the event-number `pygame.NUMVENTS-1` internally. For your
own events, only use `pygame.USEREVENT` up to `pygame.NUMEVENTS-2`.


Colors
------

The [Color](./Color.md)-class supports various color-constants, especially
all values of the predefined HTML-colors. Also available are shaded versions
of the basic colors, e.g. `fbgui.Colors.REDnnn` with `nnn` from `000` to
`100` in steps of 5.


Theming
-------

A theme consists of a number of predefined settings:

    'fg_color':       fbgui.Color.BLACK
    'bg_color':       fbgui.Color.WHITE

    'fg_color_selected':  App.theme.bg_color
    'bg_color_selected':  App.theme.fg_color

    'bg_color_hover': App.theme.bg_color
    'bg_color_down':  App.theme.bg_color

    'default_font':   None,  # use given font_name with given font_size
    'font_path':      '/usr/share/fonts',
    'font_name':      "FreeSans",
    'font_size':      12,
    'font_size_s':     8,
    'font_size_m':    12,
    'font_size_l':    16,
    'font_size_xl':   20,
    'font_size_xxl':  24

The list will probably expand in the future.

The toplevel window will inherit the theme from the application-object, and
child-widgets will inherit the theme from their parents. During widget
creation, you can override any theme-setting.


Fonts
-----

The library uses either builtin fonts or font-files. If you define a font-name
without an extension, the name is considered as a name of a builtin font.
Depending on your pygame-installation, pygame supplies a number of builtin
fonts (on Raspbian-Stretch this is only a single font).

The search-order of fonts is as follows:

  - if the font-name does not contain a dot, assume a builtin font
  - if the font-name is an absolute path, use the given path
  - otherwise, search the font relative to the `font_path`-setting

The default value for `font_path` is the value of the environment-variable
`FONTPATH` or `/usr/share/fonts` if that variable is empty or does not
exist.


Logging
-------

The main application object has builtin logger. To use the logger, call
the method `msg`:

    app = fbgui.App(...)
    app.msg_level  = "DEBUG"
    app.msg_syslog = True
    app.logger.msg(level,text)

`level` can be one of

  - "TRACE"
  - "DEBUG"
  - "INFO"
  - "WARN"
  - "ERROR"
  - "NONE"

The application-setting `msg_level` controls which messages are actually
printed (or sent to the system-log depending on `msg_syslog`). Note that
the library makes extensive use of the level "TRACE", so expect a lot of
noise if you use this level.


Layouts
-------

One of the main design goals of pygame-fbgui is the support of simple yet
powerful layout-mechanisms. All widgets of GUI have a size. There are three
alternatives to size a widget:

  - *absolute size* (`width` and `height` given in pixels)
  - *relative size* (`width` and `height` given as a fraction between 0.0 and 1.0)  
    The relative size is always relative to the parent.
  - *dynamic size*  
    Here, the size is dynamically calculated at runtime

Whenever possible, you should try to prevent using absolute sizes for
widgets, because if you switch the screen, the layout will not work anymore.
Typical exceptions are toplevel-widgets which are always absolute (they fill
the whole screen) and images.

Currently the library supports three layout mechanisms

  - *absolute*: you provide the coordinates of the upper left corner
  - *relative to the border*: any combination of `LEFT`, `CENTER`, `RIGHT`
    for the horizontal alignment and `TOP`, `CENTER`, `BOTTOM` for the
    vertical alignment
  - *flow*: layout the children in a horizontal or vertical manner

The class [Panels](./Panels.md) supports the relative layout. The classes
[HBox](./HBox.md) and [VBox](./VBox.md) support the flow-layout in horizontal
and vertical directions. In a later version of the library there will
be a [GridBox](./GridBox.md) supporting the flow-layout in two dimensions.


Class Reference
---------------


| Class                        | Description                                   |
| -----------------------------|-----------------------------------------------|
|[App](./App.md)               | The main application class                    |
|[Box](./Box.md)               | Base-class of `HBox` and `VBox`               |
|[Button](./Button.md)         | a button supporting text and an image         |
|[Color](./Color.md)           | Color-constants and support functions         |
|[Gap](./Gap.md)               | Base-class of `HGap` and `VGap`               |
|[HBox](./HBox.md)             | A panel layouting it's children horizontally  |
|[GridBox](./GridBox.md)       | A panel layouting it's children in a grid     |
|[HGap](./HGap.md)             | A horizontal gap                              |
|[Image](./Image.md)           | An image-widget supporting scaling            |
|[Label](./Label.md)           | A single-line text                            |
|[List](./List.md)             | A panel with list-items                       |
|[Line](./Line.md)             | A horizontal or vertical line                 |
|[Msg](./Msg.md)               | Logging support class                         |
|[Panel](./Panel.md)           | A rectangular area and with child widgets     |
|[ScrollArea](./ScrollArea.md) | A panel supporting scrolling                  |
|[Settings](./Settings.md)     | Configuration class for `App` and widgets     |
|[TabBox](./TabBox.md)         | A panel with tabs                             |
|[Text](./Text.md)             | A multi-line textbox                          |
|[VBox](./VBox.md)             | A panel layouting it's children vertically    |
|[VGap](./VGap.md)             | A vertical gap                                |
|[Widget](./Widget.md)         | The base class of all widgets                 |


The following classes are planned, but not implemented yet:

  - `GridBox`
  - `ScrollArea`
  - `TabBox`
