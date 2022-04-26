from DRCF import *
import powerup.remote as remote

z_min = 100
z_max = 800
x_min = -700
x_max = 700
y_min = 200
y_max = 800
r_min = -90
r_max = 90
t_min = 40
t_max = 180

v_max = 700
a_max = 700
speed_perc = 50
change_operation_speed(speed_perc)

set_singular_handling(DR_VAR_VEL)

d = 1000
fixed = True


def cross_vector(_posx1, _posx2):
    x1 = _posx1[0]
    y1 = _posx1[1]
    z1 = _posx1[2]

    x2 = _posx2[0]
    y2 = _posx2[1]
    z2 = _posx2[2]

    cross = [0, 0, 0]

    cross[0] = (y1 * z2) - (z1 * y2)
    cross[1] = (z1 * x2) - (x1 * z2)
    cross[2] = (x1 * y2) - (y1 * x2)

    return cross


def fixed_orientation(end_pose):
    R = get_current_rotm()
    pose, _ = get_current_posx()

    target_point = [pose[0] + R[0][2]*d, pose[1] + R[1][2]*d, pose[2] + R[2][2]*d]
    uz_x = target_point[0] - end_pose[0]
    uz_y = target_point[1] - end_pose[1]
    uz_z = target_point[2] - end_pose[2]
    distance = sqrt(uz_x*uz_x + uz_y*uz_y + uz_z*uz_z)

    uz = [uz_x/distance, uz_y/distance, uz_z/distance]
    ux_temp = [0, 0, 1]
    uy = cross_vector(uz, ux_temp)
    ux = cross_vector(uy, uz)

    Rn = [[ux[0], uy[0], uz[0]],
          [ux[1], uy[1], uz[1]],
          [ux[2], uy[2], uz[2]]]

    eul_angles = rotm2eul(Rn)
    return posx(end_pose[0], end_pose[1], end_pose[2], eul_angles[0], eul_angles[1], eul_angles[2])


def left():
    pose, _ = get_current_posx()
    pose[1] = x_min

    if fixed:
        pose = fixed_orientation(pose)

    amovel(pose, v=v_max, a=a_max)


def right():
    pose, _ = get_current_posx()
    pose[1] = x_max

    if fixed:
        pose = fixed_orientation(pose)

    amovel(pose, v=v_max, a=a_max)


def up():
    pose, _ = get_current_posx()
    pose[2] = z_max

    if fixed:
        pose = fixed_orientation(pose)

    amovel(pose, v=v_max, a=a_max)


def down():
    pose, _ = get_current_posx()
    pose[2] = z_min

    if fixed:
        pose = fixed_orientation(pose)

    amovel(pose, v=v_max, a=a_max)


def zoom_in():
    pose, _ = get_current_posx()
    pose[0] = y_max

    if fixed:
        pose = fixed_orientation(pose)

    amovel(pose, v=v_max, a=a_max)


def zoom_out():
    pose, _ = get_current_posx()
    pose[0] = y_min

    if fixed:
        pose = fixed_orientation(pose)

    amovel(pose, v=v_max, a=a_max)


def r_increase():
    pose, _ = get_current_posx()
    pose[3] = r_min
    pose[4] = 90
    pose[5] = 180
    amovel(pose, v=v_max, a=a_max)


def r_decrease():
    pose, _ = get_current_posx()
    pose[3] = r_max
    pose[4] = 90
    pose[5] = 180
    amovel(pose, v=v_max, a=a_max)


def t_increase():
    pose, _ = get_current_posx()
    pose[4] = t_max
    amovel(pose, v=v_max, a=a_max)


def t_decrease():
    pose, _ = get_current_posx()
    pose[4] = t_min
    amovel(pose, v=v_max, a=a_max)


def stop_motion():
    stop(DR_SSTOP)


def increase_speed():
    global speed_perc
    if speed_perc < 100:
        speed_perc = speed_perc + 10
        change_operation_speed(speed_perc)
    tp_log("speed={}".format(speed_perc))


def decrease_speed():
    global speed_perc
    if speed_perc > 0:
        speed_perc = speed_perc - 10
        change_operation_speed(speed_perc)
    tp_log("speed={}".format(speed_perc))


def enable_fixed_position():
    global fixed
    fixed = True


def disable_fixed_position():
    global fixed
    fixed = False


def toggle_fixed_position():
    global fixed
    fixed = not fixed
    tp_log("fixed={}".format(fixed))


def crazy_zoom():
    for i in range(4):
        movel(posx(0, 0, 100, 0, 0, 0), v=v_max*5, a=a_max*3, r=5, mod=DR_MV_MOD_REL, ref=DR_TOOL)
        movel(posx(0, 0, -50, 0, 0, 0), v=v_max*5, a=a_max*3, r=5, mod=DR_MV_MOD_REL, ref=DR_TOOL)


set_tcp("Camera")
movej(posj(-174.5, 9.2, -101.7, -5.7, -42.7, 8.1), v=60, a=100)
remote.start_tcp_remote_api(9225)
