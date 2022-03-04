import bpy
import os
import ast
import json

from ..utility.constants import layout_scale_x, layout_scale_y
from ..utility.functions import json_favorites_path, convert_ab_path, json_check
from .ui_functions import draw_scripts

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       CollectionProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList,
                       Menu)

from ..utility.functions import get_prefs
from .ui_functions import get_folder_icon, get_icon

def draw_main_directory (pie,prefs):

    has_folders = False

    section_1 = pie.column(align=True)
    section_1 = section_1.box()
    section_1.label(text='Script Library',icon='FILE_FOLDER')

    ############# Generate Folders

    libray_menu = section_1.column(align=True)

    if os.path.exists(convert_ab_path(prefs.script_path)):

        for fn in os.listdir(prefs.script_path): # Get Folders First

            if os.path.isdir(os.path.join(prefs.script_path,fn)):

                has_folders = True

                libray_menu.scale_y = prefs.layout_scale_y
                libray_menu.scale_x = prefs.layout_scale_x

                folder_icon = get_folder_icon(fn)

                action = libray_menu.operator("qs.openfolder", text=fn,icon=folder_icon)
                action.folder_name = fn
                action.folder_path = os.path.join(prefs.script_path,fn)
        
        ############# Generate Scripts

        if has_folders:

            libray_menu = section_1.column(align=True)
                
        draw_scripts(prefs,prefs.script_path,libray_menu)
    
    else:
        box = libray_menu.box()
        box.label(text='Library Path Not Found')


def draw_favorites_section(pie,prefs):

    section_2 = pie.column(align=True)
    section_2 = section_2.box()

    section_2.scale_y = prefs.layout_scale_y
    section_2.scale_x = prefs.layout_scale_x

    section_2.label(text='Favorites', icon='SOLO_ON')

    libray_menu = section_2.column(align=True)

    empty_favorites = False

    commands = {}  

    if os.path.exists(json_favorites_path()) and json_check(json_favorites_path()): 
        
        with open(json_favorites_path(), encoding='utf8') as json_file:
            data = json.load(json_file)  
            if not data['Favorites']:
                empty_favorites = True
            else:
                for i in data['Favorites']:  

                    #if os.path.exists(convert_ab_path(data['Favorites'][i])):

                    (script_base_name,ext) = os.path.splitext(i)

                    row = libray_menu.row(align=True)

                    script_icon = get_icon(script_base_name, folder_name = os.path.basename(os.path.dirname(data['Favorites'][i])))

                    action = row.operator("qs.runscript", text=script_base_name,icon=script_icon)

                    action.full_dict = True
                    action.script_directory = data['Favorites'][i]
                    action.script_name = i
                    
                    row = row.row(align=True)
                    
                    remove_favorite = row.operator("qs.removefavoritescript", text='',icon='X').script_name = i

                    open_editor = row.operator("qs.openscriptineditor",text='',icon='TEXT')
                    open_editor.script_path = data['Favorites'][i]
    else:
        empty_favorites = True

    if empty_favorites:
        box_section_2 = section_2.box()
        box_section_2.label(text='No Favorites Added',icon='INFO')

def draw_pie(pie,prefs,invert=False):

    if invert:
        draw_main_directory(pie,prefs)
        draw_favorites_section(pie,prefs)
    else:
        draw_favorites_section(pie,prefs)
        draw_main_directory(pie,prefs)
       
class BQF_PT_Pie_QuickFavoritesMain(bpy.types.Menu):

    bl_idname = 'qs.piequickfavorites'
    bl_label = "Quick Scripts"

    def draw(self, context):

        prefs = get_prefs()

        layout = self.layout
        pie = layout.menu_pie()

        # -------------------------------------------------------------------------------------------------------------------
        # Draw Pie Menu
        # -------------------------------------------------------------------------------------------------------------------

        draw_pie(pie,prefs,prefs.invert_pie_layout)


        


            




 