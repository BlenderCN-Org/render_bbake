import bpy

import os
from time import time

_LOGTOCONSOLE = True

def setup_log():
    logname = 'BBake Baking Report'
    if not logname in bpy.data.texts:
        bpy.data.texts.new(logname)
    log = bpy.data.texts[logname]
    log.clear()
def msg(body, disp=True):
    if disp and _LOGTOCONSOLE:
        print(body)

    logname = 'BBake Baking Report'
    log = bpy.data.texts[logname]
    lines = body.split('\n')
    for line in lines:
        log.write(line+'\n')


def bbake_copy_settings(self, context):
    source = context.active_object
    targets = [ob for ob in context.selected_objects if ob.type == 'MESH' and not ob ==source]

    non_aov_keys = [
        'path',
        'use',
        'use_selected_to_active',
        'cage_object',
        'use_cage',
        'cage_extrusion',
        'align',
        'sources',
        ]

    bbs = source.bbake
    for target in targets:
        bbt = target.bbake
        for k,v in bbs.items():
            if self.copy_ob_settings and k in non_aov_keys:
                #print('OB->',k.upper().ljust(26),v)
                bbt[k] = v

            if self.copy_aov and k not in non_aov_keys:
                #print('AOV->',k.upper().ljust(26),v)
                bbt[k] = v


def set_scene_settings(context, bbake):
    '''Set scene bake settings to the bake settings of the object'''
    ob_settings = bbake.ob_settings
    bake_settings = context.scene.render.bake
    bake_settings.use_selected_to_active = ob_settings.use_selected_to_active
    bake_settings.cage_extrusion = ob_settings.cage_extrusion
    bake_settings.normal_space = bbake.aov_normal.normal_space
    bake_settings.normal_r = bbake.aov_normal.normal_r
    bake_settings.normal_g = bbake.aov_normal.normal_g
    bake_settings.normal_b = bbake.aov_normal.normal_b
    bake_settings.cage_extrusion = ob_settings.cage_extrusion
    bake_settings.use_cage = ob_settings.use_cage
    bake_settings.cage_object = ob_settings.cage_object
    bake_settings.margin = ob_settings.margin
    bake_settings.use_clear = ob_settings.use_clear
    context.scene.update()

def getsize(context, aov):
    '''Return image size of <bake_type> pass for this object'''
    if not aov.dimensions == 'CUSTOM':
        sizex = sizey = int(aov.dimensions)
        return sizex, sizey
        return aov.dimensions_custom.x, aov.dimensions_custom.y

def setup_image(context, filename, aov):
    sizex, sizey = getsize(context, aov)
    if filename in bpy.data.images:
        img = bpy.data.images[filename]
        if not img.source == 'GENERATED':
            img.source = 'GENERATED'
        img.generated_height = sizey
        img.generated_width = sizex
        image = img
    else:
        image = bpy.data.images.new('bakeimg', sizex, sizey)

    image.name = filename
    image.update()
    return image

def setup_bake_node(context, material, image):
    if not material.use_nodes:
        material.use_nodes = True

    nodes = material.node_tree.nodes
    bake_node = next(iter([n for n in nodes
                           if n.bl_idname == 'ShaderNodeTexImage'
                           and n.image
                           and n.image == image]),
                           None)
    if not bake_node:
        bake_node = nodes.new('ShaderNodeTexImage')
    bake_node.select = True
    nodes.active = bake_node
    bake_node.image = image
    bake_node.label = image.name
    
    context.scene.update()

    return bake_node

def setup_materials(context, ob, filename, aov):

    image = setup_image(context, filename, aov)
    for slot in ob.material_slots:
        if slot:
            if slot.material:
                setup_bake_node(context, slot.material, image)
    return image



def update_image(image, filepath):
    image.source = 'FILE'
    image.filepath = bpy.path.relpath(filepath)
    image.reload()
    image.update()


def register():
    #print('\nREGISTER:\n', __name__)
    pass

def unregister():
    #print('\nUN-REGISTER:\n', __name__)
    pass


