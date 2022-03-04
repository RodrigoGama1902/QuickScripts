import bpy

keys = []

def register_keymap():

    wm = bpy.context.window_manager
    addon_keyconfig = wm.keyconfigs.addon
    kc = addon_keyconfig

    km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")

    kmi = km.keymap_items.new("wm.call_menu_pie", "Q", "PRESS", ctrl=False, shift=True)
    kmi.properties.name = "qs.piequickfavorites"   
    keys.append((km, kmi))

    kmi = km.keymap_items.new("qs.quickrunscript", "Q", "PRESS", ctrl=True, shift=True)   
    keys.append((km, kmi))

def unregister_keymap():

    for km, kmi in keys:
        km.keymap_items.remove(kmi)

    keys.clear()