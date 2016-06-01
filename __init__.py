bl_info = {
    "name": "Object Batch Baker",
    "author": "Florian Felix Meyer (tstscr)",
    "version": (0, 3, 0),
    "blender": (2, 74, 5),
    "location": "Properties >> Render >> Batch Baker",
    "description": "Batch Baking",
    "warning": "",
    "wiki_url": "",
    "category": "User",
}

if "bpy" in locals():
    import importlib
    importlib.reload(batch_bake_ui)
    importlib.reload(batch_bake_object_data)
    importlib.reload(batch_bake_operators)
    importlib.reload(batch_bake_utils)
else:
    from . import batch_bake_ui
    from . import batch_bake_object_data
    from . import batch_bake_operators
    from . import batch_bake_utils

import bpy

###########################################################################
def register():
    #print('MAIN REGISTER:\n', __name__)
    batch_bake_object_data.register()
    batch_bake_ui.register()
    batch_bake_operators.register()
    batch_bake_utils.register()

def unregister():
    #print('MAIN UN-REGISTER:\n', __name__)
    batch_bake_object_data.unregister()
    batch_bake_ui.unregister()
    batch_bake_operators.unregister()
    batch_bake_utils.unregister()

if __name__ == "__main__":
    register()
