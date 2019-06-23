Panel
=====

The base class of all panels. Draws a rectangular area on the screen.
A panel can have children. The children can be positioned relative
to the border of the panel.

Hierarchy
---------

  - [Widget](./Widget.md)
    - Panel


Settings
--------

| Name          | Description                 | Default                 |
|---------------|-----------------------------|-------------------------|
| margins       | (left,right,top,bottom)     | (0,0,0,0)               |
| radius        | radius of corners (0<=r<=1) | 0.0                     |



Public Methods
--------------

| Name                         | Description                           |
|------------------------------|---------------------------------------|
| add(widget,index=None)       | add a child-widget                    |
| remove(widget,refresh=False) | remove a child-widget                 |
| remove_all(refresh=False)    | remove all child-widgets              |
| set_offset(offset)           | set the offset to the given value     |
| inc_offset(inc=1)            | increment the offset                  |
| dec_offset(dec=1)            | decrement the offset                  |
