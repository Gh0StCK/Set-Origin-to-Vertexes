bl_info = {
    "name": "Fast Set Origin",
    "author": "Stanislav Kolesnikov",
    "version": (1, 0, 4),
    "blender": (3, 4, 1),
    "location": "View 3D > Sidebar > FastTools",
    "description": "Set origin of the selected object to selected vertexes",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


import bpy
import bmesh
from mathutils import Vector
from bpy.types import Panel, Operator

def my_button_function(self, context):

    bpy.ops.object.mode_set(mode='EDIT')

    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    selected_verts = [v for v in bm.verts if v.select]    

    # вычислить центр выбранных вершин
    center = sum((v.co for v in selected_verts), Vector()) / len(selected_verts)

    bpy.ops.object.mode_set(mode='OBJECT')

    # переместить 3D курсор в центр
    bpy.context.scene.cursor.location = obj.matrix_world @ center
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    bpy.ops.object.mode_set(mode='EDIT')
    bm.free()

class MyPanel(Panel):
    bl_label = "Set Origin To Vertexes"
    bl_idname = "OBJECT_PT_set_origin_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FastTools"
    bl_context = "mesh_edit"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.set_origin_button", text="Set Origin To Vertexes")

class MyButton(Operator):
    bl_idname = "object.set_origin_button"
    bl_label = "Set Origin To Vertexes"

    def execute(self, context):
        my_button_function(self, context)
        return {'FINISHED'}
    
classes = [
    MyPanel,
    MyButton
]

def register():
    for cl in classes:
        bpy.utils.register_class(cl)

def unregister():
    for cl in reversed(classes):
        bpy.utils.unregister_class(cl)

if __name__ == "__main__":
    register()
