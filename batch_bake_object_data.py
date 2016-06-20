'''
BBake Object_Data
holds all the per object per aov-pass settings for baking

'''

import bpy
from bpy.props import *
from bpy.types import PropertyGroup

size_items = [('265','265',''),
    ('512','512',''),
    ('1024','1024',''),
    ('2048','2048',''),
    ('4096','4096',''),
    ('CUSTOM','Custom',''),
    ]
normal_space_items = [
    ('TANGENT', 'Tangent', ''),
    ('OBJECT', 'Object', ''),
    ]
swizzle_items = [
    ('POS_X', '+X', ''),
    ('POS_Y', '+Y', ''),
    ('POS_Z', '+Z', ''),
    ('NEG_X', '-X', ''),
    ('NEG_Y', '-Y', ''),
    ('NEG_Z', '-Z', ''),
    ]

class AOV():
    #for all passes
    use = BoolProperty(name='use',
        default=False)
    dimensions = EnumProperty(
        items=size_items,
        )
    dimensions_custom = IntVectorProperty(
        name='Dimensions',
        size=2,
        default=(265, 265)
        )

    #for select passes
    use_pass_direct = BoolProperty(
        name='Direct',
        default=True)
    use_pass_indirect = BoolProperty(
        name='Indirect',
        default=True)
    use_pass_color = BoolProperty(
        name='Color',
        default=True)

    #for combined pass
    use_pass_transmission = BoolProperty(
        name='Transmission',
        default=True)
    use_pass_ambient_occlusion = BoolProperty(
        name='AO',
        default=True)
    use_pass_emit = BoolProperty(
        name='Emit',
        default=True)
    use_pass_subsurface = BoolProperty(
        name='Subsurface',
        default=True)
    use_pass_diffuse = BoolProperty(
        name='Diffuse',
        default=True)
    use_pass_glossy = BoolProperty(
        name='Glossy',
        default=True)

    #for normal pass
    normal_space = EnumProperty(
        name='Space:',
        items=normal_space_items,
        )
    normal_r = EnumProperty(
        items=swizzle_items,
        default='POS_X',
        )
    normal_g = EnumProperty(
        items=swizzle_items,
        default='POS_Y',
        )
    normal_b = EnumProperty(
        items=swizzle_items,
        default='POS_Z',
        )

class BBake_Object_Settings(PropertyGroup):
    use = BoolProperty(
        name='Bake this Object',
        default=False,
        description='Do not ignore this Object when baking.',
        )
    path = StringProperty(
        name='Bake Folder',
        subtype='DIR_PATH',
        default='//textures/',
        description='Save baked images in this Folder.',
        )
    sources = StringProperty(
        name='Source Objects',
        description='Comma separated list of source object names.'
        )
    align = BoolProperty(
        name='Align Origins',
        default=False,
        description='Align origins of source and cage object with bake object (Only if single source object).',
        )
    use_selected_to_active = BoolProperty(
        name='Selcted to active',
        default=False,
        )
    use_cage = BoolProperty(
        name='Cage',
        default=False,
        )
    cage_extrusion = FloatProperty(
        name='Extrusion',
        default=0.1,
        )
    cage_object = StringProperty(
        name='Cage Object Name',
        default='',
        description='Name of object to use as cage for raycasting.',
        )
    margin = IntProperty(
        name='Margin',
        default=16,
        description='Extends the baked result as a post process filter')
    use_clear = BoolProperty(
        name='Clear',
        default=True,
        description='Clear Images Before baking')

class AOV_Diffuse(PropertyGroup, AOV):
    name = StringProperty(name='name', default='Diffuse')

class AOV_Glossy(PropertyGroup, AOV):
    name = StringProperty(name='name', default='Glossy')

class AOV_Transmission(PropertyGroup, AOV):
    name = StringProperty(name='name', default='Transmission')

class AOV_Subsurface(PropertyGroup, AOV):
    name = StringProperty(name='name', default='Subsurface')

class AOV_Normal(PropertyGroup, AOV):
    name = StringProperty(name='name', default='Normal')

class AOV_AO(PropertyGroup, AOV):
    name = StringProperty(name='name', default='AO')

class AOV_Combined(PropertyGroup, AOV):
    name = StringProperty(name='name', default='Combined')

class AOV_Shadow(PropertyGroup, AOV):
    name = StringProperty(name='name', default='Shadow')

class AOV_Emit(PropertyGroup, AOV):
    name = StringProperty(name='name', default='Emit')

class AOV_UV(PropertyGroup, AOV):
    name = StringProperty(name='name', default='UV')

class AOV_Environment(PropertyGroup, AOV):
    name = StringProperty(name='name', default='Environment')

###########################################################################
class BBake_Object_Data(PropertyGroup):
    ### OBJECT BAKE SETTINGS
    ob_settings = PointerProperty(type=BBake_Object_Settings)
    ### PER AOV SETTINGS
    aov_diffuse = PointerProperty(type=AOV_Diffuse)
    aov_glossy = PointerProperty(type=AOV_Glossy)
    aov_transmission = PointerProperty(type=AOV_Transmission)
    aov_subsurface = PointerProperty(type=AOV_Subsurface)
    aov_normal = PointerProperty(type=AOV_Normal)
    aov_ao = PointerProperty(type=AOV_AO)
    aov_combined = PointerProperty(type=AOV_Combined)
    aov_shadow = PointerProperty(type=AOV_Shadow)
    aov_emit = PointerProperty(type=AOV_Emit)
    aov_uv = PointerProperty(type=AOV_UV)
    aov_environment = PointerProperty(type=AOV_Environment)


###########################################################################
def register():
    #print('\nREGISTER:\n', __name__)
    bpy.utils.register_class(BBake_Object_Settings)
    bpy.utils.register_class(AOV_Diffuse)
    bpy.utils.register_class(AOV_Glossy)
    bpy.utils.register_class(AOV_Transmission)
    bpy.utils.register_class(AOV_Subsurface)
    bpy.utils.register_class(AOV_Normal)
    bpy.utils.register_class(AOV_AO)
    bpy.utils.register_class(AOV_Combined)
    bpy.utils.register_class(AOV_Shadow)
    bpy.utils.register_class(AOV_Emit)
    bpy.utils.register_class(AOV_UV)
    bpy.utils.register_class(AOV_Environment)

    bpy.utils.register_class(BBake_Object_Data)
    bpy.types.Object.bbake = PointerProperty(type=BBake_Object_Data)

def unregister():
    #print('\nUN-REGISTER:\n', __name__)
    bpy.utils.unregister_class(BBake_Object_Data)

    bpy.utils.unregister_class(AOV_Diffuse)
    bpy.utils.unregister_class(AOV_Glossy)
    bpy.utils.unregister_class(AOV_Transmission)
    bpy.utils.unregister_class(AOV_Subsurface)
    bpy.utils.unregister_class(AOV_Normal)
    bpy.utils.unregister_class(AOV_AO)
    bpy.utils.unregister_class(AOV_Combined)
    bpy.utils.unregister_class(AOV_Shadow)
    bpy.utils.unregister_class(AOV_Emit)
    bpy.utils.unregister_class(AOV_UV)
    bpy.utils.unregister_class(AOV_Environment)

    del bpy.types.Object.bbake


