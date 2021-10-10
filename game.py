# Simple pygame program

# Import and initialize the pygame library
import pygame
import hearts
from pygame.constants import K_ESCAPE

keyReady = True
cardx = 0
cardy = 0
humanPlayedCard = False
aPlayer = 0
playerHands = []

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
#screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
screen = pygame.display.set_mode([1500, 700])

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
    # Flip the display
    pygame.display.flip()
    screen.fill((0,0,0))

    #deal is done once per game
    if deal:
        hearts.initializeGame()
        deal = False
        aPlayer = hearts.getFirstPlayer()
        if aPlayer == hearts.human:
           playerHands = hearts.getPlayerHands()
        cardPlayed = hearts.procGame(aPlayer, True)
    else:
        cardPlayed = hearts.procGame(aPlayer, False)
    
    if aPlayer == hearts.human:
        # wait for human to play card
        # increment player index by 1
        if humanPlayedCard:
            humanPlayedCard = False
            print(aPlayer)
            aPlayer = 0
    else:
        print(aPlayer)
        playerHands = hearts.getPlayerHands()
        aPlayer += 1

    # draws players hands    
    for i in range(len(playerHands[0])):
        pos1 = 500+(20*i)
        pos2 = pos1 + 20
        row,offset = getCardImageLocation(playerHands[0][i])
        screen.blit( my_image, (300, 200+(20*i)), (98.4*offset, 153*row, 99, 153) )
    
    for i in range(len(playerHands[2])):
        pos1 = 500+(20*i)
        pos2 = pos1 + 20
        row,offset = getCardImageLocation(playerHands[2][i])
        screen.blit( my_image, (1000, 200+(20*i)), (98.4*offset, 153*row, 99, 153) )
    
    for i in range(len(playerHands[1])):
        pos1 = 500+(20*i)
        pos2 = pos1 + 20
        row,offset = getCardImageLocation(playerHands[1][i])
        screen.blit( my_image, (500+(20*i), 50), (98.4*offset, 153*row, 99, 153) )

    # draws our hand    
    for i in range(len(playerHands[3])):
        pos1 = 500+(20*i)
        pos2 = pos1 + 20
        row,offset = getCardImageLocation(playerHands[3][i])
        screen.blit( my_image, (500+(20*i), 600), (98.4*offset, 153*row, 99, 153) )
            #print(pygame.mouse.get_pos())
        if keyReady:
            if pygame.mouse.get_pos()[0] >= pos1 and pygame.mouse.get_pos()[0] <= pos2:
                if pygame.mouse.get_pos()[1] >= 600 and pygame.mouse.get_pos()[1] <= 753:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        cardx,cardy = getCardImageLocation(playerHands[0][i])
                        keyReady = False
                        humanPlayedCard = True
                        #TODO: remove card from human hand, put the card in the center
                            #1. which card was clicked?
                            #2. remove card from hand
                            #3. put card in center
                        break
        if event.type == pygame.MOUSEBUTTONUP:
            keyReady = True

    #center cards
    '''screen.blit( my_image, (trick_locationx, trick_locationy), (98.4*2, 153*3, 99, 153) )
    screen.blit( my_image, (trick_locationx + 80, trick_locationy), (98.4*2, 153*3, 99, 153) )
    screen.blit( my_image, (trick_locationx + 30, trick_locationy - 40), (98.4*2, 153*3, 99, 153) )'''
    screen.blit( my_image, (trick_locationx + 50, trick_locationy + 30), (98.4*cardy, 153*cardx, 99, 153) )

# Done! Time to quit.
pygame.quit()