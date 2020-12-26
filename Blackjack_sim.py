#to do:
#check cards in hand when reshuffling
#check who is bust or who wins
#main loop
#player agent code



import random


#start by declaring needed variables

hands_playing = 100 #the amount of hands being played

#the first digit is the card and the second is the suit, eg. 'AC' = Ace of clubs. T = 10
complete_deck = ['AC','2C','3C','4C','5C','6C','7C','8C','9C','TC','JC','QC','KC','AD','2D','3D','4D','5D','6D','7D','8D','9D','TD','JD','QD','KD','AH','2H','3H','4H','5H','6H','7H','8H','9H','TH','JH','QH','KH','AS','2S','3S','4S','5S','6S','7S','8S','9S','TS','JS','QS','KS']

current_deck = complete_deck #do this to reset the temp deck

#this can be used in future so the player agent can retain knowledge from previous hands
player_knowledge = [] 

#deal two cards to the player and the dealer. calling this function should be done like so: "dealer_hand, player_hand = deal_starting_cards()"
def deal_starting_cards():
    #deal two cards to player and dealer

    #declare lists
    dealer_cards = []
    player_cards = []
    global current_deck
    #generate cards
    if len(current_deck) > 3:
        dealer_cards.append(current_deck.pop(random.randint(0,len(current_deck) - 1)))
        dealer_cards.append(current_deck.pop(random.randint(0,len(current_deck) - 1)))
        player_cards.append(current_deck.pop(random.randint(0,len(current_deck) - 1)))
        player_cards.append(current_deck.pop(random.randint(0,len(current_deck) - 1)))
    else:
        need_shuffle()
        dealer_cards.append(current_deck.pop(random.randint(0,len(current_deck) - 1)))
        need_shuffle()
        dealer_cards.append(current_deck.pop(random.randint(0,len(current_deck) - 1)))
        need_shuffle()
        player_cards.append(current_deck.pop(random.randint(0,len(current_deck) - 1)))
        need_shuffle()
        player_cards.append(current_deck.pop(random.randint(0,len(current_deck) - 1)))


    return dealer_cards, player_cards

#check if the deck is empty and if so, reshuffle the discard pile back in. call this when drawing from the deck to make sure it gets shuffled when it runs out
def need_shuffle():
    global current_deck
    if len(current_deck) == 0:
        current_deck = ['AC','2C','3C','4C','5C','6C','7C','8C','9C','10C','JC','QC','KC','AD','2D','3D','4D','5D','6D','7D','8D','9D','10D','JD','QD','KD','AH','2H','3H','4H','5H','6H','7H','8H','9H','10H','JH','QH','KH','AS','2S','3S','4S','5S','6S','7S','8S','9S','10S','JS','QS','KS']
    
    return

#split string into list of characters
def split(string): 
    return [char for char in string]  

#get the value of the current hand
def get_hand_value(hand):
    #hand value logic
    x = 0
    hand_value = 0
    aces = 0
    while x < len(hand):
        x = x + 1
        temp = split(hand[x - 1])
        if temp[0].isnumeric() == 1:  
            hand_value = hand_value + int(temp[0])
        elif temp[0] == 'A':
            aces = aces + 1
        else:
            hand_value = hand_value + 10
    x = 0
    while x < aces:
        x = x + 1
        if hand_value + 11 > 21:
            hand_value = hand_value + 1
        else:
            hand_value = hand_value + 11

    return hand_value

#draw a card and add it to selected hand
def draw_card(hand):
    global current_deck
    need_shuffle()
    hand.append(current_deck.pop(random.randint(0,len(current_deck) - 1)))
    return hand


#this is the logic that decides the dealers action. this will return the dealers final hand when finished running
def dealer_agent(dealer_hand):
    hand_value = get_hand_value(dealer_hand)
    #dealer decision making
    if hand_value < 17:
        #draw a card
        dealer_hand = draw_card(dealer_hand)
        dealer_hand = dealer_agent(dealer_hand)
        return dealer_hand

    else:
        return dealer_hand

#this is the logic that decides the players action. this will return the players final hand when finished running
def player_agent(player_hand, dealer_first_card,player_knowledge):
    #this is temporary logic
    player_hand = dealer_agent(player_hand)
    return player_hand

#this handles calling all agent functions and decides what agent won that hand
def engine_loop():
    global current_deck
    global player_knowledge
    player_win = 0 #set this to 1 if player wins

    dealer_hand, player_hand = deal_starting_cards()
    
    dealer_hand = dealer_agent(dealer_hand)
    player_hand = player_agent(player_hand, 'null', player_knowledge)

    dealer_hand_value = get_hand_value(dealer_hand)
    player_hand_value = get_hand_value(player_hand)

    if player_hand_value > dealer_hand_value and player_hand_value < 22:
        player_win = 1
    elif dealer_hand_value > 21 and player_hand_value < 22:
        player_win = 1
    elif player_hand_value == 21 and len(player_hand) == 2:
        player_win = 1
    elif player_hand_value <= dealer_hand_value:
        player_win = 0


    return player_win

#this function handles the replaying of hands and recording the amount of wins. this functions outputs an integer of how many times the player won the hand
def main_loop(hands_playing):
    x = 0
    player_wins = 0
    while x < hands_playing:
        x = x + 1
        player_wins = player_wins + engine_loop()
    
    return player_wins


wins = main_loop(hands_playing)

#print an output that shows how many games were played, the amount of player agent wins and the win rate for the given player agent.
print(str(hands_playing) + " hands played with the player winning " + str(wins) + " times. win rate: " + str((wins/hands_playing)*100) + "%")