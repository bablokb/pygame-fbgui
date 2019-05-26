Settings
========

Value-holder class for settings (configurations). You either pass a
dictionary to initialize values or you use simple assignments, e.g.

    setting1 = fbgui.Settings({'foo': 'bar'})

and

    setting2     = fbgui.Settings()
    setting2.foo = 'bar'

are (almost) equivalent. Also see the note regarding the `copy`-method below.


Hierarchy
---------

  - Settings


Settings
--------

No settings available.


Public Methods
--------------

| Name                    | Description                                          |
|-------------------------|------------------------------------------------------|
| Settings(defaults=None) | constructor with optional dictionary of settings     |
| copy(other)             | copy (subset) of settings from other object          |

If you pass a dictionary to the constructor, the (key,value) pairs will
initialize the settings of the object.

The `copy`-method behaves differently if the object was initialized with a
dictionary or not. If the former was the case, the `copy`-method only copies
the initial keys from the other-object. If no defaults were passed to the
contructor, the `copy`-method copies all keys from the other object.
