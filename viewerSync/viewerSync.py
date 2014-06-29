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
# GLOBALS
# =============================================================================

KNOB_TITLES = {
    'channels': 'channels',
    'cliptest': 'zebra-stripe',
    'downrez': 'proxy settings',
    'format_center': 'format center',
    'gain': 'gain',
    'gamma': 'gamma',
    'masking_mode': 'masking mode',
    'masking_ratio': 'masking ratio',
    'overscan': 'overscan',
    'ignore_pixel_aspect': 'ignore pixel aspect ratio',
    'input_number': 'viewed input',
    'input_process': 'input process on/off',
    'input_process_node': 'input process node',
    'inputs': 'input nodes',
    'rgb_only': 'LUT applies to rgb channels only',
    'roi': 'roi',
    'safe_zone': 'safe zone',
    'show_overscan': 'show overscan',
    'viewerInputOrder': 'input process order',
    'viewerProcess': 'LUT',
    'zoom_lock': 'zoom lock'
}

KNOB_TOOLTIPS = {
    'channels': 'Sync the layers and alpha channel to display in the viewers. '
                'The "display style" is not synced.',
    'cliptest': 'Sync if zebra-striping is enabled or not between viewers.',
    'downrez': 'Sync the scale down factor for proxy mode. Proxy mode '
               'activation is always synced.',
    'format_center': 'Sync if a crosshair is displayed at the center of the '
                     'viewer window.',
    'gain': 'Sync the gain slider between viewers.',
    'gamma': 'Sync the gamma slider between viewers.',
    'masking_mode': 'Sync the mask style between viewers.',
    'masking_ratio': 'Sync the mask ratio selection between viewers.',
    'overscan': 'Sync the amount of overscan displayed between viewers.',
    'ignore_pixel_aspect': 'If selected all viewers will either show square '
                           'pixels or the pixel aspect ratio denoted by '
                           'the format.',
    'input_number': 'Syncs which input number is being viewed between all '
                    'viewers. This does not mean that all viewers are '
                    'viewing the same nodes, just that all viewers are '
                    'viewing input 1, etc.',
    'input_process': 'If selected all viewers will either have the input '
                     'process on, or off.',
    'input_process_node': 'Syncs what node is used as the input process '
                          'between all viewers.',
    'inputs': 'If selected, all viewers will point to the same nodes in the '
              'node graph.',
    'rgb_only': 'Syncs the "apply LUT to color channels only" knob, which '
                'indicates that the viewer will attempt to apply the lut to '
                'only the color channels. This only works with knobs that '
                'have an "rgb_only" knob, which is few.',
    'roi': 'Syncs the ROI window between all viewers. ROI needs to be manually '
           'activated for all viewers.',
    'safe_zone': 'Syncs the safe zone overlays between all viewers.',
    'show_overscan': 'If selected, all viewers will either show overscan or '
                     'not show overscan.',
    'viewerInputOrder': 'Syncs if the input process occurs before or after '
                        'the viewer process between all viewers.',
    'viewerProcess': 'Syncs the LUT between all viewers.',
    'zoom_lock': 'If selected, the zoom lock will apply to all viewers or '
                 'none.'
}

SYNC_DEFAULTS = {
    'channels': False,
    'cliptest': True,
    'downrez': True,
    'format_center': True,
    'gain': False,
    'gamma': False,
    'masking_mode': True,
    'masking_ratio': True,
    'overscan': True,
    'ignore_pixel_aspect': True,
    'input_number': True,
    'input_process': True,
    'input_process_node': True,
    'inputs': False,
    'rgb_only': True,
    'roi': True,
    'safe_zone': True,
    'show_overscan': True,
    'viewerInputOrder': True,
    'viewerProcess': True,
    'zoom_lock': True
}

VIEWER_SYNC_KNOBS = [
    'vs_{knob}'.format(knob=sync_knob) for sync_knob in SYNC_DEFAULTS.keys()
]

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    'remove_callbacks',
    'setup_sync',
    'sync_viewers',
]

# =============================================================================
# PRIVATE FUNCTIONS
# =============================================================================


def _add_sync_knobs(viewer):
    """Adds the sync option knobs to the given given viewer node."""
    if 'vs_options' in viewer.knobs():
        # This node already has a settings pane.
        return

    tab = nuke.Tab_Knob('vs_options', 'Viewer Sync')
    viewer.addKnob(tab)

    def add_knobs(knob_list):
        """For every knob in the list, adds that knob to the current tab"""
        for knob in knob_list:
            new_knob = nuke.Boolean_Knob('vs_' + knob, KNOB_TITLES[knob])
            new_knob.setTooltip(KNOB_TOOLTIPS[knob])
            new_knob.setValue(SYNC_DEFAULTS[knob])
            new_knob.setFlag(nuke.STARTLINE)
            viewer.addKnob(new_knob)

    input_options = nuke.Text_Knob('vs_input_options', 'Input Options')
    viewer.addKnob(input_options)
    add_knobs(['inputs', 'input_number', 'channels'])

    display_options = nuke.Text_Knob('vs_display_options', 'Display Options')
    viewer.addKnob(display_options)
    add_knobs(
        [
            'viewerProcess', 'rgb_only', 'input_process',
            'input_process_node', 'viewerInputOrder', 'gain', 'gamma',
            'ignore_pixel_aspect', 'zoom_lock', 'show_overscan',
            'overscan'
        ]
    )

    overlay_options = nuke.Text_Knob('vs_overlay_options', 'Overlay Options')
    viewer.addKnob(overlay_options)
    add_knobs(
        [
            'masking_mode', 'masking_ratio', 'safe_zone',
            'format_center', 'cliptest'
        ]
    )

    process_options = nuke.Text_Knob('vs_process_options', 'Processing Options')
    viewer.addKnob(process_options)
    add_knobs(['downrez', 'roi'])

# =============================================================================


def _extract_viewer_list(viewer):
    """Extracts a list of Viewer nodes from a callback.

    Searches a viewer node for a viewerSync callback, and extracts the
    value of the `viewers` arg.

    Args:
        viewer : (<nuke.nodes.Viewer>)
            The viewer node with the callback attached.

    Returns:
        [<nuke.nodes.Viewer>]
            A list of viewer nodes that were listed in the callback arg.

    Raises:
        ValueError
            If the callback found on the viewer is present, but not for
            viewerSync.

    """
    callback = viewer['knobChanged'].value()

    if not callback:
        return []
    elif 'viewerSync' not in callback:
        raise ValueError("Not a viewerSync'd viewer.")

    callback = callback.replace('viewerSync.sync_viewers(', '')[:-1]
    linked_viewers = literal_eval(callback)
    viewer_nodes = [
        nuke.toNode(node) for node in linked_viewers if nuke.toNode(node)
    ]

    return viewer_nodes

# =============================================================================


def _remove_knobs(viewer):
    """Removes all viewerSync knobs from a viewer"""
    for knob in viewer.knobs():
        if knob.startswith('vs_'):
            viewer.removeKnob(viewer[knob])
    # It's unlikely that the tab knob was deleted at first.
    if 'vs_options' in viewer.knobs():
        viewer.removeKnob(viewer['vs_options'])

# =============================================================================


def _sync_knob(source, targets, knob):
    """Syncs a knob setting from the source to the target"""
    for target in targets:
        target[knob].setValue(source[knob].value())

# =============================================================================


def _set_callback(node, viewers):
    """Sets the callback on the node with the viewers and knobs args"""
    viewers = list(viewers)  # Create a copy of list, as we're poppin'
    # Remove our caller from the nodes to update if present.
    if node in viewers:
        viewers.pop(viewers.index(node))

    # Get the list of node names to populate the arg with
    viewer_names = [viewer.fullName() for viewer in viewers]

    node['knobChanged'].setValue(
        'viewerSync.sync_viewers({viewers})'.format(
            viewers=viewer_names
        )
    )

# =============================================================================
# PUBLIC FUNCTIONS
# =============================================================================


def remove_callbacks():
    """Removes callback from all selected viewers and all viewers linked."""
    viewers = nuke.selectedNodes('Viewer')

    if not viewers:
        viewers = nuke.allNodes('Viewer')
    else:
        extra_viewers = []  # Viewers that weren't in the selected group.
        for viewer in viewers:
            try:
                linked_viewers = _extract_viewer_list(viewer)
            except ValueError:
                pass
            else:
                extra_viewers.extend(linked_viewers)

        viewers.extend(extra_viewers)

    for viewer in viewers:
        if 'viewerSync' in viewer['knobChanged'].value():
            viewer['knobChanged'].setValue('')
        _remove_knobs(viewer)

# =============================================================================


def setup_sync():
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
            # If this node was already setup as a sync, we'll remove the
            # sync settings knobs.
            _remove_knobs(viewer)
            # In case Nuke returns us viewers split across different levels,
            # we'll need to split them up by level so that we don't
            # attempt to link those.
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

    bad_viewers = []  # List of viewers that have foreign callbacks

    for viewers in viewer_levels.values():
        for viewer in viewers:
            try:
                linked_viewers = _extract_viewer_list(viewer)
            except ValueError:
                bad_viewers.append(viewer)
            else:
                remove_viewers.extend(linked_viewers)

    if remove_viewers:
        for viewer in set(remove_viewers):
            viewer['knobChanged'].setValue('')
            _remove_knobs(viewer)

    for viewers in viewer_levels.values():
        for viewer in bad_viewers:
            if viewer in viewers:
                viewers.remove(viewer)
        for viewer in viewers:
            _add_sync_knobs(viewer)
            _set_callback(viewer, viewers)

# =============================================================================


def sync_viewers(viewers):

    caller = nuke.thisNode()
    caller_knob = nuke.thisKnob().name()

    # We need to check what knob is calling us first- if that knob isn't a
    # syncing knob, we'll return.
    if caller_knob not in ['inputChange', 'knobChanged']:
        if caller_knob not in SYNC_DEFAULTS.keys() + VIEWER_SYNC_KNOBS:
            return

        if caller_knob not in VIEWER_SYNC_KNOBS:
            if not caller['vs_{knob}'.format(knob=caller_knob)].value():
                # Sync setting is false for this knob
                return

    # Grab our viewer nodes and remove any that have been deleted.
    viewer_nodes = [
        nuke.toNode(viewer) for viewer in viewers if nuke.toNode(viewer)
    ]

    if caller_knob in VIEWER_SYNC_KNOBS:
        # Sync setting and continue
        _sync_knob(caller, viewer_nodes, caller_knob)
        if caller[caller_knob].value():
            caller_knob = caller_knob.replace('vs_', '')

    if caller_knob in ['inputChange', 'inputs']:
        if caller['vs_inputs'].value():
            for viewer in viewer_nodes:
                for i in xrange(caller.inputs()):
                    viewer.setInput(i, caller.input(i))
        return
    elif caller_knob == 'knobChanged':
        knob_list = [
            knob for knob in SYNC_DEFAULTS.keys() if SYNC_DEFAULTS[knob]
        ]
    else:
        knob_list = [caller_knob]

    # Update remaining viewers to point at our current node.
    for knob in knob_list:
        _sync_knob(caller, viewer_nodes, knob)
