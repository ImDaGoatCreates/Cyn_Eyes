#I worte and used this code in Visual Studio Code, or VS Code. I am unsure whether it will work elsewhere, so keep that in mind.
#THIS IS IMPORTANT, AND THE CODE WILL ONLY WORK IF YOU DO THIS PROPERLY. To run the code, type "python3 cyn_bot_V2.py" in the terminal and hit ENTER
#Type it in the terminal EXACTLY as shown otherwise it won't work. Hit ENTER to run the code.
#The program will be full-screen, so to end the program, click on the PyGame window and hit ALT + F4

import pygame
import tkinter as tk
import random

# pygame setup
pygame.init()

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

# Eye properties
eye_width = screen_width / 3.75  
eye_height = (screen_height / 5) * 4  
eye_spacing = (screen_width / 6) * 2

# Initial positions
initialX = (screen.get_width() - (eye_width * 2 + eye_spacing)) / 2
secondX = initialX + eye_width + eye_spacing
eye_y = (screen.get_height() - eye_height) / 2  # Eyes stay in place

# Blinking variables
open_time = random.randint(7500, 12500)
close_time = 350  
last_state_change_time = pygame.time.get_ticks()  
current_state = 'open'  
blink_speed = 45  
eye_current_height = eye_height  # Track current eye height for blinking
eye_top_y = eye_y  # Track top of eye position
eye_bottom_y = eye_y + eye_height  # Track bottom of eye position

# Annoyed expression variables
annoyed = False  # Start with no annoyed expression
annoyed_start_time = 0
annoyed_duration = 0
last_annoyed_check = pygame.time.get_ticks()  # To check every 60 seconds

# Function to manually trigger the annoyed expression
def trigger_annoyed():
    global annoyed, annoyed_start_time, annoyed_duration
    annoyed = True
    annoyed_start_time = pygame.time.get_ticks()
    annoyed_duration = random.randint(7000, 14000)  # 7 to 14 seconds in milliseconds

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    current_time = pygame.time.get_ticks()  

    # Check if it's time to possibly trigger the annoyed expression (15% chance every 60 seconds)
    if current_time - last_annoyed_check >= 60000:  # Every 60 seconds
        if random.random() < 0.15:  # 15% chance
            trigger_annoyed()
        last_annoyed_check = current_time  # Reset the last check time

    # Reset annoyed expression after duration
    if annoyed and current_time - annoyed_start_time >= annoyed_duration:
        annoyed = False  

    # Blinking logic (only when NOT annoyed)
    if not annoyed:
        if current_state == 'open' and current_time - last_state_change_time >= open_time:
            current_state = 'closing'
        elif current_state == 'closing':
            eye_current_height -= blink_speed * 2  # Shrink eye from both directions
            eye_top_y += blink_speed  # Move top of eye downward
            eye_bottom_y -= blink_speed  # Move bottom of eye upward
            if eye_current_height <= 0:
                eye_current_height = 0
                current_state = 'closed'
                last_state_change_time = current_time
        elif current_state == 'closed' and current_time - last_state_change_time >= close_time:
            current_state = 'opening'
        elif current_state == 'opening':
            eye_current_height += blink_speed * 2  # Open eye from both directions
            eye_top_y -= blink_speed  # Move top of eye back up
            eye_bottom_y += blink_speed  # Move bottom of eye back down
            if eye_current_height >= eye_height:
                eye_current_height = eye_height
                eye_top_y = eye_y  # Reset to original position
                eye_bottom_y = eye_y + eye_height  # Reset bottom position
                current_state = 'open'
                last_state_change_time = current_time
                open_time = random.randint(15000, 25000)  

    # Draw the eyes (blinking from both directions)
    left_eye_rect = pygame.Rect(initialX, eye_top_y, eye_width, eye_bottom_y - eye_top_y)
    right_eye_rect = pygame.Rect(secondX, eye_top_y, eye_width, eye_bottom_y - eye_top_y)
    
    pygame.draw.ellipse(screen, "yellow", left_eye_rect)
    pygame.draw.ellipse(screen, "yellow", right_eye_rect)

    # Annoyed expression overlay (lid line & black box)
    if annoyed:
        # Black box covering the upper portion of the eye
        lid_cover_height = eye_height * 0.475  # Covers the top 47.5% of the eye
        left_cover = pygame.Rect(initialX, eye_y, eye_width, lid_cover_height)
        right_cover = pygame.Rect(secondX, eye_y, eye_width, lid_cover_height)

        pygame.draw.rect(screen, "black", left_cover)
        pygame.draw.rect(screen, "black", right_cover)

        # Thin yellow eyelid line slightly wider than the eye
        lid_width = eye_width * 1.25  # Slightly wider than the eye
        lid_height = 15  
        lid_y = eye_y + lid_cover_height - 2  # Positioned near the bottom of the black cover

        left_lid = pygame.Rect(initialX - (lid_width - eye_width) / 2, lid_y, lid_width, lid_height)
        right_lid = pygame.Rect(secondX - (lid_width - eye_width) / 2, lid_y, lid_width, lid_height)

        pygame.draw.rect(screen, "yellow", left_lid)
        pygame.draw.rect(screen, "yellow", right_lid)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
