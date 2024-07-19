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

    def create_objects(self):
        self.camera = Camera(self, [-5, 500, -500])
        # self.camera = Camera(self , [0.5, 1, -4])
        self.projection = Projection(self)
        self.object = self.get_object_from_file('resources/t_34_obj1.obj')
        # self.object = Object3D(self)
        self.object.translate([0.2, 0.4, 0.2])

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


    def handle_mouse_motion(self, event):
        self.camera.control_mouse(event)



    # def update_camera(self):
    #     # Get the current state of all keys
    #     keys = pg.key.get_pressed()
        
    #     # Define movement speed and rotation speed
    #     move_speed = 0.1  # adjust as needed
    #     rotation_speed = 0.05  # adjust as needed
    
    #     self.camera.update_vectors()
    def update_camera(self):
        self.camera.update_vectors()


    def handle_key_press(self, event):
        if event.key == pg.K_ESCAPE:
            self.running = False
        elif event.key == pg.K_f:
            pg.display.toggle_fullscreen()
        elif event.key == pg.K_p:
            self.paused = not self.paused

    # this checks if the application is closed
    # def run(self):
    #     self.running = True
    #     while self.running:
    #         for event in pg.event.get():
    #             if event.type == pg.QUIT:
    #                 self.running = False
    #             elif event.type == pg.KEYDOWN:
    #                 self.handle_key_press(event)  # Handle individual key press events
            
    #         self.draw()
    #         self.camera.control()
    #         self.update_camera()  # Continuous camera updates based on key states
    #         pg.display.set_caption(str(self.clock.get_fps()))
    #         pg.display.flip()
    #         self.clock.tick(self.FPS)
                
    #         if not self.paused:  # Only update game state if not paused
    #             self.update_camera()  # Continuous camera updates based on key states
    #             self.draw()
    #             self.camera.control()
    #             pg.display.set_caption(str(self.clock.get_fps()))
    #             pg.display.flip()
    #             self.clock.tick(self.FPS)
        
    #     pg.quit()  # Clean up and close the application properly

    def handle_movement(self):
        key = pg.key.get_pressed()

        movement_delta = np.array([0.0, 0.0, 0.0])

        if key[pg.K_a]:
            print("A key pressed")
            movement_delta -= self.camera.right * self.camera.moving_speed
        if key[pg.K_d]:
            print("D key pressed")
            movement_delta += self.camera.right * self.camera.moving_speed
        if key[pg.K_w]:
            print("W key pressed")
            movement_delta += self.camera.forward * self.camera.moving_speed
        if key[pg.K_s]:
            print("S key pressed")
            movement_delta -= self.camera.forward * self.camera.moving_speed
        if key[pg.K_SPACE]:
            print("SPACE key pressed")
            movement_delta += np.array([0, 1, 0]) * self.camera.moving_speed
        if key[pg.K_LSHIFT]:
            print("LSHIFT key pressed")
            movement_delta -= np.array([0, 1, 0]) * self.camera.moving_speed

        # Debugging: Print movement delta and position updates
        print(f"Movement delta: {movement_delta}")
        self.camera.position += movement_delta
        print(f"Position after update: {self.camera.position}")

    def run(self):
        self.running = True
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)  # Grabs the mouse to the window
        
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    self.handle_key_press(event)
                elif event.type == pg.MOUSEMOTION:
                    self.handle_mouse_motion(event)
            
            
            self.handle_movement()
            self.update_camera()
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)
            
            if not self.paused:
                self.update_camera()
                self.draw()
                self.handle_movement()
                pg.display.set_caption(str(self.clock.get_fps()))
                pg.display.flip()
                self.clock.tick(self.FPS)
        
        pg.quit()


## testing that the buttons are being pressed



if __name__ == '__main__': 
    app = SoftwareRender()
    app.run()            

