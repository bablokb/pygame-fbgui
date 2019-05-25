Box
===

This is the base class of `HBox` and `VBox`. 

Don't use directly, this class only contains common settings and methods
for it's subclasses.

Hierarchy
---------

  - [Widget](./Widget.md)
    - [Panel](./Panel.md)
      - Box


Settings
--------

| Name          | Description           | Default                         |
|---------------|-----------------------|---------------------------------|
| padding       | (horizontal,vertical) | (0,0)                           |
| uniform       | (horizontal,vertical) | (False,False)                   |

`padding` is extra space in pixels between childs. Setting `uniform` to
`True` will make all children the same size.


Public Methods
--------------

Only inherited methods from base classes.
