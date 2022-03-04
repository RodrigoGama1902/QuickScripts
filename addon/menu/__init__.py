import bpy

from .main_menu import BQF_PT_Pie_QuickFavoritesMain

classes = (
    BQF_PT_Pie_QuickFavoritesMain,
)

def register_menus():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
def unregister_menus():

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    
    
    