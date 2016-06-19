import bpy
from bpy.types import Panel

###########################################################################
class CyclesButtonsPanel:
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    COMPAT_ENGINES = {'CYCLES'}

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        ob = context.active_object
        return rd.engine in cls.COMPAT_ENGINES and ob and ob.type == 'MESH'

class BBake_Panel(CyclesButtonsPanel, Panel):
    bl_label = "BBake"
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'CYCLES'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        cscene = scene.cycles
        cbk = scene.render.bake
        ob = context.active_object
        bbake = ob.bbake
        ob_settings = bbake.ob_settings

        col = layout.column()

        row=col.row(align=True)
        row.operator('scene.bbake_bake_selected', icon='RENDER_STILL', text='Bake Selected Objects')
        row.operator('scene.bbake_bake_selected', icon='RENDER_STILL', text='Bake All Objects').all=True
        col.separator()
        col.separator()
        col.prop(ob_settings, 'use', text='Bake this object ("%s")' %ob.name, toggle=0)

        if ob_settings.use:
            ### SELECTED TO ACTIVE SETTINGS
            box = col.box()
            box.prop(ob_settings, 'path')
            row = box.row()
            row.prop(ob_settings, 'use_selected_to_active')
            if ob_settings.use_selected_to_active:
                if ob_settings.sources:
                    sources = [s.strip() for s in ob_settings.sources.split(',')]
                    if len(sources) == 1:
                        row.prop(ob_settings, 'align')

                row = box.row()
                row.prop(ob_settings, 'use_cage')
                if ob_settings.use_cage:
                    row.prop(ob_settings, 'cage_object', icon='OBJECT_DATAMODE')

                row=box.row()
                row.prop(ob_settings, 'cage_extrusion')

                subbox = box.box()
                row=subbox.row()
                row.label('Source Objects:')
                row.operator('object.set_bbake_sources', icon='FORWARD', text='Set Sources')
                row=subbox.row()
                if ob_settings.sources:
                    row.prop(ob_settings, 'sources', text='')

            ### AOVs SETTINGS
            box = col.box()

            row = box.row()
            row.label('AOVs:')
            row.operator('object.bbake_copy_settings', text='Copy Settings', icon='COPY_ID')

            #COMBINED
            aov_combined = bbake.aov_combined
            box_combined = box.box()
            row = box_combined.row()
            row.prop(aov_combined, 'use')
            if aov_combined.dimensions == 'CUSTOM':
                row.prop(aov_combined, 'dimensions_custom', text='')
            row.prop(aov_combined, 'dimensions', text='')
            if aov_combined.use:
                row=box_combined.row()
                row.prop(aov_combined, 'use_pass_ao')
                row.prop(aov_combined, 'use_pass_emit')
                row=box_combined.row(align=True)
                row.prop(aov_combined, 'use_pass_direct', toggle=True)
                row.prop(aov_combined, 'use_pass_indirect', toggle=True)
                row=box_combined.row()
                row.prop(aov_combined, 'use_pass_diffuse')
                row.prop(aov_combined, 'use_pass_transmission')
                row=box_combined.row()
                row.prop(aov_combined, 'use_pass_glossy')
                row.prop(aov_combined, 'use_pass_subsurface')

            #DIFFUSE
            aov_diffuse = bbake.aov_diffuse
            box_diffuse = box.box()
            row = box_diffuse.row()
            row.prop(aov_diffuse, 'use')
            if aov_diffuse.dimensions == 'CUSTOM':
                row.prop(aov_diffuse, 'dimensions_custom', text='')
            row.prop(aov_diffuse, 'dimensions', text='')
            if aov_diffuse.use:
                row = box_diffuse.row(align=True)
                row.prop(aov_diffuse, 'use_pass_direct', toggle=True)
                row.prop(aov_diffuse, 'use_pass_indirect', toggle=True)
                row.prop(aov_diffuse, 'use_pass_color', toggle=True)

            #GLOSSY
            aov_glossy = bbake.aov_glossy
            box_glossy = box.box()
            row = box_glossy.row()
            row.prop(aov_glossy, 'use')
            if aov_glossy.dimensions == 'CUSTOM':
                row.prop(aov_glossy, 'dimensions_custom', text='')
            row.prop(aov_glossy, 'dimensions', text='')
            if aov_glossy.use:
                row = box_glossy.row(align=True)
                row.prop(aov_glossy, 'use_pass_direct', toggle=True)
                row.prop(aov_glossy, 'use_pass_indirect', toggle=True)
                row.prop(aov_glossy, 'use_pass_color', toggle=True)

            #TRANSMISSION
            aov_transmission = bbake.aov_transmission
            box_transmission = box.box()
            row = box_transmission.row()
            row.prop(aov_transmission, 'use')
            if aov_transmission.dimensions == 'CUSTOM':
                row.prop(aov_transmission, 'dimensions_custom', text='')
            row.prop(aov_transmission, 'dimensions', text='')
            if aov_transmission.use:
                row = box_transmission.row(align=True)
                row.prop(aov_transmission, 'use_pass_direct', toggle=True)
                row.prop(aov_transmission, 'use_pass_indirect', toggle=True)
                row.prop(aov_transmission, 'use_pass_color', toggle=True)

            #SUBSURFACE
            aov_subsurface = bbake.aov_subsurface
            box_subsurface = box.box()
            row = box_subsurface.row()
            row.prop(aov_subsurface, 'use')
            if aov_subsurface.dimensions == 'CUSTOM':
                row.prop(aov_subsurface, 'dimensions_custom', text='')
            row.prop(aov_subsurface, 'dimensions', text='')
            if aov_subsurface.use:
                row = box_subsurface.row(align=True)
                row.prop(aov_subsurface, 'use_pass_direct', toggle=True)
                row.prop(aov_subsurface, 'use_pass_indirect', toggle=True)
                row.prop(aov_subsurface, 'use_pass_color', toggle=True)

            #NORMAL
            aov_normal = bbake.aov_normal
            box_normal = box.box()
            row = box_normal.row()
            row.prop(aov_normal, 'use')
            if aov_normal.dimensions == 'CUSTOM':
                row.prop(aov_normal, 'dimensions_custom', text='')
            row.prop(aov_normal, 'dimensions', text='')
            if aov_normal.use:
                box_normal.label('Normal Settings:')
                box_normal.prop(aov_normal, "normal_space", text="Space")
                row = box_normal.row(align=True)
                row.label(text="Swizzle:")
                row.prop(aov_normal, "normal_r", text="")
                row.prop(aov_normal, "normal_g", text="")
                row.prop(aov_normal, "normal_b", text="")

            #AO
            aov_ao = bbake.aov_ao
            box_ao = box.box()
            row = box_ao.row()
            row.prop(aov_ao, 'use')
            if aov_ao.dimensions == 'CUSTOM':
                row.prop(aov_ao, 'dimensions_custom', text='')
            row.prop(aov_ao, 'dimensions', text='')

            #SHADOW
            aov_shadow = bbake.aov_shadow
            box_shadow = box.box()
            row = box_shadow.row()
            row.prop(aov_shadow, 'use')
            if aov_shadow.dimensions == 'CUSTOM':
                row.prop(aov_shadow, 'dimensions_custom', text='')
            row.prop(aov_shadow, 'dimensions', text='')

            #EMIT
            aov_emit = bbake.aov_emit
            box_emit = box.box()
            row = box_emit.row()
            row.prop(aov_emit, 'use')
            if aov_emit.dimensions == 'CUSTOM':
                row.prop(aov_emit, 'dimensions_custom', text='')
            row.prop(aov_emit, 'dimensions', text='')

            #UV
            aov_uv = bbake.aov_uv
            box_uv = box.box()
            row = box_uv.row()
            row.prop(aov_uv, 'use')
            if aov_uv.dimensions == 'CUSTOM':
                row.prop(aov_uv, 'dimensions_custom', text='')
            row.prop(aov_uv, 'dimensions', text='')

            #ENVIRONMENT
            aov_environment = bbake.aov_environment
            box_env = box.box()
            row = box_env.row()
            row.prop(aov_environment, 'use')
            if aov_environment.dimensions == 'CUSTOM':
                row.prop(aov_environment, 'dimensions_custom', text='')
            row.prop(aov_environment, 'dimensions', text='')


def register():
    #print('\nREGISTER:\n', __name__)
    bpy.utils.register_class(BBake_Panel)

def unregister():
    #print('\nUN-REGISTER:\n', __name__)
    bpy.utils.unregister_class(BBake_Panel)
