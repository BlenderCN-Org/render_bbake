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

        col = layout.column()

        row=col.row(align=True)
        row.operator('scene.bbake_bake_selected', icon='RENDER_STILL', text='Bake Selected Objects')
        row.operator('scene.bbake_bake_selected', icon='RENDER_STILL', text='Bake All Objects').all=True
        col.separator()
        col.separator()
        col.prop(bbake, 'use', text='Bake this object ("%s")' %ob.name, toggle=0)

        if ob.bbake.use:
            ### SELECTED TO ACTIVE SETTINGS
            box = col.box()
            box.prop(ob.bbake, 'path')
            row = box.row()
            row.prop(ob.bbake, 'use_selected_to_active')
            if ob.bbake.use_selected_to_active:
                if ob.bbake.sources:
                    sources = [s.strip() for s in ob.bbake.sources.split(',')]
                    if len(sources) == 1:
                        row.prop(ob.bbake, 'align')

                row = box.row()
                row.prop(ob.bbake, 'use_cage')
                if ob.bbake.use_cage:
                    row.prop(ob.bbake, 'cage_object', icon='OBJECT_DATAMODE')

                row=box.row()
                row.prop(ob.bbake, 'cage_extrusion')

                subbox = box.box()
                row=subbox.row()
                row.label('Source Objects:')
                row.operator('object.set_bbake_sources', icon='FORWARD', text='Set Sources')
                row=subbox.row()
                if ob.bbake.sources:
                    row.prop(ob.bbake, 'sources', text='')
                    #sources = [s.strip() for s in ob.bbake.sources.split(',')]
                    #for s in sources:
                    #    row.label('"%s"'%s)

            ### AOVs SETTINGS
            box = col.box()

            row = box.row()
            row.label('AOVs:')
            row.operator('object.bbake_copy_settings', text='Copy Settings', icon='COPY_ID')

            #COMBINED
            box_combined = box.box()
            row = box_combined.row()
            row.prop(ob.bbake, 'combined')
            if ob.bbake.combinedsize == 'CUSTOM':
                row.prop(ob.bbake, 'combinedsize_custom', text='')
            row.prop(ob.bbake, 'combinedsize', text='')
            if ob.bbake.combined:
                row=box_combined.row()
                row.prop(ob.bbake, 'combined_use_pass_ao')
                row.prop(ob.bbake, 'combined_use_pass_emit')
                row=box_combined.row(align=True)
                row.prop(ob.bbake, 'combined_use_pass_direct', toggle=True)
                row.prop(ob.bbake, 'combined_use_pass_indirect', toggle=True)
                row=box_combined.row()
                row.prop(ob.bbake, 'combined_use_pass_diffuse')
                row.prop(ob.bbake, 'combined_use_pass_transmission')
                row=box_combined.row()
                row.prop(ob.bbake, 'combined_use_pass_glossy')
                row.prop(ob.bbake, 'combined_use_pass_subsurface')

            #DIFFUSE
            box_diffuse = box.box()
            row = box_diffuse.row()
            row.prop(ob.bbake, 'diffuse_pass')
            if ob.bbake.diffsize == 'CUSTOM':
                row.prop(ob.bbake, 'diffsize_custom', text='')
            row.prop(ob.bbake, 'diffsize', text='')
            if ob.bbake.diffuse_pass:
                row = box_diffuse.row(align=True)
                row.prop(ob.bbake, 'diffuse_use_pass_direct', toggle=True)
                row.prop(ob.bbake, 'diffuse_use_pass_indirect', toggle=True)
                row.prop(ob.bbake, 'diffuse_use_pass_color', toggle=True)

            #GLOSSY
            box_glossy = box.box()
            row = box_glossy.row()
            row.prop(ob.bbake, 'glossy_pass')
            if ob.bbake.specsize == 'CUSTOM':
                row.prop(ob.bbake, 'specsize_custom', text='')
            row.prop(ob.bbake, 'specsize', text='')
            if ob.bbake.glossy_pass:
                row = box_glossy.row(align=True)
                row.prop(ob.bbake, 'glossy_use_pass_direct', toggle=True)
                row.prop(ob.bbake, 'glossy_use_pass_indirect', toggle=True)
                row.prop(ob.bbake, 'glossy_use_pass_color', toggle=True)

            #TRANSMISSION
            box_transmission = box.box()
            row = box_transmission.row()
            row.prop(ob.bbake, 'transmission_pass')
            if ob.bbake.transmissionsize == 'CUSTOM':
                row.prop(ob.bbake, 'transmissionsize_custom', text='')
            row.prop(ob.bbake, 'transmissionsize', text='')
            if ob.bbake.transmission_pass:
                row = box_transmission.row(align=True)
                row.prop(ob.bbake, 'transmission_use_pass_direct', toggle=True)
                row.prop(ob.bbake, 'transmission_use_pass_indirect', toggle=True)
                row.prop(ob.bbake, 'transmission_use_pass_color', toggle=True)

            #SUBSURFACE
            box_subsurface = box.box()
            row = box_subsurface.row()
            row.prop(ob.bbake, 'subsurface_pass')
            if ob.bbake.subsurfacesize == 'CUSTOM':
                row.prop(ob.bbake, 'subsurfacesize_custom', text='')
            row.prop(ob.bbake, 'subsurfacesize', text='')
            if ob.bbake.subsurface_pass:
                row = box_subsurface.row(align=True)
                row.prop(ob.bbake, 'subsurface_use_pass_direct', toggle=True)
                row.prop(ob.bbake, 'subsurface_use_pass_indirect', toggle=True)
                row.prop(ob.bbake, 'subsurface_use_pass_color', toggle=True)

            #NORMAL
            box_normal = box.box()
            row = box_normal.row()
            row.prop(ob.bbake, 'normal')
            if ob.bbake.normalsize == 'CUSTOM':
                row.prop(ob.bbake, 'normalsize_custom', text='')
            row.prop(ob.bbake, 'normalsize', text='')
            if ob.bbake.normal:
                box_normal.label('Normal Settings:')
                box_normal.prop(ob.bbake, "normal_space", text="Space")
                row = box_normal.row(align=True)
                row.label(text="Swizzle:")
                row.prop(ob.bbake, "normal_r", text="")
                row.prop(ob.bbake, "normal_g", text="")
                row.prop(ob.bbake, "normal_b", text="")

            #AO
            box_ao = box.box()
            row = box_ao.row()
            row.prop(ob.bbake, 'ao')
            if ob.bbake.aosize == 'CUSTOM':
                row.prop(ob.bbake, 'aosize_custom', text='')
            row.prop(ob.bbake, 'aosize', text='')

            #SHADOW
            box_shadow = box.box()
            row = box_shadow.row()
            row.prop(ob.bbake, 'shadow')
            if ob.bbake.shadowsize == 'CUSTOM':
                row.prop(ob.bbake, 'shadowsize_custom', text='')
            row.prop(ob.bbake, 'shadowsize', text='')

            #EMIT
            box_emit = box.box()
            row = box_emit.row()
            row.prop(ob.bbake, 'emit')
            if ob.bbake.emitsize == 'CUSTOM':
                row.prop(ob.bbake, 'emitsize_custom', text='')
            row.prop(ob.bbake, 'emitsize', text='')

            #UV
            box_uv = box.box()
            row = box_uv.row()
            row.prop(ob.bbake, 'uv')
            if ob.bbake.uvsize == 'CUSTOM':
                row.prop(ob.bbake, 'uvsize_custom', text='')
            row.prop(ob.bbake, 'uvsize', text='')

            #ENVIRONMENT
            box_env = box.box()
            row = box_env.row()
            row.prop(ob.bbake, 'env')
            if ob.bbake.envsize == 'CUSTOM':
                row.prop(ob.bbake, 'envsize_custom', text='')
            row.prop(ob.bbake, 'envsize', text='')


def register():
    #print('\nREGISTER:\n', __name__)
    bpy.utils.register_class(BBake_Panel)

def unregister():
    #print('\nUN-REGISTER:\n', __name__)
    bpy.utils.unregister_class(BBake_Panel)
