#!/usr/bin/env python
"""

Viewer Sync
==========

Contains the functions required for two views to be kept in sync.

## Public Functions

## License

The MIT License (MIT)

iconPanel
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

"""

# =============================================================================
# IMPORTS
# =============================================================================

# Nuke Imports
try:
    import nuke
except ImportError:
    pass

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
]

# =============================================================================
# PRIVATE FUNCTIONS
# =============================================================================


def sync_viewers():
    try:
        active_view = nuke.activeViewer()
        active_view_node = active_view.node()
        active_view_input = active_view.activeInput()

        current_node = active_view_node.input(active_view_input)

        if active_view_node['name'].value() == 'Viewer1Sync':
            viewer_to_sync = nuke.toNode('Viewer1')
        else:
            viewer_to_sync = nuke.toNode('Viewer1Sync')

        viewer_to_sync.setInput(0, current_node)
        viewer_to_sync.setInput(active_view_input, current_node)
    except:  # TODO: Determine specific exceptions
        print 'No valid viewer.'

# =============================================================================


def add_callback():
    viewer1 = nuke.toNode('Viewer1')
    viewer1['knobChanged'].setValue('viewerSync.sync_viewers()')

    if not nuke.toNode('Viewer1Sync'):
        nuke.nodes.Viewer(name='Viewer1Sync')

    viewer2 = nuke.toNode('Viewer1Sync')
    viewer2['knobChanged'].setValue('viewer_sync.sync_viewers()')

# =============================================================================


def remove_callback():
    viewer1 = nuke.toNode('Viewer1')
    viewer1['knobChanged'].setValue('')

    if nuke.toNode('Viewer1Sync'):
        viewer2 = nuke.toNode('Viewer1Sync')
        viewer2['knobChanged'].setValue('')
