import bpy

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       FloatProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)

from ..utility.constants import addon_name
from ..utility.functions import get_prefs

class QS_Prefs(bpy.types.AddonPreferences): 
    bl_idname = addon_name   
 
    script_path : StringProperty(
    
      name = "",
      default = "",
      description = "Select Your Script Library Folder",
      subtype = 'DIR_PATH'
      )

    detect_icons : BoolProperty(default=True, name= "Auto Detect Icons",description='Auto Detect Icons from file/folder names, check the documentation for more information')
    detect_icons_scripts : BoolProperty(default=False, name= "Detect Script Icons")
    detect_icons_folder : BoolProperty(default=True, name= "Detect Folder Icons")
    
    favorites_path : StringProperty(
    
      name = "",
      default = "",
      description = "Select a custom path for your favorite scripts data (JSON file)",
      subtype = 'DIR_PATH'
      )

    invert_pie_layout : BoolProperty(default=False, name= "Invert Pie Layout")

    layout_scale_x: FloatProperty(default = 1.1, min = 1, max= 2,name="Layout X Scale")
    layout_scale_y: FloatProperty(default = 1.3, min = 1, max= 3,name="Layout Y Scale")

    try_other_method: BoolProperty(default=True, name= "Try a different script running method if any error happens in the default method")
            
    def draw(self, context):

        prefs = get_prefs()
        layout = self.layout
    
        box = layout.box()
        box.label(text='Script Library directory:')
        box.prop(prefs, 'script_path')

        box = layout.box()
        box.label(text='Pie Menu Layout')
        box1 = box.box()
        box1.prop(prefs, 'detect_icons')

        if prefs.detect_icons:
          box_2 = box1.box()
          box_2.prop(prefs, 'detect_icons_folder')
          box_2.prop(prefs, 'detect_icons_scripts')
        
        box1 = box.box()
        box1.prop(prefs, 'invert_pie_layout')
        box2 = box.box()
        box2.label(text='Layout Scale')
        box2.prop(prefs, 'layout_scale_x')
        box2.prop(prefs, 'layout_scale_y')

        #box = layout.box()
        #box.label(text='Advanced')
        #box.prop(prefs,'try_other_method')
        #box1 = box.box()
        #box1.label(text='Custom Favorite Scripts Data (JSON File)')
        #box1.prop(prefs, 'favorites_path')


        


        


        
       