# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ObjData import ObjData

WIN_SIZE = (400, 300)
WIN_POSITION = (300, 200)
TITLE = "Model Display"

obj_data = None
draw_interval = 20  # ms  1000ms/frame
rotate_angle = 0  # °
rotate_speed = 30  # °/s
scale = 1


def init_window(win_size, win_pos, title):
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(win_size[0], win_size[1])
    glutInitWindowPosition(win_pos[0], win_pos[1])
    glutCreateWindow(title)


def read_obj_data(file_path):
    global obj_data
    file_dir, file_name = os.path.dirname(file_path)+'/', os.path.basename(file_path)
    obj_data = ObjData(file_dir, file_name)


def set_window(win_size):
    #  平行光
    glLightfv(GL_LIGHT0, GL_POSITION, (-50, 100, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = win_size
    gluPerspective(90.0, width / float(height), 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 1, 0.7, 0)

    glLoadIdentity()
    gluLookAt(0.0, 5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glTranslatef(0, 0, 0)
    glRotate(rotate_angle, 0, 1, 0)
    glScale(scale, scale, scale)
    glCallList(obj_data.gl_list)

    glutSwapBuffers()


def mouse_wheel_callback(button, direction, x, y):
    global scale
    scale += direction * 0.1
    glutPostRedisplay()


def on_timer(value):
    global rotate_angle, rotate_speed, draw_interval
    rotate_angle += rotate_speed * draw_interval/1000.0
    glutPostRedisplay()
    glutTimerFunc(draw_interval, on_timer, 0)


def display(file_path):
    init_window(WIN_SIZE, WIN_POSITION, TITLE)
    set_window(WIN_SIZE)
    read_obj_data(file_path)

    glutDisplayFunc(draw)
    glutMouseWheelFunc(mouse_wheel_callback)
    glutTimerFunc(draw_interval, on_timer, 0)
    glutMainLoop()


