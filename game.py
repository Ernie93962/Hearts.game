# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])
my_image = pygame.image.load('cards.png').convert()

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    surf = pygame.Surface((500, 500))

    # Fill the background with white
    surf.fill((255, 255, 255))
    screen.blit( my_image, (50, 50), (99, 153, 99, 153) )

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()