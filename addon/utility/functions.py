import bpy
import os
import json

from .constants import addon_name, favorites_path, command_file_name

def get_prefs():
    return bpy.context.preferences.addons[addon_name].preferences

def json_favorites_path():

    prefs = get_prefs()

    if not prefs.favorites_path:
        return favorites_path
    else:
        return os.path.join(prefs.favorites_path, command_file_name)
    
def convert_ab_path(filepath):
    if filepath.startswith('//'):
            filepath = (os.path.abspath(bpy.path.abspath(filepath)) + '\\')

    return filepath

def json_check(json_path):

    try:
        with open(json_path) as json_file:
            json_data = json.load(json_file)
    except ValueError as e:
        print('QS: Invalid Json')
        return False
    return True





