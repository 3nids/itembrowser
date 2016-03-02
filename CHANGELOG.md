##  Changelog

#### Version 2.5 04.02.2015

* Allow transparency for rubber band

#### Version 2.4 04.02.2015

* Use display expression in the combo box
* Small UI improvements
* New Makefile

#### Version 2.3 16.07.2013

* New set of SVG icons

#### Version 2.2 11.07.2013

* Add option to specify dock area

##### Version 2.1.1 27.06.2013

* Reload session after project load instance of layer changed (fix missing actions)
* Fix: disconnect properly the layer

#### Version 2.1 25.06.2013

* Layer actions can be run for current feature from the dock

##### Version 2.0.1 21.06.2013

* Fix help link

### Version 2.0 20.06.2013

* New workflow: an icon is enabled as soon as the current layer has a multiple selection. Clicking this icon shows the dock to browse the selection.
* Updated to new API

#### Version 1.9 18.02.2013

*  bugfix: at launch, if a previously saved feature has been deleted

#### Version 1.8 11.02.2013

* Updated for new vector API

#### Version 1.7 01.02.2013

* Added layer to map coordinates transformation [issue #1](https://github.com/3nids/itembrowser/issues/1)

#### Version 1.6 10.04.2012

* pan and/or zoom option
* added help link to wiki in the menu

#### Version 1.5 07.03.2012

* created new wiki

#### Version 1.4 01.03.2012

* Fix: empty selection was badly saved to project and led to crash at project startup
* created new wiki

#### Version 1.3 29.02.2012

* Put first item in rubber band
* At first connection, if the layer already has some items selected, the browser is started
* Connect and disconnect properly the layer
* the dock is now entitled: "ItemBrowser: layer name"
* updated metadata to handle the plugin in github and not in qgis hub anymore
* it's not very often, you can release on feb. 29th ;)

#### Version 1.2 20.02.2012

* handles the map extent while browsing points

#### Version 1.1 14.02.2012

* current selection can now be saved in project
* the list of layers is generated from the legend and not from the canvas (i.e. even undisplayed layers can be connected)

#### Version 1.0.2 24.01.2012

* hide widget if no item is selected
* do not put in rubber band if only one item is selected

#### Version 1.0.1 20.01.2012

* signal is now emitted by the layer, corrected slot
* completed metadata
