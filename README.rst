Viewer Sync
===========

- **Author:** Philippe Huberdeau
- **Maintainer:** Sean Wallitsch
- **Email:** sean@grenadehop.com
- **License:** MIT
- **Status:** Development
- **Python Versions:** 2.6-2.7
- **Nuke Versions:** 6.3 and up

Synchronizes two or more viewers in Nuke so that they always show the same node.

Usage
-----

Synchronizing viewers in nuke is as easy as hitting `Shift+j` with two or more
viewers selected. If no viewers are selected, all viewers on the root node
graph level are synchronized.

From that point on, certain designated settings are synced between those
viewers whenever you change one of those settings on either one. Those settings
are selectable from a new 'Viewer Sync' tab in the Viewer settings. You can
choose to sync channels, inputs, viewed input number, luts, input processes,
color corrections, overlays, ROI, and more.

To remove the synchronization from nodes, select the nodes you wish to remove
synchronization from, and select 'Remove Viewer Sync'. If no nodes are
selected, all the viewers found on the root node graph level are de-synced.
Note that any viewers that are in the same group

Installation
------------

To install, simply ensure the 'viewerSync' directory is in your .nuke
directory or anywhere else within the Nuke python path.

Then, add the following lines to your 'menu.py' file:
::
    import viewerSync
    viewerSync.run()

Hotkey can be set with the `hotkey` argument, which defaults to `Shift+j`.

Changelog
---------

*New in version 2.0*

- Refactoring
- Now sync more than 2 viewers together- sync as many viewers as you want.
- Adds two menu options to the 'Viewer' menu:
    - 'Create Viewer Sync' (hotkey: `Shift-j`)
    - 'Remove Viewer Sync' (no hotkey)
- Sync viewers by selecting them and then hitting `Shift-j`.
- Hitting `Shift-j` with no selection causes all viewers on the same DAG level to sync.
- Adds way more sync possibilities:
    - Sync channels
    - Sync inputs
    - Sync viewed input
    - Sync LUT
    - Sync input processes
    - Sync gain & gamma
    - Sync overlays
    - Sync ROI
    - Many more
- Choose between those possibilities from a new 'Viewer Sync' tab in the normal Viewer settings panel.
- Many bugs squashed.

License
-------

The MIT License (MIT)

    viewerSync
    Copyright (c) 2011-2014 Philippe Huberdeau and Sean Wallitsch

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
