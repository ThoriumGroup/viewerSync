# -*- coding: utf-8 -*-
# philhub 2011   -   contact at philpma.AT.free.DOT.fr

import nuke

def viewerSync() :
    try :
        av = nuke.activeViewer()
        avn = av.node()
        avi = av.activeInput()
        curN = avn.input(avi)
        if avn['name'].value() == 'Viewer1Sync' :
            vSync = nuke.toNode('Viewer1')
        else :
            vSync = nuke.toNode('Viewer1Sync')
        vSync.setInput( 0, curN )
        vSync.setInput( avi, curN )
    except :
        print 'no valid viewer'
    
def viewerSyncCBs() :
    vSync = nuke.toNode('Viewer1')
    vSync['knobChanged'].setValue('viewerSync.viewerSync()')
    if not (nuke.toNode('Viewer1Sync')) :
        nuke.nodes.Viewer( name = 'Viewer1Sync' )
    vSync = nuke.toNode('Viewer1Sync')
    vSync['knobChanged'].setValue('viewerSync.viewerSync()')
    
def viewerSyncOFF() :
    vSync = nuke.toNode('Viewer1')
    vSync['knobChanged'].setValue('')
    if (nuke.toNode('Viewer1Sync')) :
        vSync = nuke.toNode('Viewer1Sync')
        vSync['knobChanged'].setValue('')