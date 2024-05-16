import pygame
from pygame.locals import *
import clips

# Create a CLIPS environment
env = clips.Environment()

env.load("rubik.clp")

env.reset()

facts = env.facts()

# Define the colors for each face (assuming RGB values)
FACE_COLORS = {
    'w': (255, 255, 255),  # White
    'r': (255, 0, 0),      # Red
    'b': (0, 0, 255),      # Blue
    'g': (0, 255, 0),      # Green
    'o': (255, 165, 0),    # Orange
    'y': (255, 255, 0)     # Yellow
}

FACES ={
    'up':0,
    'left':1,
    'front':2,
    'right':3,
    'back':4,
    'down':5
}
# Dimensions and positions for each cubelet
CUBELET_SIZE = 50
CUBELET_GAP = 10

# Window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 720



menu_height = 100
# Draw the button
button_width = 100
button_height = 40
button_x = WINDOW_WIDTH - (2 * button_width)
button_y = WINDOW_HEIGHT - menu_height + (menu_height - button_height) // 2

class RubiksCube:
    DISPLAYED_MESSAGE="The rubiks cube isn't solved"

    def __init__(self):
        # Initialize the cube with default colors
        self.cube = [[[ 'w' for _ in range(3)] for _ in range(3)] for _ in range(6)]

    def set_face(self, face_string, face_index):
        # Validate the face index
        if face_index < 0 or face_index >= 6:
            print("Invalid face index.")
            return

        # Validate the face string length
        if len(face_string) != 9:
            print("Invalid face string length.")
            return

        # Update the cube with the provided face string
        for i in range(9):
            row = i // 3
            col = i % 3
            self.cube[face_index][row][col] = face_string[i]

    def display_cube(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_x <= mouse[0] <= button_x+button_width and button_y <= mouse[1] <= button_y+button_height:
                        self.handle_button_click()
                        #self.draw_cube(screen)

            screen.fill((0, 0, 0))  # Clear the screen
            mouse = pygame.mouse.get_pos()
            # Draw the Rubik's Cube
            self.draw_cube(screen)

            # Draw the bottom menu
            self.draw_bottom_menu(screen)

            pygame.display.flip()
            clock.tick(60)

    def draw_cube(self, screen):
        cube_width = 3 * CUBELET_SIZE + 2 * CUBELET_GAP
        cube_height = 3 * CUBELET_SIZE + 2 * CUBELET_GAP
        cube_x = cube_width // 2  + cube_width+2 * CUBELET_GAP
        cube_y = cube_height // 2 -2 * CUBELET_GAP

        # Draw the border around the cube
        border_width = 4
        border_color = (0, 0, 0)
        pygame.draw.rect(screen, border_color, (cube_x - border_width, cube_y - border_width, cube_width + 2 * border_width, cube_height + 2 * border_width))

        for face_index in range(6):
            for row in range(3):
                for col in range(3):
                    cubelet_x = cube_x + col * (CUBELET_SIZE + CUBELET_GAP)
                    cubelet_y = cube_y + row * (CUBELET_SIZE + CUBELET_GAP)

                    color = FACE_COLORS[self.cube[face_index][row][col]]
                    pygame.draw.rect(screen, color, (cubelet_x, cubelet_y, CUBELET_SIZE, CUBELET_SIZE))

            if face_index == 0:
                cube_x = cube_width //2 - cube_width- 2 * CUBELET_GAP
                cube_y = cube_height // 2 + cube_height
            if face_index == 4:
                cube_x = cube_x = cube_width // 2  + cube_width+2 * CUBELET_GAP
                cube_y = cube_height // 2 + 2*cube_height + 20
            else:
                cube_x += cube_width + 20

    def draw_bottom_menu(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), (0, WINDOW_HEIGHT - menu_height, WINDOW_WIDTH, menu_height))

        # Draw the message box
        message_box_width = 300
        message_box_height = 40
        message_box_x = (message_box_width) // 2
        message_box_y = WINDOW_HEIGHT - menu_height + (menu_height - message_box_height) // 2

        pygame.draw.rect(screen, (255, 255, 255), (message_box_x, message_box_y, message_box_width, message_box_height))

        # Draw the message in the message box
        font = pygame.font.Font(None, 24)
        message = self.DISPLAYED_MESSAGE
        message_text = font.render(message, True, (0, 0, 0))
        message_text_rect = message_text.get_rect(center=(message_box_x + message_box_width // 2, message_box_y + message_box_height // 2))
        screen.blit(message_text, message_text_rect)

        #draw step button
        pygame.draw.rect(screen, (100, 100, 100), (button_x, button_y, button_width, button_height))

        # Draw the button label
        font = pygame.font.Font(None, 24)
        label = font.render("Next Step", True, (255, 255, 255))
        label_rect = label.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(label, label_rect)
    
    def handle_button_click(self):
        env.run(1)
        self.set_faces()
    
    def set_faces(self):
        facts = env.facts()
        for fact in facts:
            if len(fact)>0 and fact[0] in FACES:
                colors = ""
                for i in range(1,len(fact)):
                    colors+=fact[i]
                if str(fact[0]) == 'back':
                    colors=colors[::-1]
                self.set_face(colors, FACES[fact[0]])
            else:
                self.DISPLAYED_MESSAGE = str(fact)
            print(fact) 
     
cube = RubiksCube()

cube.display_cube()