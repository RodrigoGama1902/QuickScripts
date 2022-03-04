import bpy

from bpy.props import (IntProperty,
                       BoolProperty,
                       StringProperty,
                       CollectionProperty,
                       PointerProperty)

from bpy.types import (Operator,
                       Panel,
                       PropertyGroup,
                       UIList)

from .preferences import QS_Prefs
from .props import QS_Props_QuickScript

classes = (
    QS_Prefs, QS_Props_QuickScript
)

def register_properties():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.quick_scripts = bpy.props.PointerProperty(type= QS_Props_QuickScript)
    
def unregister_properties():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    
    del bpy.types.Scene.quick_scripts

