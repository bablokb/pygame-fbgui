VBox
====

The class implements a panel with a vertical layout of it's children
from left to right.

If the size of the VBox *is not* absolute or relative, it's height will be
calculated as the sum of the heights of the children (plus padding). It's
width will be the same as the largest width of the children.

If the size of the VBox *is* absolute or relative, and the size is
larger than the aggregated child-sizes, then the extra size will be
distributed across the children according to the `weight`-setting of
the children. Since this attribute defaults to zero, the extra size
will not be distributed automatically.


Hierarchy
---------

  - [Widget](./Widget.md)
    - [Panel](./Panel.md)
      - [Box](./Box.md)
        - VBox


Settings
--------

No additional settings.


Public Methods
--------------

Only inherited methods from base classes.
