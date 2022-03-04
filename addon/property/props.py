import bpy

class QS_Props_QuickScript(bpy.types.PropertyGroup):  

    ############################ Main Path Property

    last_script_name : bpy.props.StringProperty(name= "Last Script Name", default = "")
    last_script_dir : bpy.props.StringProperty(name= "Last Script Directory", default = "")