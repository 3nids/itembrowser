**Item Browser** is a [QGIS](http:://www.qgis.org) plugin to browse a multiple selection.

## Howto

Set a layer with a multiple selection as the current layer, and the
![plugin](https://raw.github.com/3nids/itembrowser/blob/master/icons/itembrowser.png) icon is now enabled.

 Click on this icon, and a dock will appear on the bottom left of the application.
You can now navigate within the selection. The plugin can auto pan and scale to the current feature.

The edit form can be opened by clicking the ![form](https://raw.github.com/3nids/itembrowser/blob/master/icons/openform.png) icon.

In the settings, can be defined:
* color and width of the rubber band
* scaling of the bounding box of the current item can be defined
* save of the current selection and current item for all currently browsed layers

If save of current selection is enabled, at project launch, the last selection is restored, and the last current item is reset in the dock.

A demo video is available on [youtube](http://www.youtube.com/watch?v=VU7YVz_zHUI&hd=1).

## Python developpers

If you want something to happen with the selection, the connected layer emits two signals as soon as the selection changed:

* _browserCurrentItem(long)_ if there is a selection, the given integer being the feature id.
* _browserNoItem()_ if there is nothing selected.


