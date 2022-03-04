import bpy
import os
import json
import traceback
import copy

from ..utility.functions import get_prefs, json_favorites_path, convert_ab_path, json_check
from ..utility.constants import operator_text_detect
from ..menu.ui_functions import draw_scripts, get_folder_icon, get_icon

def change_area_running_method(text_data):

    default_area = copy.copy(bpy.context.area.type)

    try:
        bpy.context.area.type = 'TEXT_EDITOR'
        bpy.context.area.spaces.active.text = text_data
        bpy.ops.text.run_script()
        bpy.context.area.type = default_area

        return True
    except:

        bpy.context.area.type = default_area
        return False

def run_script(script_name, script_directory):
    
    #prefs = get_prefs()

    print()
    print('Running: ' + script_name)
    print()

    # In this method, a temporary script text is generated, in this way, the addon can check each line to find any modal test call to run
    
    temp_script_name = 'temp_running_script'

    if bpy.data.texts.get(temp_script_name):
        bpy.data.texts.remove(bpy.data.texts.get(temp_script_name))

    temp_text = bpy.data.texts.new(temp_script_name)

    execute = ''
    teste_call = False
    with open(script_directory) as fp:
        for line in fp:
            for i in operator_text_detect:
                if i in line:
                    teste_call = True
                    continue

            if teste_call == True:
                if 'bpy.ops' in line:
                    execute += line                   
                continue

            temp_text.write(line)

    # Running 

    try:
        exec(compile(temp_text.as_string(),script_name,'exec'),None,globals())     
        
        if teste_call:
            if execute:  
                print(execute.strip())   
                exec(execute.strip())
                return True

    except Exception:
                
        print()
        print('---------------------------------------- Script Error ----------------------------------------')
        print()
        print(f'FILE: {script_name}')
        print()
        print('ERROR:')
        print()

        traceback.print_exc()

        return False

    '''
    
    if teste_call:
                    
        change_area_running_method(temp_text)

        if execute:  
            print(execute.strip())   
            exec(execute.strip())
            return True
    
    else:  

        filename = script_directory

        try:
            exec(compile(temp_text.as_string(),script_name,'exec'))           
        except Exception:
                    
            print()
            print('---------------------------------------- Script Error ----------------------------------------')
            print()
            print(f'FILE: {script_name}')
            print()
            print('ERROR:')
            print()

            traceback.print_exc()
            
            if prefs.try_other_method:
                
                print('---------------------------------------------------')
                print('')
                print('Main Method Failed, Running Second Method')
                print('')

                if not change_area_running_method(temp_text):

                    print('Second Method Failed')

                    return False

                print('Second Method Finished: Done')

                return True

            else:
                return False
    '''   

    return True

class QS_OT_RunScripts(bpy.types.Operator):
    """Run Selected Script"""

    bl_idname = "qs.runscript"
    bl_label = "Run Scripts"
    bl_options = {'REGISTER', 'UNDO'}

    script_name : bpy.props.StringProperty()
    script_directory : bpy.props.StringProperty()
    full_dict : bpy.props.BoolProperty(default=False)
    
    def execute(self, context):

        if not os.path.exists(convert_ab_path(self.script_directory)):           
            self.report({'ERROR'},
                            "Script Path Not Found")
            return {'CANCELLED'}

        props = bpy.context.scene.quick_scripts

        props.last_script_name = self.script_name
        props.last_script_dir = self.script_directory
                          
        if run_script(self.script_name, self.script_directory):
            return {'FINISHED'}
        else:
            self.report({'ERROR'},
                            "Script Error. Check the console for more datails")
            return {'CANCELLED'}
                            
class QS_OT_QuickExcScript(bpy.types.Operator):
    """ShortCut Run Selected Script"""

    bl_idname = "qs.quickrunscript"
    bl_label = "ShortCut Run Script"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        props = bpy.context.scene.quick_scripts

        script_name = props.last_script_name 
        script_directory = props.last_script_dir
        
        if not script_name or not script_directory:
            self.report({'ERROR'},
                            "No Recent Script Found")
            return {'CANCELLED'}

        if not os.path.exists(convert_ab_path(script_directory)):
            self.report({'ERROR'},
                            "Script Path Not Found")
            return {'CANCELLED'}
       
        if run_script(script_name, script_directory):
            return {'FINISHED'}
        else:
            self.report({'ERROR'},
                            "Script Error. Check the console for more datails")
            return {'CANCELLED'}

class QS_OT_OpenFolder(bpy.types.Operator):
    """Open selected folder"""

    bl_idname = "qs.openfolder"
    bl_label = "Open Folder"
    bl_options = {'REGISTER', 'UNDO'}

    folder_name : bpy.props.StringProperty()
    folder_path : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        print(self.folder_name)

        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self)

    def draw(self, context):

        #### Check if has folders

        prefs = get_prefs()

        has_folders = False

        for fn in os.listdir(self.folder_path):
            if os.path.isdir(os.path.join(self.folder_path,fn)):
                has_folders = True

        layout = self.layout

        row = layout.row()
        row.label(text=self.folder_name)

        col = layout.column(align=True)

        for fn in os.listdir(self.folder_path):

            if os.path.isdir(os.path.join(self.folder_path,fn)):

                has_folders = True

                row = col.row(align=True)

                row.scale_x = prefs.layout_scale_x
                row.scale_y = prefs.layout_scale_y

                folder_icon = get_folder_icon(fn)

                action = row.operator("qs.openfolder", text=fn,icon=folder_icon)
                action.folder_name = fn
                action.folder_path = os.path.join(self.folder_path,fn)

        if has_folders:  

            col = layout.column(align=True)

        ## Draw Scripts
        
        draw_scripts(prefs,self.folder_path,col)

class QS_OT_FavoriteScript(bpy.types.Operator):
    """Favorite selected script"""

    bl_idname = "qs.favoritescript"
    bl_label = "Favorite Selected"
    bl_options = {'REGISTER', 'UNDO'}

    script_name : bpy.props.StringProperty()
    script_path : bpy.props.StringProperty()
    
    def execute(self, context):
        
        data = {}
        data['Favorites'] = {self.script_name : self.script_path}

        if not os.path.exists(json_favorites_path()) or not json_check(json_favorites_path()):
            with open(json_favorites_path(), "w", encoding='utf8') as file: 
                json.dump(data, file, ensure_ascii=False)
                file.write("\n")
        else:
            with open(json_favorites_path()) as json_file:
                old_data = json.load(json_file)
                old_data['Favorites'][self.script_name] = self.script_path

            with open(json_favorites_path(), "w", encoding='utf8') as file:
                json.dump(old_data, file, ensure_ascii=False)
                file.write("\n")

        self.report({'INFO'},
                            "QS Script Favorited")
        return {'FINISHED'}

class QS_OT_RemoveFavoriteScript(bpy.types.Operator):
    """Remove script from favorites"""

    bl_idname = "qs.removefavoritescript"
    bl_label = "Remove from Favorites"
    bl_options = {'REGISTER', 'UNDO'}

    script_name : bpy.props.StringProperty()
    
    def execute(self, context):

        if os.path.exists(json_favorites_path()):

            with open(json_favorites_path()) as json_file:

                old_data = json.load(json_file)
                del old_data['Favorites'][self.script_name]

            with open(json_favorites_path(), "w", encoding='utf8') as file: # create a new empty blend file
                json.dump(old_data, file, ensure_ascii=False)
                file.write("\n")

        self.report({'INFO'},
                            "Script removed from favorites")
        return {'FINISHED'}
    
class QS_OT_OpenScriptInTextEditor(bpy.types.Operator):
    """Open selected script in a new text editor window"""

    bl_idname = "qs.openscriptineditor"
    bl_label = "Open in Text Editor"
    bl_options = {'REGISTER', 'UNDO'}

    script_path : bpy.props.StringProperty()
    
    def execute(self, context):

        if not os.path.exists(convert_ab_path(self.script_path)):
            self.report({'ERROR'},
                            "Script Path Not Found")
            return {'CANCELLED'}

        script_name = os.path.basename(self.script_path)

        if not bpy.data.texts.get(script_name):
            text = bpy.data.texts.load(self.script_path)
        else:
            text = bpy.data.texts.get(script_name)

        context = bpy.context.copy()

        for area in bpy.context.screen.areas:
            if area.type in ('IMAGE_EDITOR', 'VIEW_3D', 'NODE_EDITOR'):
                old_area = area.type        
                area.type = 'TEXT_EDITOR' 
                area.spaces.active.text = text 
                context['area'] = area     
                bpy.ops.screen.area_dupli(context, 'INVOKE_DEFAULT')
                area.type = old_area    
                break 
        
        self.report({'INFO'},
                            "Script opened in a new window")
        return {'FINISHED'}



        
        