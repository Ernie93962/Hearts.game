# Simple pygame program

# Import and initialize the pygame library
import pygame
import hearts
from pygame.constants import K_ESCAPE

CARD_WIDTH = 98.4
ROW_HEIGTH = 153

allowButton = True
cardx = 0
cardy = 0
humanPlayedCard = False
aPlayer = 0

# X,Y locations of player hands
#TODO - add veritcal/hoizontal info to this array
DeckLocations = [ 
                 [300,200],
                 [500,50],
                 [1000,200],
                 [500,600]
                ]

#Get index of the Human player card based on screen position
def getCardIndexFromScreenCoord(mousePos):
    x = mousePos[0]
    y = mousePos[1]

    if x > 500 and x < 760:
        if y > 600 and y < 763:
            return int(( x - 500 ) / 20)

#Get the card location for the main PNG
#Return - Row and index the card is in card coordinates, not screen coordinates!
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

#Draws a players hand at given X,Y location
# handX - X coordinate
# handY - Y coordinate
# hand - list of cards in the hand to be drawn
# hoz - true if hand is drawn in the horizontal direction, false it is drawn vertically
def drawPlayerHand(handX,handY, hand, hoz=True):
    for i in range(len(hand)):
            X = handX+(20*i) if hoz == True else handX
            Y = handY+(20*i) if hoz == False else handY

            row,offset = getCardImageLocation(hand[i])
            pngCol = CARD_WIDTH * offset
            pngRow = ROW_HEIGTH * row
            screen.blit( my_image, (X, Y), (pngCol, pngRow, CARD_WIDTH, ROW_HEIGTH) )

pygame.init()

# Set up the drawing window
#screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
screen = pygame.display.set_mode([1500, 700])

#Get the main PNG that contiains all the card images 
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

    #Deal the cards just Once per game
    #TODO Find a way to restart a game after one game is done
    if deal:
        needHumanInput = hearts.procGame(True)
        deal = False
    else:
        needHumanInput = hearts.procGame(False)

    #Loop over all the player Hands and draw there hands
    #TODO Don't show the other players cards, just the back of the cards!
    for i, player in enumerate(hearts.getPlayerHands()):  
        drawPlayerHand(DeckLocations[i][0], DeckLocations[i][1], player, i != 0 and i != 2)
    
    #Detect Mouse Button and act if input is needed and previous input is done
    if event.type == pygame.MOUSEBUTTONDOWN and needHumanInput and allowButton:
        idx = getCardIndexFromScreenCoord(pygame.mouse.get_pos())
        if None != idx:
            hearts.UIplayCard(idx)
            needHumanInput = False
            allowButton = False

    if event.type == pygame.MOUSEBUTTONUP:
        allowButton = True

    #Get the cards in the current Trick and draw them in the center
    #TODO Make sure the lead card is always on top so player can see the suite
    #TODO Animate these to the center
    Tricks = hearts.getCurrentTrick()
    for aTrick in Tricks:
        if aTrick[0] == 0:
            x, y = getCardImageLocation(aTrick[1])
            screen.blit( my_image, (trick_locationx, trick_locationy), (CARD_WIDTH*y, 153*x, 99, 153) )
        elif aTrick[0] == 1:
            x, y = getCardImageLocation(aTrick[1])
            screen.blit( my_image, (trick_locationx + 80, trick_locationy), (CARD_WIDTH*y, 153*x, 99, 153) )
        elif aTrick[0] == 2:
            x, y = getCardImageLocation(aTrick[1])
            screen.blit( my_image, (trick_locationx + 30, trick_locationy - 40), (CARD_WIDTH*y, 153*x, 99, 153) )
        elif aTrick[0] == 3:
            x, y = getCardImageLocation(aTrick[1])
            screen.blit( my_image, (trick_locationx + 50, trick_locationy + 30), (CARD_WIDTH*y, 153*x, 99, 153) )
        
# Done! Time to quit.
pygame.quit()