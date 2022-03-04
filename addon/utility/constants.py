import bpy
import pathlib
import os

addon_name = __name__.partition('.')[0]
command_file_name = 'qs_favorites.json'
favorites_path = os.path.join(os.path.dirname(pathlib.Path(__file__).parent.absolute()), command_file_name)
operator_text_detect = ['# test call','#testecall','#teste call','#modal call','#modal-call']

### UI Param

layout_scale_x = 1.1
layout_scale_y = 1.3