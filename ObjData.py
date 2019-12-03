# -*- coding: utf-8 -*-
from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame


class Point(object):
    def __init__(self, v, vt, vn):
        self.vertex = v
        self.texcoord = vt
        self.normal = vn


class Face(object):

    def __init__(self):
        self.points = []
        self.mtl_name = None

    def add_point(self, v, vt, vn):
        self.points.append(Point(v, vt, vn))


class ObjData(object):
    def __init__(self, file_dir, file_name):
        self.faces = []
        self.materials = {}
        self.gl_list = None
        self.read_obj_file(file_dir, file_name)
        self.make_gl_list()

    def read_obj_file(self, file_dir, file_name):
        file_path = file_dir + file_name
        vertices = []
        normals = []
        texcoords = []
        mtl_name = None
        for line in open(file_path, "r"):
            if line.startswith('#'):
                continue
            values = line.split()
            if len(values) == 0:
                continue
            if values[0] == 'v':
                vertices.append(map(float, values[1:4]))
            elif values[0] == 'vt':
                texcoords.append(map(float, values[1:3]))
            elif values[0] == 'vn':
                normals.append(map(float, values[1:4]))
            elif values[0] in ('usemtl', 'usemat'):
                mtl_name = values[1]
            elif values[0] == 'mtllib':
                self.read_mtl_file(file_dir, values[1])
            elif values[0] == 'f':
                face = Face()
                face.mtl_name = mtl_name
                for v in values[1:]:
                    p_num = v.split('/')
                    if len(p_num) < 3:
                        p_num = p_num + ['0'] * (3 - len(p_num))
                    p_v, p_vt, p_vn = map(lambda x: int(x)-1 if x > 0 else 0, p_num[0:3])
                    face.add_point(vertices[p_v], texcoords[p_vt], normals[p_vn])
                self.faces.append(face)

    def read_mtl_file(self, file_dir, file_name):
        file_path = file_dir + file_name
        mtl_now = None
        for line in open(file_path, "r"):
            if line.startswith('#'):
                continue
            values = line.split()
            if len(values) == 0:
                continue
            if values[0] == 'newmtl':
                mtl_now = self.materials[values[1]] = {}
            elif values[0] == 'map_Kd':
                # 读取贴图文件
                mtl_now[values[0]] = values[1]
                surf = pygame.image.load(file_dir + mtl_now['map_Kd'])
                image = pygame.image.tostring(surf, 'RGBA', 1)
                ix, iy = surf.get_rect().size
                texid = mtl_now['texture_Kd'] = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, texid)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                                GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                                GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                             GL_UNSIGNED_BYTE, image)
            else:
                mtl_now[values[0]] = map(float, values[1:])

    def make_gl_list(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            mtl_now = self.materials[face.mtl_name]
            if 'texture_Kd' in mtl_now:
                glBindTexture(GL_TEXTURE_2D, mtl_now['texture_Kd'])
            else:
                glColor(*mtl_now['Kd'])
            glBegin(GL_POLYGON)
            for point in face.points:
                glNormal3fv(point.normal)
                glTexCoord2fv(point.texcoord)
                glVertex3fv(point.vertex)
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
