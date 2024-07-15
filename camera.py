import pygame as pg
from matrix_functions import *


class Camera: 
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100 


        self.moving_speed = 0.10
        self.rotation_speed = 0.01


    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_SPACE]:
            self.position += self.up * self.moving_speed
        if key[pg.K_LSHIFT]:
            self.position -= self.up * self.moving_speed

        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)
        if key[pg.K_UP]:
            self.camera_pitch(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_pitch(self.rotation_speed)

    # def control(self):
    #     key = pg.key.get_pressed()
        
    #     move_direction = np.zeros(4)
    #     if key[pg.K_a]:
    #         move_direction -= self.right
    #     if key[pg.K_d]:
    #         move_direction += self.right
    #     if key[pg.K_w]:
    #         move_direction += self.forward
    #     if key[pg.K_s]:
    #         move_direction -= self.forward
    #     if key[pg.K_SPACE]:
    #         move_direction += self.up
    #     if key[pg.K_LSHIFT]:
    #         move_direction -= self.up
        
    #     # Normalize move direction to prevent faster diagonal movement
    #     if np.linalg.norm(move_direction[:3]) > 0:
    #         move_direction[:3] = move_direction[:3] / np.linalg.norm(move_direction[:3])
        
    #     self.position += move_direction * self.moving_speed

    #     if key[pg.K_LEFT]:
    #         self.camera_yaw(-self.rotation_speed)
    #     if key[pg.K_RIGHT]:
    #         self.camera_yaw(self.rotation_speed)
    #     if key[pg.K_UP]:
    #         self.camera_pitch(-self.rotation_speed)
    #     if key[pg.K_DOWN]:
    #         self.camera_pitch(self.rotation_speed)



    def camera_yaw(self, angle):
        rotate = rotate_y(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_pitch(self, angle):
            rotate = rotate_x(angle)
            self.forward = self.forward @ rotate
            self.right = self.right @ rotate
            self.up = self.up @ rotate


    # def camera_yaw(self, angle):
    #     rotate = rotate_y(angle)
    #     self.forward = self.forward @ rotate
    #     self.forward /= np.linalg.norm(self.forward[:3])
        
    #     # Recompute the right vector
    #     self.right = np.cross(self.up[:3], self.forward[:3])
    #     self.right = np.append(self.right, 1.0)
    #     self.right /= np.linalg.norm(self.right[:3])
        
    #     # Recompute the up vector
    #     self.up = np.cross(self.forward[:3], self.right[:3])
    #     self.up = np.append(self.up, 1.0)
    #     self.up /= np.linalg.norm(self.up[:3])

   
    # def camera_pitch(self, angle):
    #     rotate = rotate_x(angle)
    #     self.forward = self.forward @ rotate
    #     self.forward /= np.linalg.norm(self.forward[:3])
        
    #     # Recompute the up vector
    #     self.up = np.cross(self.forward[:3], self.right[:3])
    #     self.up = np.append(self.up, 1.0)
    #     self.up /= np.linalg.norm(self.up[:3])
        
    #     # Recompute the right vector
    #     self.right = np.cross(self.up[:3], self.forward[:3])
    #     self.right = np.append(self.right, 1.0)
    #     self.right /= np.linalg.norm(self.right[:3])

    def translate_matrix(self): 
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0], 
            [0, 1, 0, 1],
            [0, 0, 1, 0], 
            [-x, -y,  -z, 1]
        ])
    
    def rotate_matrix(self): 
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up 
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
    
    def camera_matrix(self): 
        return self.translate_matrix() @ self.rotate_matrix()