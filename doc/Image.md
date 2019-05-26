Image
=====

A widget for the display of images. See `demo/images.py` for an example.


Hierarchy
---------

  - [Widget](./Widget.md)
    - Image


Settings
--------


| Name          | Description            | Default                         |
|---------------|------------------------|---------------------------------|
| scale         | scale image to size    | False                           |
| min_size      | minimum size if scaled | native size                     |


Be careful when adding a scalable image to a dynamically sized HBox/VBox.
This does not work, since a scalable image can have an arbitrary large
size.


Public Methods
--------------

| Name          | Description                                          |
|---------------|------------------------------------------------------|
| set_image     | Set the image of this widget                         |
