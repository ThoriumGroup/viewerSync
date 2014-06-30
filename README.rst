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

From that point on, whenever you switch an input on one viewer, the other
viewers will switch to the same input.

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
- Now only one menu command, activated with `Shift-j`
- Now sync more than 2 viewers together- sync as many viewers as you want.
- Sync viewers by selecting them and then hitting `Shift-j`.
- Hitting `Shift-j` with no selection causes all viewers on the same DAG level to sync.

License
-------

The MIT License (MIT)

    viewerSync
    Copyright (c) 2011-2012 Philippe Huberdeau

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
