from object_3d import *
from camera import *
from projection import *
import pygame as pg


class SoftwareRender: 
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT= 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2 
        self.FPS = 144 
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.paused = False
        self.create_objects()


    # Translation matrix 

    # [[1, 0, 0, 0],
    #  [0, 1, 0, 0],
    #  [0, 0, 1, 0],
    #  [tx, ty, tz, 1]]

    # THIS IS SUPER DUPPA CRAZY MAD IMPORTANT TYPE SHIIIIIIT

    # Scaling matrix 

    # [[Sx, 0, 0, 0],
    #  [0, Sy, 0, 0],
    #  [0, 0, Sz, 0],
    #  [0, 0, 0, 1]]

    # this up here is deadass the most important part of the program, its the math type shit. I am gonna put it in a seperate file to make the program easier to code
    # im feeling big brain type shiiit 

    def create_objects(self):
        self.camera = Camera(self, [-5, 5, -50])
        # self.camera = Camera(self , [0.5, 1, -4])
        self.projection = Projection(self)
        self.object = self.get_object_from_file('resources/t_34_obj1.obj')
        # self.object = Object3D(self)
        self.object.translate([0.2, 0.4, 0.2])

        # self.axes = Axes(self)
        # self.axes.translate([0.7, 0.9, 0.7])
        # self.world_axes= Axes(self)
        # self.world_axes.movement_flag = False
        # self.world_axes.scale(2.5)
        # self.world_axes.translate([0.0001, 0.0001, 0.0001])

    def get_object_from_file(self, filename):
            vertex, faces = [], []
            with open(filename) as f:
                for line in f:
                    if line.startswith('v '):
                        vertex.append([float(i) for i in line.split()[1:]] + [1])
                    elif line.startswith('f'):
                        faces_ = line.split()[1:]
                        faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
            return Object3D(self, vertex, faces)    

# CHEK THIS FUNCTION ^^^^
    def draw(self):
        self.screen.fill(pg.Color('darkslategray'))
        # self.axes.draw()
        # self.world_axes.draw()
        self.object.draw()

    # def run(self): 
    #     while True:
    #         self.draw()
    #         self.camera.control()
    #         [exit() for i in pg.event.get() if i.type == pg.QUIT]
    #         pg.display.set_caption(str(self.clock.get_fps()))
    #         pg.display.flip()
    #         self.clock.tick(self.FPS)
    def run(self):
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    self.handle_key_press(event)  # Handle individual key press events
                
            if not self.paused:  # Only update game state if not paused
                self.update_camera()  # Continuous camera updates based on key states
                self.draw()
                pg.display.set_caption(str(self.clock.get_fps()))
                pg.display.flip()
                self.clock.tick(self.FPS)
        
        pg.quit()  # Clean up and close the application properly

            

    def update_camera(self):
        # Get the current state of all keys
        keys = pg.key.get_pressed()
        
        # Define movement speed and rotation speed
        move_speed = 0.1  # adjust as needed
        rotation_speed = 0.05  # adjust as needed
        
        # Adjust the camera's position based on key presses
        if keys[pg.K_w]:  # Move forward
            self.camera.position += self.camera.forward * move_speed
        if keys[pg.K_s]:  # Move backward
            self.camera.position -= self.camera.forward * move_speed
        if keys[pg.K_a]:  # Strafe left
            self.camera.position -= self.camera.right * move_speed
        if keys[pg.K_d]:  # Strafe right
            self.camera.position += self.camera.right * move_speed

        # Adjust the camera's yaw based on left or right arrow keys
        if keys[pg.K_LEFT]:
            self.camera.yaw -= rotation_speed
            self.camera.update_vectors()  # Update forward, right, up vectors based on the new yaw
        if keys[pg.K_RIGHT]:
            self.camera.yaw += rotation_speed
            self.camera.update_vectors()

        # Make sure to update the camera's matrix after changing position or orientation
        # This line assumes you have a method to update the camera matrix based on the current position and orientation
        self.camera.update_vectors()


    def handle_key_press(self, event):
    # Check for specific keys and perform actions
        if event.key == pg.K_ESCAPE:
            # Example: Quit the game when the ESC key is pressed
            self.running = False
        elif event.key == pg.K_f:
            # Example: Toggle fullscreen mode
            pg.display.toggle_fullscreen()
        elif event.key == pg.K_p:
            # Example: Pause the game
            self.paused = not self.paused  # Toggle pause state
        # Add more key bindings as needed


    # this checks if the application is closed

if __name__ == '__main__': 
    app = SoftwareRender()
    app.run()            

