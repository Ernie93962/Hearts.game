#1=2 13=ace
#spades 1-13
#clubs 14-26
#hearts 27-39
#diamonds 40-52
#queen of spades = 11
import random
import argparse

CLUBS_2 = 14
SUITE_SPADES = 0
SUITE_CLUBS = 1
SUITE_HEARTS = 2
SUITE_DIAMONDS = 3

playHearts = False
deck = []
player0 = []
player1 = []
player2 = []
player3 = []
players = [player0, player1, player2, player3]
currentHand = []
trickPile0 = []
trickPile1 = []
trickPile2 = []
trickPile3 = []
trickPiles = [trickPile0,trickPile1,trickPile2,trickPile3]
scores = []
playerNames = ['Jim', 'Doug', 'Bob']
human = 3

def getHighestCards(player, cardNumber):
    highCards = []
    if player != player3:
        for i in range(13, 0, -1):
            if i in player:
                highCards.append(i)
            if (i + 13) in player:
                highCards.append(i + 13)
            if (i + 26) in player:
                highCards.append(i + 26)
            if (i + 39) in player:
                highCards.append(i + 39)
    if player == player3:
            print("Your hand is: ")
            printCards(player)
            while True:
                humanCard1 = input('Please pass a card: ')
                highCards.append(convertHumanCard(humanCard1))
                if convertHumanCard(humanCard1) in player3:
                    break
            player3.remove(convertHumanCard(humanCard1))
            
            print("Your hand is: ")
            printCards(player)
            while True:
                humanCard2 = input('Please pass a card: ')
                highCards.append(convertHumanCard(humanCard2))
                if convertHumanCard(humanCard2) in player3:
                    break
            player3.remove(convertHumanCard(humanCard2))
            
            print("Your hand is: ")
            printCards(player)
            while True:
                humanCard3 = input('Please pass a card: ')
                highCards.append(convertHumanCard(humanCard3))
                if convertHumanCard(humanCard3) in player3:
                    break
            player3.remove(convertHumanCard(humanCard3))
    if len(highCards) >= cardNumber:
                return(highCards[:cardNumber])

def passCards():
    highCards = []
    for index,player in enumerate(players):
        highCards.append(getHighestCards(player, 3))
        if index != 3:
            for card in highCards[index]:
                player.remove(card)
    players[1] += highCards[0]
    players[2] += highCards[1]
    players[3] += highCards[2]
    players[0] += highCards[3]
    player3.sort()

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
    playHearts = False
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
            #not the first player in the round
            if len(currentHand) != 0:
                if not playHearts and humanCard >=27 and humanCard <= 39:
                    playHearts = True
                    print('you played a heart')
                break
            #we are the first player of the round
            else:
                if humanCard >=27 and humanCard <= 39 and playHearts == True:
                    break
                elif (humanCard < 27 or humanCard > 39) and humanCard in player3:
                    break
    player.remove(humanCard)
    return(humanCard)

def playCard(player,isFirstCard=False):
    global playHearts
    if isFirstCard:
        player.remove(CLUBS_2)
        return(CLUBS_2)
    elif(len(currentHand)>0):
        handSuite=getSuite(currentHand[0][1])
        suiteCards=getCardsBySuite(player,handSuite)
        if len(suiteCards)==0:
            #testing - just use the first card in their hand
            if not playHearts and player[0] >= 27 and player[0] <= 39:
                playHearts = True
                print('someone played a heart')
            return(player.pop(0))
        else:
            #testing - just use the first found card in the suite
            player.remove(suiteCards[0])
            return(suiteCards[0])
    else:
        #testing - just use the first card in their hand
        for card in player:
            if card < 27 or card > 39:
                player.remove(card)
                return(card)
            elif playHearts == True:
                player.remove(card)
                return(card)
        #if we get here all cards must be hearts
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

def getArguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--test', type = int, default = 0, help='foo help')

    args = parser.parse_args()
    return(args)

def playGame():
    for pile in trickPiles:
        pile.clear()
    scores.clear()
    aPlayer = getFirstPlayer()
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

def main():
    global human
    args = getArguments()
    if args.test > 0:
        human = 5
        print('test')
        name = 'Jerry'
    else:
        name = input('Please enter your name: ')

    random.seed()
    playerNames.append(name)
    initalizeDeck()
    for i in range(0,args.test+1):
        shuffleDeck(1000)
        deal()
        passCards()
        playGame()
        pass
    
if __name__ == "__main__":
    main()