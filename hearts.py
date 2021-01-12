#1=2 13=ace
#spades 1-13
#clubs 14-26
#hearts 27-39
#diamonds 40-52
#queen of spades = 11
import random

CLUBS_2 = 14
SUITE_SPADES = 0
SUITE_CLUBS = 1
SUITE_HEARTS = 2
SUITE_DIAMONDS = 3

deck = []
player0=[]
player1=[]
player2=[]
player3=[]
players=[player0, player1, player2, player3]
currentHand=[]
trickPile0 = []
trickPile1 = []
trickPile2 = []
trickPile3 = []
trickPiles = [trickPile0,trickPile1,trickPile2,trickPile3]
scores = []
playerNames = ['Jim', 'Doug', 'Bob']
human = 3

def printCards(cards):
    debugString = ''
    for card in cards:
        txt = getCardString(card)
        debugString += txt+' '
    print(debugString)   

def printCurrentHand(aHand):
    debugString = ''
    for cardPair in aHand:
        txt = playerNames[cardPair[0]]+":"+getCardString(cardPair[1])
        debugString += txt+' '
    print(debugString)  

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
    return(string)

def findScore():
    for index,pile in enumerate(trickPiles):
        scores.append(0)
        for card in pile:
            if SUITE_HEARTS == getSuite(card):
                scores[index] += 1
            elif(card==11):
                scores[index] += 13


def takeTrick(winner,hand):
    for card in hand:
        trickPiles[winner].append(card[1])

def findTrickWinner(hand):
    theSuite = getSuite(hand[0][1])
    leader = hand[0]
    for card in hand:
        if theSuite==getSuite(card[1]):
            if card[1]>leader[1]:
                leader = card
    return(leader)

def humanPlayCard(player,isFirstcard=False):
    print("Your hand is: ")
    printCards(player)
    print("Current Trick is:")
    printCurrentHand(currentHand) 
    validCards = []
    if len(currentHand) > 0:
        leaderSuite = getSuite(currentHand[0][1])
        validCards = getCardsBySuite(player,leaderSuite)
    while True:  
        humanCard = input('Play card: ')
        humanCard = convertHumanCard(humanCard)
        if isFirstcard:
            if humanCard == 14:
                break
        elif len(validCards) > 0:
            if humanCard in validCards:
                break
        else:
            break
    player.remove(humanCard)
    return(humanCard)

def playCard(player,isFirstCard=False):
    if isFirstCard:
        player.remove(CLUBS_2)
        return(CLUBS_2)
    elif(len(currentHand)>0):
        handSuite=getSuite(currentHand[0][1])
        suiteCards=getCardsBySuite(player,handSuite)
        if len(suiteCards)==0:
            #testing - just use the first card in their hand
            return(player.pop(0))
        else:
            #testing - just use the first found card in the suite
            player.remove(suiteCards[0])
            return(suiteCards[0])
    else:
        #testing - just use the first card in their hand
        return(player.pop(0))

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

def getCardsBySuite(player,handSuite):
    cards=[]
    for card in player:
        if handSuite == getSuite(card):
            cards.append(card)
    return(cards)

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

def getFirstPlayer():
    for index,player in enumerate(players):
        if CLUBS_2 in player:
            return(index)
def deal():
    for index,card in enumerate(deck):
        players[index%4].append(card)
    for player in players:
        player.sort()

def initalizeDeck():
    for x in range(1, 53):
        deck.append(x)

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
        
def shuffleDeck(amount=1):
    for i in range(0,amount):
        shuffle()

def main():
    random.seed()
    name = input('Please enter your name: ')
    playerNames.append(name)

    initalizeDeck()
    shuffleDeck(1000)
    deal()
    aPlayer = getFirstPlayer()
    debugString = ''
    for card in players[aPlayer]:
        txt = getCardString(card)
        debugString += txt+' '
    #print(debugString)
    playedCard = None
    isFirstPlayer = True
    for round in range(0,13):
        for trick in range(0,4):
            if aPlayer == human:
                playedCard = humanPlayCard(players[aPlayer],isFirstPlayer)
            else:
                playedCard = playCard(players[aPlayer],isFirstPlayer)
            currentHand.append([aPlayer,playedCard])
            aPlayer=(aPlayer+1)%4
            isFirstPlayer = False
        trickWinner = findTrickWinner(currentHand)
        print("Then trick winner is: " + playerNames[trickWinner[0]] + ' [' + playerNames[currentHand[0][0]] + ':' + getCardString(currentHand[0][1]) + ', ' + playerNames[currentHand[1][0]] + ':' + getCardString(currentHand[1][1]) + ', ' + playerNames[currentHand[2][0]] + ':' + getCardString(currentHand[2][1]) + ', ' + playerNames[currentHand[3][0]] + ':' + getCardString(currentHand[3][1]) + ']')
        takeTrick(trickWinner[0],currentHand)
        currentHand.clear()
        aPlayer = trickWinner[0]
    findScore()
    winner = 0
    winnerScore = 26
    for index,score in enumerate(scores):
        print(playerNames[index]+': '+str(scores[index]))
        if scores[index] < winnerScore:
            winnerScore = scores[index]
            winner = index
    print('The winner is: ' + playerNames[winner])

if __name__ == "__main__":
    main()