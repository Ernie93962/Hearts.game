import random

CLUBS_2 = 14
SUITE_SPADES = 0
SUITE_CLUBS = 1
SUITE_HEARTS = 2
SUITE_DIAMONDS = 3

deck = []

def getTrickSuite(currentHand):
    if len(currentHand) > 0:
        return(getSuite(currentHand[0][1]))
    return(None)

def getSuite(card):
    if card>=1 and card<=13:
        return(SUITE_SPADES)
    if card>=14 and card<=26:
        return(SUITE_CLUBS)
    if card>=27 and card<=39:
        return(SUITE_HEARTS)
    if card>=40 and card<=52:
        return(SUITE_DIAMONDS)
    else:
        print('NICE TRY, CHEATER.')
        exit()

def getCardString(card):
    tempCard = card
    suite = getSuite(card)
    string = None
    if suite==SUITE_HEARTS:
        string = '\u2665'
        tempCard -= 26
    elif suite==SUITE_CLUBS:
        string = '\u2663'
        tempCard -= 13
    elif suite==SUITE_SPADES:
        string = '\u2660'
    elif suite==SUITE_DIAMONDS:
        string = '\u2666'
        tempCard -= 39
    else:
        print('NICE TRY, CHEATER!')
        exit()

    if tempCard>0 and tempCard<10:
        string = str(tempCard+1)+string
    elif tempCard == 10:
        string = 'J' + string
    elif tempCard == 11:
        string = 'Q' + string
    elif tempCard == 12:
        string = 'K' + string
    elif tempCard == 13:
        string = 'A' + string
    return(string+' ')

def convertHumanCard(card):
    suite = card[0].upper()
    value = card[1:].upper()
    cardNumber = 0
    if( suite == 'C'):
        cardNumber = 13
    elif( suite == 'H'):
        cardNumber = 26
    elif( suite == 'D'):
        cardNumber = 39

    if( value == 'J'):
        cardNumber += 10
    elif( value == 'Q'):
        cardNumber += 11
    elif( value == 'K'):
        cardNumber += 12
    elif( value == 'A'):
        cardNumber += 13
    else:
        cardNumber += int(value)-1
    return cardNumber

def printCards(cards):
    debugString = ''
    a = list(map(getCardString,cards))
    print(debugString.join(a))   

def getHighestCards(player, cardNumber):
    highCards = []
    for i in range(13, 0, -1):
        if i in player:
            highCards.append(i)
        if (i + 13) in player:
            highCards.append(i + 13)
        if (i + 26) in player:
            highCards.append(i + 26)
        if (i + 39) in player:
            highCards.append(i + 39)

    if len(highCards) >= cardNumber:
        return(highCards[:cardNumber])

def getHumanPassCards(player, cardNumber):
    highCards = []
    for p in range(0,3):
        print("Your hand is: ")
        printCards(player)
        while True:
            humanCard1 = input('Please pass a card: ')
            if len(humanCard1) < 2:
                continue
            if convertHumanCard(humanCard1) in player:
                highCards.append(convertHumanCard(humanCard1))
                break
        player.remove(convertHumanCard(humanCard1))

    if len(highCards) >= cardNumber:
        return(highCards[:cardNumber])


def getLowestCards(currentHand):
    lowestCard = 52
    for trick in currentHand:
        if trick[1] < lowestCard and getSuite(trick[1]) == getTrickSuite(currentHand):
            lowestCard = trick[1]
    return(lowestCard)
    
def passCards(players, human):
    highCards = []
    for index,player in enumerate(players):
        highCards.append(getHighestCards(player, 3))
        if index == 3:
            getHumanPassCards(player, 3)
        if index != 3 or human == 5:
            for card in highCards[index]:
                player.remove(card)
    players[1] += highCards[0]
    players[2] += highCards[1]
    players[3] += highCards[2]
    players[0] += highCards[3]
    players[3].sort()

def deal(players):
    for index,card in enumerate(deck):
        players[index%4].append(card)
    for player in players:
        player.sort()

def initalizeDeck():
    for x in range(1, 53):
        deck.append(x)

def shuffleDeck(amount=1):
    for i in range(0,amount):
        shuffle()

def shuffle():
    global deck
    half1=deck[:26]
    half2=deck[26:]
    half1Count = len(half1)
    half2Count = len(half2)
    deck.clear()
    i=0
    while(half1Count > 0 or half2Count > 0):
        selectCount = random.randrange(0,12)
        if i%2 and half1Count > 0:
            start = 26 - half1Count
            deck = deck + half1[start:start+selectCount]
            half1Count = half1Count - selectCount
        elif half2Count > 0:
            start = 26 - half2Count
            deck = deck + half2[start:start+selectCount]
            half2Count = half2Count - selectCount
        i=i+1