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

    nuke.tprint(nuke.thisKnob().name())

    # Grab our active viewer's node & input.
    active_view_node = nuke.activeViewer().node()
    active_view_input = nuke.activeViewer().activeInput()
    current_node = active_view_node.input(active_view_input)

    # Grab our viewer nodes
    viewer_nodes = [nuke.toNode(viewer) for viewer in viewers]

    # Remove our active viewer from the nodes to update.
    if active_view_node in viewer_nodes:
        viewer_nodes.pop(active_view_node)

    # Update remaining viewers to point at our current node.
    for viewer in viewer_nodes:
        viewer.setInput(0, current_node)
        viewer.setInput(active_view_input, current_node)

# =============================================================================


def toggle():
    # Grab all of our currently selected Viewer nodes:
    viewers = nuke.selectedNodes('Viewer')

    # We'll be using the viewer_levels dictionary to link viewers
    # across the same DAG level, and avoid linking lone viewers on sub DAGs.
    viewer_levels = {}

    # If we find ANY viewers of the currently selected set having a
    # knobChanged value, we'll turn them all off. Safer this way.
    remove = False

    if viewers:
        for viewer in viewers:
            group = '.'.join(viewer.fullname().split('.')[:-1])
            group_viewers = viewer_levels.get(group, [])
            group_viewers.append(viewer)
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
            if viewer['knobChanged'].value():
                remove = True

    for viewers in viewer_levels.values():
        for viewer in viewers:
            if remove:
                viewer['knobChanged'].setValue('')
            else:
                # We need a list of viewer names to link this node with.
                viewer_names = [node.fullName() for node in viewers]
                viewer['knobChanged'].setValue(
                    'viewerSync.sync_viewers({viewers})'.format(
                        viewers=viewer_names
                    )
                )
