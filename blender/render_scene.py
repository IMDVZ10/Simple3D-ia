import bpy
import math
import sys


argv = sys.argv
if "--" not in argv:
    raise RuntimeError("Missing render arguments.")
args = argv[argv.index("--") + 1 :]
kind, duration, width, height, output = args
duration = int(duration)
width = int(width)
height = int(height)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
plane = bpy.context.object
plane.name = "Ground"

bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.55, location=(0, 0, 2.2))
head = bpy.context.object
head.name = "Head"
head.data.materials.append(bpy.data.materials.new(name="Skin"))

bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.42, depth=1.5, location=(0, 0, 1.05))
body = bpy.context.object
body.name = "Body"
body.data.materials.append(bpy.data.materials.new(name="Shirt"))

bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.12, depth=1.1, location=(-0.32, 0, 0.15))
left_leg = bpy.context.object
left_leg.name = "LeftLeg"

bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.12, depth=1.1, location=(0.32, 0, 0.15))
right_leg = bpy.context.object
right_leg.name = "RightLeg"

for mesh in (plane, head, body, left_leg, right_leg):
    mesh.show_axis = False

if kind == "talking":
    head.rotation_euler[2] = math.radians(12)
elif kind == "walking":
    left_leg.rotation_euler[1] = math.radians(-12)
    right_leg.rotation_euler[1] = math.radians(12)

bpy.ops.object.light_add(type="AREA", location=(4, -4, 7))
bpy.context.object.data.energy = 900

bpy.ops.object.camera_add(location=(6, -8, 5))
camera = bpy.context.object
camera.rotation_euler = (math.radians(62), 0, math.radians(38))
bpy.context.scene.camera = camera

scene = bpy.context.scene
try:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
except TypeError:
    scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = width
scene.render.resolution_y = height
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = duration * 24
scene.render.filepath = output

scene.world.color = (0.08, 0.1, 0.15)

for frame in range(scene.frame_start, scene.frame_end + 1):
    scene.frame_set(frame)
    if kind == "walking":
        left_leg.rotation_euler[1] = math.radians(math.sin(frame * 0.25) * 18)
        right_leg.rotation_euler[1] = math.radians(-math.sin(frame * 0.25) * 18)
    elif kind == "talking":
        head.rotation_euler[2] = math.radians(math.sin(frame * 0.18) * 8)
    elif kind == "soccer":
        right_leg.rotation_euler[1] = math.radians(math.sin(frame * 0.2) * 20)

bpy.ops.render.render(animation=True)
