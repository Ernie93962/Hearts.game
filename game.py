# Simple pygame program

# Import and initialize the pygame library
import pygame
import hearts
from pygame.constants import K_ESCAPE

keyReady = True
posx = 500+20
posy = 520+20

def getCardImageLocation(idx):
    if idx >= 1 and idx <= 13:
        row = 3
        offset = idx-1
    elif idx >= 14 and idx <= 26:
         row = 0
         offset = idx-13-1
    elif idx >= 27 and idx <= 39:
        row = 2
        offset = idx-26-1
    elif idx >= 40 and idx <= 52:
        row = 1
        offset = idx-39-1
    offset += 1
    if offset > 12:
        offset = 0
    return(row, offset)

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
#screen = pygame.display.set_mode([800, 700])

my_image = pygame.image.load('cards.png').convert()

# Run until the user asks to quit
running = True
deal = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[K_ESCAPE] == True:
                running = False
        if event.type == pygame.QUIT:
            running = False
  
    trick_locationx = 600
    trick_locationy = 350
    '''screen.blit( my_image, (trick_locationx, trick_locationy), (98.4*2, 153*3, 99, 153) )
    screen.blit( my_image, (trick_locationx + 80, trick_locationy), (98.4*2, 153*3, 99, 153) )
    screen.blit( my_image, (trick_locationx + 30, trick_locationy - 40), (98.4*2, 153*3, 99, 153) )
    screen.blit( my_image, (trick_locationx + 50, trick_locationy + 30), (98.4*2, 153*3, 99, 153) )'''

    # Flip the display
    pygame.display.flip()
    screen.fill((0,0,0))
    if deal:
        hearts.main()
        deal = False
    playerHands = hearts.getPlayerHands()

    for i in range(13):
        screen.blit( my_image, (500+(20*i), 50), (98.4*2, 153*4, 99, 153) )
        #screen.blit( my_image, (500+(20*i), 600), (98.4*2, 153*4, 99, 153) )
        screen.blit( my_image, (1000, 200+(20*i)), (98.4*2, 153*4, 99, 153) )
        screen.blit( my_image, (300, 200+(20*i)), (98.4*2, 153*4, 99, 153) )

    for i in range(len(playerHands[0])):
        '''if posy > 800:
        posx = 500
        posy = 520'''
        posx = 500+(20*i)
        posy = posx + 20
        row,offset = getCardImageLocation(playerHands[0][i])
        screen.blit( my_image, (500+(20*i), 600), (98.4*offset, 153*row, 99, 153) )
        #print(pygame.mouse.get_pos())
        if keyReady:
            if pygame.mouse.get_pos()[0] >= posx and pygame.mouse.get_pos()[0] <= posy:
                if pygame.mouse.get_pos()[1] >= 600 and pygame.mouse.get_pos()[1] <= 753:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        playerHands[0].remove(playerHands[0][i])
                        print(i)
                        keyReady = False
                        break
        if event.type == pygame.MOUSEBUTTONUP:
            keyReady = True
        posx += 20
        posy += 20


# Done! Time to quit.
pygame.quit()