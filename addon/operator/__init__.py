import bpy

from .run_script import QS_OT_RunScripts, QS_OT_OpenFolder, QS_OT_FavoriteScript, QS_OT_RemoveFavoriteScript, QS_OT_OpenScriptInTextEditor, QS_OT_QuickExcScript

classes = (
    QS_OT_RunScripts,
    QS_OT_OpenFolder,
    QS_OT_FavoriteScript,
    QS_OT_RemoveFavoriteScript,
    QS_OT_OpenScriptInTextEditor,
    QS_OT_QuickExcScript
)


def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)