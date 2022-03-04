

def register_addon():

    from ..property import register_properties
    register_properties()

    from ..operator import register_operators
    register_operators()

    from ..menu import register_menus
    register_menus()

    from .keymap import register_keymap
    register_keymap()

def unregister_addon():

    from ..property import unregister_properties
    unregister_properties()

    from ..operator import unregister_operators
    unregister_operators()
    
    from ..menu import unregister_menus
    unregister_menus()

    from .keymap import unregister_keymap
    unregister_keymap()

