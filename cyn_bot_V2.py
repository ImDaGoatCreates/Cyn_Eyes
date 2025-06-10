#I worte and used this code in Visual Studio Code, or VS Code. I am unsure whether it will work elsewhere, so keep that in mind.
#Copy the image path for the puppy eyes expression, paste it in your browser, download the image, name it "puppy.jpg", and put it in the same folder as the .py file.
#Do the same thing as the puppy expression, but save the image as "center_image.jpg" instead.
#The program will be full-screen, so to end the program, click on the PyGame window and hit ALT + F4

import pygame
import tkinter as tk
import random
import urllib.request
import os

# Constants
SOLVER_IMAGE_PATH = "center_image.jpg"
PUPPY_IMAGE_PATH = "puppy.jpg"

if not os.path.exists(PUPPY_IMAGE_PATH):
    url = "https://th.bing.com/th/id/OIP.v5ma-JlCh47YfZ61p5mYSgAAAA?rs=1&pid=ImgDetMain"
    urllib.request.urlretrieve(url, PUPPY_IMAGE_PATH)

if not os.path.exists(SOLVER_IMAGE_PATH):
    url = "https://i.quotev.com/g76gnudmst2q.jpg"
    urllib.request.urlretrieve(url, SOLVER_IMAGE_PATH)

# Pygame setup
pygame.init()
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
running = True

# Eye properties
eye_width = screen_width / 3.75
eye_height = (screen_height / 5) * 4
eye_spacing = (screen_width / 6) * 2
initialX = (screen.get_width() - (eye_width * 2 + eye_spacing)) / 2
secondX = initialX + eye_width + eye_spacing
eye_y = (screen.get_height() - eye_height) / 2

# Blinking variables
open_time = random.randint(7500, 12500)
close_time = 350
last_state_change_time = pygame.time.get_ticks()
current_state = 'open'
blink_speed = 45
eye_current_height = eye_height
eye_top_y = eye_y
eye_bottom_y = eye_y + eye_height

# Expression variables
scared = False
scared_start_time = 0
scared_duration = 10000

annoyed = False
annoyed_start_time = 0
annoyed_duration = 10000
last_annoyed_check = pygame.time.get_ticks()

happy = False
happy_start_time = 0
happy_duration = 10000
last_happy_check = pygame.time.get_ticks()

puppy_mode = False
puppy_start_time = 0
puppy_duration = 10000
last_puppy_check = pygame.time.get_ticks()

shocked = False
shocked_start_time = 0
shocked_duration = 10000
last_shocked_check = pygame.time.get_ticks()

center_image_mode = False
center_image_start_time = 0
center_image_duration = 10000
last_center_image_check = pygame.time.get_ticks()

# Load and scale images
puppy_image = pygame.image.load(PUPPY_IMAGE_PATH)
puppy_scaled_height = int((eye_bottom_y - eye_top_y))
puppy_image = pygame.transform.scale(puppy_image, (int(eye_width), puppy_scaled_height))
puppy_image_left = puppy_image
puppy_image_right = puppy_image

center_image = pygame.image.load(SOLVER_IMAGE_PATH)
center_image = pygame.transform.scale(center_image, (screen_width, screen_height))

# Eye movement variables
eye_move_range_x = 50  # wider horizontal movement
eye_move_range_y = 40  # wider vertical movement

eye_move_delay = 800  # ms between movements
last_eye_move_time = 0

eye_wait_time_range = (2000, 5000)
eye_waiting = False
eye_wait_start_time = 0
eye_wait_duration = 0

eye_move_sequence_length = 0
eye_move_count = 0
eye_returning = False

eye_current_offsets = [0, 0]
eye_target_offsets = [0, 0]

def get_random_eye_offset():
    return [
        random.randint(-eye_move_range_x, eye_move_range_x),
        random.randint(-eye_move_range_y, eye_move_range_y)
    ]

def trigger_annoyed():
    global annoyed, annoyed_start_time, annoyed_duration
    annoyed = True
    annoyed_start_time = pygame.time.get_ticks()
    annoyed_duration = random.randint(4000, 8000)

def trigger_happy():
    global happy, happy_start_time, happy_duration
    happy = True
    happy_start_time = pygame.time.get_ticks()
    happy_duration = random.randint(4000, 8000)

def trigger_puppy():
    global puppy_mode, puppy_start_time
    puppy_mode = True
    puppy_start_time = pygame.time.get_ticks()
    puppy_duration = random.randint(4000, 8000)

def trigger_shocked():
    global shocked, shocked_start_time
    shocked = True
    shocked_start_time = pygame.time.get_ticks()
    shocked_duration = random.randint(4000, 8000)

def trigger_center_image():
    global center_image_mode, center_image_start_time, center_image_duration
    center_image_mode = True
    center_image_start_time = pygame.time.get_ticks()
    center_image_duration = random.randint(4000, 8000)

def draw_happy_eyes():
    happy_eye_top_y = eye_y
    left_eye_rect = pygame.Rect(initialX, happy_eye_top_y, eye_width, eye_bottom_y - eye_top_y)
    right_eye_rect = pygame.Rect(secondX, happy_eye_top_y, eye_width, eye_bottom_y - eye_top_y)
    pygame.draw.ellipse(screen, "yellow", left_eye_rect)
    pygame.draw.ellipse(screen, "yellow", right_eye_rect)

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    current_time = pygame.time.get_ticks()

    # Eye movement logic
    if not eye_waiting and current_time - last_eye_move_time >= eye_move_delay:
        if eye_returning:
            eye_current_offsets = [0, 0]
            eye_returning = False
            eye_waiting = True
            eye_wait_start_time = current_time
            eye_wait_duration = random.randint(*eye_wait_time_range)
        else:
            if eye_move_count < eye_move_sequence_length:
                eye_current_offsets = get_random_eye_offset()
                eye_move_count += 1
                last_eye_move_time = current_time
            else:
                eye_returning = True
                last_eye_move_time = current_time
    elif eye_waiting and current_time - eye_wait_start_time >= eye_wait_duration:
        eye_waiting = False
        eye_move_count = 0
        eye_move_sequence_length = random.randint(2, 4)
        last_eye_move_time = current_time

    # Expression triggers
    if not shocked and current_time - last_shocked_check >= 75000:
        if random.random() < 0.15:
            trigger_shocked()
        last_shocked_check = current_time

    if current_time - last_annoyed_check >= 90000:
        if random.random() < 0.15:
            trigger_annoyed()
        last_annoyed_check = current_time

    if not annoyed and not happy and not puppy_mode and not shocked and current_time - last_happy_check >= 60000:
        if random.random() < 0.15:
            trigger_happy()
        last_happy_check = current_time

    if not annoyed and not happy and not puppy_mode and not shocked and current_time - last_puppy_check >= 45000:
        if random.random() < 0.15:
            trigger_puppy()
        last_puppy_check = current_time

    if not center_image_mode and not shocked and not puppy_mode and not annoyed and not happy and current_time - last_center_image_check >= 100000:
        if random.random() < 0.10:
            trigger_center_image()
        last_center_image_check = current_time

    # End expressions
    if shocked and current_time - shocked_start_time >= shocked_duration:
        shocked = False
    if puppy_mode and current_time - puppy_start_time >= puppy_duration:
        puppy_mode = False
    if annoyed and current_time - annoyed_start_time >= annoyed_duration:
        annoyed = False
    if happy and current_time - happy_start_time >= happy_duration:
        happy = False
        last_happy_check = current_time
    if center_image_mode and current_time - center_image_start_time >= center_image_duration:
        center_image_mode = False

    # Blinking logic
    if not shocked and not annoyed and not scared and not happy and not puppy_mode and not center_image_mode:
        if current_state == 'open' and current_time - last_state_change_time >= open_time:
            current_state = 'closing'
        elif current_state == 'closing':
            eye_current_height -= blink_speed * 2
            eye_top_y += blink_speed
            eye_bottom_y -= blink_speed
            if eye_current_height <= 0:
                eye_current_height = 0
                current_state = 'closed'
                last_state_change_time = current_time
        elif current_state == 'closed' and current_time - last_state_change_time >= close_time:
            current_state = 'opening'
        elif current_state == 'opening':
            eye_current_height += blink_speed * 2
            eye_top_y -= blink_speed
            eye_bottom_y += blink_speed
            if eye_current_height >= eye_height:
                eye_current_height = eye_height
                eye_top_y = eye_y
                eye_bottom_y = eye_y + eye_height
                current_state = 'open'
                last_state_change_time = current_time
                open_time = random.randint(15000, 25000)

    # Drawing logic
    if center_image_mode:
        screen.blit(center_image, (0, 0))

    elif shocked:
        yellow_left = pygame.Rect(initialX, eye_top_y, eye_width, eye_bottom_y - eye_top_y)
        yellow_right = pygame.Rect(secondX, eye_top_y, eye_width, eye_bottom_y - eye_top_y)
        pygame.draw.ellipse(screen, "yellow", yellow_left)
        pygame.draw.ellipse(screen, "yellow", yellow_right)
        black_margin_x = eye_width * 0.075
        black_margin_y = (eye_bottom_y - eye_top_y) * 0.05
        black_width = eye_width - 2 * black_margin_x
        black_height = (eye_bottom_y - eye_top_y) - 2 * black_margin_y
        black_left = pygame.Rect(yellow_left.x + black_margin_x, yellow_left.y + black_margin_y, black_width, black_height)
        black_right = pygame.Rect(yellow_right.x + black_margin_x, yellow_right.y + black_margin_y, black_width, black_height)
        pygame.draw.ellipse(screen, "black", black_left)
        pygame.draw.ellipse(screen, "black", black_right)

    elif happy:
        draw_happy_eyes()

    elif puppy_mode:
        screen.blit(puppy_image_left, (initialX, eye_y))
        screen.blit(puppy_image_right, (secondX, eye_y))

    else:
        left_eye_rect = pygame.Rect(
            initialX + eye_current_offsets[0],
            eye_top_y + eye_current_offsets[1],
            eye_width,
            eye_bottom_y - eye_top_y
        )
        right_eye_rect = pygame.Rect(
            secondX + eye_current_offsets[0],
            eye_top_y + eye_current_offsets[1],
            eye_width,
            eye_bottom_y - eye_top_y
        )
        pygame.draw.ellipse(screen, "yellow", left_eye_rect)
        pygame.draw.ellipse(screen, "yellow", right_eye_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
