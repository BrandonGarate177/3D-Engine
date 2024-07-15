import numpy as np
import math

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array(position, dtype=float)
        self.yaw = 0
        self.pitch = 0
        self.mouse_sensitivity = 0.01
        self.moving_speed = 0.02

        self.near_plane = 0.1
        self.far_plane = 1000.0
        self.h_fov = math.radians(90)
        self.v_fov = self.h_fov * (self.render.HEIGHT / self.render.WIDTH)

        self.update_vectors()

    def update_vectors(self):
        # Calculate the new direction vector
        x = math.cos(self.yaw) * math.cos(self.pitch)
        z = math.sin(self.yaw) * math.cos(self.pitch)
        y = math.sin(self.pitch)
        self.forward = np.array([x, y, z])
        self.right = np.cross(np.array([0, 1, 0]), self.forward)
        self.up = np.cross(self.forward, self.right)

    def camera_matrix(self):
        # Camera position (eye point)
        eye = self.position
        # Camera looking direction (forward vector)
        center = eye + self.forward
        # Up vector for the camera
        up = self.up

        # Normalized forward vector (z-axis of the camera)
        zaxis = (center - eye) / np.linalg.norm(center - eye)
        # Right vector (x-axis of the camera)
        xaxis = np.cross(up, zaxis)
        xaxis /= np.linalg.norm(xaxis)  # Normalize x-axis
        # Camera up vector (y-axis of the camera)
        yaxis = np.cross(zaxis, xaxis)  # Corrected cross product order

        # Camera rotation matrix
        R = np.array([
            [xaxis[0], yaxis[0], zaxis[0], 0],
            [xaxis[1], yaxis[1], zaxis[1], 0],
            [xaxis[2], yaxis[2], zaxis[2], 0],
            [0, 0, 0, 1]
        ])

        # Camera translation matrix
        T = np.array([
            [1, 0, 0, -eye[0]],
            [0, 1, 0, -eye[1]],
            [0, 0, 1, -eye[2]],
            [0, 0, 0, 1]
        ])

        # The view matrix is the product of the rotation and translation matrices
        return R @ T


    def control_mouse(self, event):
        dx, dy = event.rel
        self.yaw += dx * self.mouse_sensitivity
        self.pitch -= dy * self.mouse_sensitivity
        self.pitch = max(-math.pi/2, min(math.pi/2, self.pitch))
        self.update_vectors()
