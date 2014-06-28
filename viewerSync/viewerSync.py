#!/usr/bin/env python
"""

Viewer Sync
===========

Contains the functions required for two views to be kept in sync.

## Public Functions

    sync_viewers()
        Syncs the inputs of one or more viewers to match the input list
        of the calling node.

    toggle()
        Toggles the callback args of selected viewers or all viewers in root.

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

# Standard Imports
from ast import literal_eval

# Nuke Imports
try:
    import nuke
except ImportError:
    pass

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'sync_viewers',
    'toggle',
]

# =============================================================================
# PRIVATE FUNCTIONS
# =============================================================================


def sync_viewers(viewers):

    sync_knobs = [
        'channels',
        'cliptest',
        'downrez',  # Proxy Mode
        'fps',
        'gain',
        'gamma',
        'input_number',  # What input we're looking at
        'input_process',
        'input_process_node',
        'masking_mode',
        'masking_ratio',
        'rgb_only',
        'roi',  # Doesn't work 100% yet.
        'safe_zone',
        'viewerProcess'
    ]

    caller = nuke.thisNode()

    # Grab our viewer nodes and remove any that have been deleted.
    viewer_nodes = [
        nuke.toNode(viewer) for viewer in viewers if nuke.toNode(viewer)
    ]
    if not viewer_nodes:
        # All linked viewers have been deleted.
        # We should remove the callback.
        caller['knobChanged'].setValue('')
        return

    # Remove our active viewer from the nodes to update.
    if caller in viewer_nodes:
        viewer_nodes.pop(viewer_nodes.index(caller))

    # Update remaining viewers to point at our current node.
    for viewer in viewer_nodes:
        #viewer.setInput(0, current_node)
        #viewer.setInput(active_view_input, current_node)
        for i in xrange(caller.inputs()):
            viewer.setInput(i, caller.input(i))
        for knob in sync_knobs:
            viewer[knob].setValue(caller[knob].value())

# =============================================================================


def toggle():
    # Grab all of our currently selected Viewer nodes:
    viewers = nuke.selectedNodes('Viewer')

    # We'll be using the viewer_levels dictionary to link viewers
    # across the same DAG level, and avoid linking lone viewers on sub DAGs.
    viewer_levels = {}

    # If we find ANY viewers of the currently selected set having a
    # knobChanged value, we'll turn off syncing on all the node's it's linked
    # to. Safer that way.
    remove_viewers = []

    if viewers:
        for viewer in viewers:
            group = '.'.join(viewer.fullName().split('.')[:-1])
            if not group:
                group = 'root'
            group_viewers = viewer_levels.get(group, [])
            group_viewers.append(viewer)
            viewer_levels[group] = group_viewers
    else:
        # No viewers were provided, so we'll just grab all the viewers
        # at our current level
        viewers = nuke.allNodes('Viewer')
        viewer_levels['group'] = viewers

    for level in viewer_levels.keys():
        if len(viewer_levels[level]) <= 1:
            # Nothing to sync, delete this level.
            del viewer_levels[level]

    for viewers in viewer_levels.values():
        for viewer in viewers:
            callback = viewer['knobChanged'].value()
            if callback:
                callback = callback.replace('viewerSync.sync_viewers(', '')[:-1]
                linked_viewers = literal_eval(callback)
                linked_viewers = [
                    nuke.toNode(name) for name in linked_viewers
                    if nuke.toNode(name)
                ]
                remove_viewers.extend(linked_viewers)

    if remove_viewers:
        for viewer_name in set(remove_viewers):
            viewer = nuke.toNode(viewer_name)
            viewer['knobChanged'].setValue('')

    for viewers in viewer_levels.values():
        for viewer in viewers:
            # We need a list of viewer names to link this node with.
            viewer_names = [node.fullName() for node in viewers]
            viewer['knobChanged'].setValue(
                'viewerSync.sync_viewers({viewers})'.format(
                    viewers=viewer_names
                )
            )
