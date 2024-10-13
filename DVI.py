from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import sys

class WavefrontOBJ:
    def __init__(self, filename):
        self.vertices = []  # List of vertices
        self.faces = []  # List of faces
        self.groups = {}  # Dictionary of groups and their faces
        self.current_group = None  # Current group being loaded
        self.load(filename)

    def load(self, filename):
        """
        Loads an Wavefront OBJ file and stores its data.
        """
        with open(filename, 'r') as file:
            lines = file.readlines()

            for line in lines:
                parts = line.split()

                if not parts:
                    continue

                keyword = parts[0]

                if keyword == 'v':
                    # Vertex
                    vertex = list(map(float, parts[1:4]))
                    self.vertices.append(vertex)

                elif keyword == 'f':
                    # Face
                    face = [int(vertex.split('/')[0]) for vertex in parts[1:]]
                    self.faces.append(face)

                    # Add face to current group if any
                    if self.current_group:
                        self.groups[self.current_group].append(face)

                elif keyword == 'g':
                    # Group
                    group_name = parts[1]
                    self.current_group = group_name
                    if group_name not in self.groups:
                        self.groups[group_name] = []

    def list_objects(self):
        """
        Prints the names of all groups in the object.
        """
        print("Objects in the file:")
        for group_name in self.groups.keys():
            print(group_name)

    def calculate_object_center(self, object_name):
        sum_x, sum_y, sum_z = 0, 0, 0
        count = 0
        for face in self.groups[object_name]:
            for vertex_index in face:
                vertex = self.vertices[vertex_index - 1]
                sum_x += vertex[0]
                sum_y += vertex[1]
                sum_z += vertex[2]
                count += 1
        return sum_x / count, sum_y / count, sum_z / count

    def display_object(self, object_name, display_mode):
        """
        Displays the specified object in the given mode.
        """
        if object_name not in self.groups:
            print(f"Error: Object '{object_name}' not found.")
            return

        print(f"Displaying object '{object_name}' in {display_mode} mode:")

        # Initialize pygame and setup OpenGL display
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        #glTranslatef(0.0, -0.2, -5)

        # Centering the object
        object_center = self.calculate_object_center(object_name)
        glTranslatef(-object_center[0], -object_center[1], -object_center[2] - 5)

        # Main loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Clear the screen and set the display mode
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            if display_mode == "Points":
                glPointSize(5.0)
                glBegin(GL_POINTS)
            elif display_mode == "Wireframe":
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                glBegin(GL_TRIANGLES)
            elif display_mode == "Solid":
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                glBegin(GL_TRIANGLES)

            glBegin(GL_TRIANGLES)
            for face in self.groups[object_name]:
                for vertex_index in face:
                    glVertex3fv(self.vertices[vertex_index - 1])
            #glEnd()

            # Update the display and handle timing
            pygame.display.flip()
            pygame.time.wait(10)

    def setup_lighting(self):
        """
        Sets up basic lighting for the object.
        """
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_DIFFUSE)

    def save_object(self, object_name, filename):
        """
        Saves the specified object to a new OBJ file.
        """
        if object_name not in self.groups:
            print(f"Error: Object '{object_name}' not found.")
            return

        try:
            with open(filename, 'w') as file:
                file.write(f"# Saved from {object_name}\n")
                file.write(f"g {object_name}\n")

                for vertex in self.vertices:
                    file.write(f"v {' '.join(map(str, vertex))}\n")

                for face in self.groups[object_name]:
                    file.write(f"f {' '.join(map(str, face))}\n")
            print(f"Object '{object_name}' saved to {filename}")
        except Exception as e:
            print(f"Error saving object '{object_name}': {e}")

if __name__ == "__main__":
    obj_file = "C:\\Users\\emy7u\\Downloads\\Objets3D.obj"
    wavefront_obj = WavefrontOBJ(obj_file)
    wavefront_obj.list_objects()

    # Prompt the user to choose the object
    object_choices = {
        "1": "Urn",
        "2": "Budvase",
        "3": "Bowl",
        "4": "Bottle",
        "5": "Amphora",
    }
    object_number = input("Choose the object (1: Urn, 2: Budvase, 3: Bowl, 4: Bottle, 5: Amphora): ")
    object_name = object_choices.get(object_number)

    if not object_name:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    # Save the object to a new .obj file
    new_obj_file = "output.obj"
    wavefront_obj.save_object(object_name, new_obj_file)

    # Prompt the user to choose the display mode
    display_mode_choices = {
        "1": "Points",
        "2": "Wireframe",
        "3": "Solid",
    }
    display_mode_number = input("Choose the display mode (1: Points, 2: Wireframe, 3: Solid): ")
    display_mode = display_mode_choices.get(display_mode_number)

    if not display_mode:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    # Display the chosen object in the selected display mode
    wavefront_obj.display_object(object_name, display_mode)

