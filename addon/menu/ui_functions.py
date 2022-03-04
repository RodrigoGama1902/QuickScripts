import bpy
import os

from ..utility.constants import favorites_path, layout_scale_x, layout_scale_y
from ..utility.functions import get_prefs

def get_icon(script_base_name,folder_name = ''):

    prefs = get_prefs()

    if not prefs.detect_icons:
        return 'FILE_SCRIPT'

    if prefs.detect_icons_scripts:

        icons = {
            ('array',):'MOD_ARRAY',
            ('bevel',):'MOD_BEVEL',
            ('solidify',):'MOD_SOLIDIFY',     
            ('subdivision',):'MOD_SUBSURF', 
            ('mirror',):'MOD_MIRROR',    
            ('smooth',):'MOD_SMOOTH', 
            ('decimate',):'MOD_DECIM',  
            ('boolean',):'MOD_BOOLEAN',
            ('wireframe',):'MOD_WIREFRAME',               
            }

        for i in icons:
            for tag in i:
                if tag in script_base_name.lower():
                    return icons[i]

    if prefs.detect_icons_folder:
    
        if folder_name:

            folder_icon = get_folder_icon(folder_name)

            if folder_icon != 'FILE_FOLDER':

                return folder_icon

    return 'FILE_SCRIPT'

def get_folder_icon(fn):

    prefs = get_prefs()

    if not prefs.detect_icons:
        return 'FILE_FOLDER'
    
    if prefs.detect_icons_folder:

        icons = {
                ('modifiers',):'MODIFIER',
                ('materials',):'NODE_MATERIAL',
                ('objects',):'OBJECT_DATAMODE',     
                ('edit mode','edit_mode','edit','edit-mode'):'EDITMODE_HLT', 
                ('camera',):'CAMERA_DATA',  
                ('scene',):'SCENE_DATA', 
                ('nodes','node-tree','node setup','node-setup'):'NODETREE', 
                ('pipeline','workflow'):'WORKSPACE', 
                ('select',):'RESTRICT_SELECT_OFF',                  
                }

        for i in icons:
            for tag in i:
                if tag in fn.lower():
                    return icons[i]

    return 'FILE_FOLDER'

def draw_scripts(prefs,path,layout,window = 1):

    for fn in os.listdir(path): 

        if fn.endswith(".py"):

            (script_base_name,ext) = os.path.splitext(os.path.join(path,fn))
            script_base_name = os.path.basename(script_base_name)

            row = layout.row(align=True)

            if window == 1:
                row.scale_x = prefs.layout_scale_x
                row.scale_y = prefs.layout_scale_y

            script_icon = get_icon(script_base_name,folder_name = path)

            action = row.operator("qs.runscript", text= script_base_name ,icon=script_icon)
            action.script_directory = os.path.join(path,fn)
            action.script_name = script_base_name

            row = row.row(align=True)
        
            favorite = row.operator("qs.favoritescript", text='',icon='SOLO_OFF')
            favorite.script_name = fn
            favorite.script_path = os.path.join(path,fn)

            open_editor = row.operator("qs.openscriptineditor",text='',icon='TEXT')
            open_editor.script_path = os.path.join(path,fn)
