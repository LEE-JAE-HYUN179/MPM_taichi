import taichi as ti

arch = ti.vulkan if ti._lib.core.with_vulkan() else ti.cuda
ti.init(arch=arch)

########## simulation parameter ##############
particle_num = 512 * 8  ##python global variable : not updated in taichi kernel
particle_mass = 1
particle_initial_volume = 1
grid_res = 128
scene_len = 1
grid_dx = scene_len / grid_res
grid_inv_dx = 1 / grid_dx
dt = 1e-3

gravity = 9.8

# material property
rho_0 = particle_mass / particle_initial_volume

bulk_modulus = 1  ## lame's second coefficient
gamma = 7  ## compressibility

# taichi data
# particle data
ti_particle_pos = ti.Vector.field(3, ti.f32, particle_num)
ti_particle_vel = ti.Vector.field(3, ti.f32, particle_num)
ti_particle_F = ti.Matrix.field(3, 3, ti.f32, particle_num)  ## need?
ti_particle_Jp = ti.field(ti.f32, particle_num)

# grid data
ti_grid_force = ti.Vector.field(3, ti.f32, shape=(grid_res, grid_res, grid_res))
ti_grid_vel = ti.Vector.field(3, ti.f32, shape=(grid_res, grid_res, grid_res))
ti_grid_mass = ti.field(ti.f32, shape=(grid_res, grid_res, grid_res))

##########################################


window = ti.ui.Window('Window Title', (1280, 720))
scene = ti.ui.Scene()
camera = ti.ui.make_camera()
canvas = window.get_canvas()
canvas.set_background_color((1, 1, 1))


@ti.kernel
def init():
    # particle initialize
    for p in range(particle_num):
        ti_particle_pos[p] = [
            ti.random() * 0.2 + 0.5,
            ti.random() * 0.2 + 0.5,
            ti.random() * 0.2 + 0.5,
        ]
        ti_particle_Jp[p] = 1
        ti_particle_vel[p] = [0, 0, 0]

    # grid initialize
    for i, j, k in ti_grid_mass:
        ti_grid_mass[i, j, k] = 0
        ti_grid_vel[i, j, k] = [0, 0, 0]


@ti.kernel
def step():
    # init grid
    # can be optimized
    for i, j, k in ti_grid_mass:
        ti_grid_mass[i, j, k] = 0
        ti_grid_vel[i, j, k] = [0, 0, 0]
        ti_grid_force[i, j, k] = [0, 0, 0]

    # p2g
    for p in ti_particle_pos:
        pass

    # grid update

    # grid collision

    # g2p

    # particle update


def render():
    camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.RMB)
    scene.set_camera(camera)

    scene.point_light((0.5, 2, 0.5), (1, 1, 1))

    scene.particles(ti_particle_pos, 0.01, (0, 0, 1))
    canvas.scene(scene)


if __name__ == '__main__':
    init()

    camera.position(1, 1, 1)
    camera.lookat(0, 0, 0)
    camera.up(0, 1, 0)
    camera.fov(55)
    camera.projection_mode(ti.ui.ProjectionMode.Perspective)

    while window.running:
        for s in range(50):
            step()

        render()
        window.show()

    print("hello")
