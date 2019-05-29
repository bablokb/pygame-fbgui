List
====

The class implements a widget displaying a list of objects (list-items).

Hierarchy
---------

  - [Widget](./Widget.md)
    - [Panel](./Panel.md)
      - [Box](./Box.md)
        - [VBox](./VBox.md)
          - List



Settings
--------

| Name          | Description                 | Default                   |
|---------------|-----------------------------|---------------------------|
| multiselect   | support multiple selections | False                     |



Public Methods
--------------

| Name                          | Description                                 |
|-------------------------------|---------------------------------------------|
| add_items(items,refresh=True) | add the items to the list and refresh GUI   |
| clear(refresh=True)           | clear all items and refresh GUI             |
| get_selected()                | return widget or list of widgets            |


Events
------

The list class currently supports the following additional event-methods:

| Name                         | Description                                    |
|------------------------------|------------------------------------------------|
| on_selection_changed(widget) | passes selected widget(s) or None.             |

To receive this event, add a `on_selection_changed`-method to your list
instance. If `multiselect` is `True`, then the method receives a (possibly empty
list of selected widgets. Otherwise, the method receives the selected
widget or None if no item was selected.
