#1=2 13=ace
#spades 1-13
#clubs 14-26
#hearts 27-39
#diamonds 40-52
#queen of spades = 11
import random
import argparse
import sys
import cardFunc as cards

theMode = False
playHearts = False
player0 = []
player1 = []
player2 = []
player3 = []
players = [player0, player1, player2, player3]
currentHand = [] # list: [player, card]
trickPile0 = []
trickPile1 = []
trickPile2 = []
trickPile3 = []
trickPiles = [trickPile0,trickPile1,trickPile2,trickPile3]
scores = []
playerNames = ['Jim', 'Doug', 'Bob']
human = 3
scoreStatistics = [0,0,0,0]
timesRun = 0
dumbDoug = 0

def getLowerThan(target, cardList):
    closestCard = 52
    mostDifference = 52
    for card in cardList:
        if (target-card) < mostDifference:
            closestCard = card
            mostDifference = target-card
    return(closestCard)

def printCurrentHand(aHand):
    debugString = ''
    for cardPair in aHand:
        txt = playerNames[cardPair[0]]+":"+cards.getCardString(cardPair[1])
        debugString += txt+' '
    print(debugString)  

def findScore():
    for index,pile in enumerate(trickPiles):
        scores.append(0)
        for card in pile:
            if cards.SUITE_HEARTS == cards.getSuite(card):
                scores[index] += 1
            elif(card==11):
                scores[index] += 13
    if sum(scores) != 26:
        print("something's wrong")
        print(scores)
        quit()
    if 26 in scores:
        for index,score in enumerate(scores):
            if score == 26:
                scores[index] = 0
            elif score == 0:
                scores[index] = 26
            else:
                sys.exit("NICE TRY CHEATER!")
        global timesRun
        timesRun += 1
        #print(scores)
        #sys.exit("Someone ran it")

def takeTrick(winner,hand):
    for card in hand:
        trickPiles[winner].append(card[1])

def findTrickWinner(hand):
    theSuite = cards.getSuite(hand[0][1])
    leader = hand[0]
    for card in hand:
        if theSuite==cards.getSuite(card[1]):
            if card[1]>leader[1]:
                leader = card
    return(leader)

def humanPlayCard(player,isFirstcard=False):
    playHearts = False
    print("Your hand is: ")
    cards.printCards(player)
    print("Current Trick is:")
    printCurrentHand(currentHand) 
    validCards = []
    if len(currentHand) > 0:
        leaderSuite = cards.getSuite(currentHand[0][1])
        validCards = getCardsBySuite(player,leaderSuite)
    while True:  
        humanCard = input('Play card: ')
        if len(humanCard) < 2:
            continue
        if not humanCard[0].isalpha() or not humanCard[1].isnumeric():
            continue
        humanCard = cards.convertHumanCard(humanCard)
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

def getLeastSuite(player):
    suiteCount = [0,0,0,0]
    suite = [0,52]
    for card in player:
        cardSuite = cards.getSuite(card)
        if cardSuite == cards.SUITE_SPADES:
            suiteCount[0] += 1
        elif cardSuite == cards.SUITE_CLUBS:
            suiteCount[1] += 1
        #elif cardSuite == SUITE_HEARTS:
            #suiteCount[2] += 1
        elif cardSuite == cards.SUITE_DIAMONDS:
            suiteCount[3] += 1
        else:
            sys.exit('STOP CHEATING!')
    for index,leastSuite in enumerate(suiteCount):
        if leastSuite < suite[1] and suite[1] != 0:
            suite = [index, leastSuite]
    return(suite[0])

def playCard(player,isFirstCard=False):
    global playHearts
    global dumbDoug
    if isFirstCard:
        player.remove(cards.CLUBS_2)
        return(cards.CLUBS_2)
    elif(len(currentHand)>0):
        handSuite=cards.getSuite(currentHand[0][1])
        suiteCards=getCardsBySuite(player,handSuite)
        if len(suiteCards)==0:
            #testing - just use the first card in their hand
            if not playHearts and player[0] >= 27 and player[0] <= 39:
                playHearts = True
                print('someone played a heart')
            return(player.pop(0))
        else:
            #testing - just use the first found card in the suite
            lowCard = cards.getLowestCards(currentHand)
            closeCard = getLowerThan(lowCard, suiteCards)
            player.remove(closeCard)
            return(closeCard)
    else:
        #if 11 in player and player == player1:
            #print('dumb doug')
            #dumbDoug += 1
            #player.remove(11)
            #return(11)
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

def getCardsBySuite(player,handSuite):
    cardList=[]
    for card in player:
        if handSuite == cards.getSuite(card):
            cardList.append(card)
    return(cardList)

def getFirstPlayer():
    for index,player in enumerate(players):
        if cards.CLUBS_2 in player:
            return(index)

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
        if not getTest():
            print("Then trick winner is: " + playerNames[trickWinner[0]] + ' [' + playerNames[currentHand[0][0]] + ':' + cards.getCardString(currentHand[0][1]) + ', ' + playerNames[currentHand[1][0]] + ':' + cards.getCardString(currentHand[1][1]) + ', ' + playerNames[currentHand[2][0]] + ':' + cards.getCardString(currentHand[2][1]) + ', ' + playerNames[currentHand[3][0]] + ':' + cards.getCardString(currentHand[3][1]) + ']')
        takeTrick(trickWinner[0],currentHand)
        currentHand.clear()
        aPlayer = trickWinner[0]
    findScore()
    winner = 0
    winnerScore = 26
    for index,score in enumerate(scores):
        if not getTest():
            print(playerNames[index]+': '+str(scores[index]))
        if scores[index] < winnerScore:
            winnerScore = scores[index]
            winner = index
    print('The winner is: ' + playerNames[winner])
    if human == 5:
        scoreStatistics[winner] += 1

def setTest(mode):
    global theMode
    theMode = mode

def getTest():
    return(theMode)

#def makeDougLose():
    #for player in players:
        #if 11 in player:
           # player.remove(11)
            #player1.append(11)
            #player.append(player1.pop(0))
            #break

def getPlayerHands():
    player0.sort()
    return(players)

def main():
    global human
    args = getArguments()
    if args.test > 0:
        human = 5
        setTest(True)
        print('test')
        name = 'Jerry'
    else:
        name = 'You'

    random.seed()
    playerNames.append(name)
    cards.initalizeDeck()
    for i in range(0,args.test+1):
        cards.shuffleDeck(1000)
        cards.deal(players)
        cards.passCards(players, human)
       # makeDougLose()
        #playGame()
        pass
    if human == 5:
        print(scoreStatistics)
        print(timesRun)
        print(dumbDoug)
    
if __name__ == "__main__":
    main()