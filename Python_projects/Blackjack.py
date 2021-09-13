from IPython.display import clear_output
from random import shuffle

card_values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6, 'Seven':7,'Eight':8,'Nine':9,'Ten':10,
              'Jack':10,'Queen':10,'King':10,'Ace':1}
suits = ('Hearts','Diamonds','Clubs','Spades')
ranks = ('Two','Three','Four','Five','Six', 'Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')


class Card():
    #card class will need a suit and rank, a value assigned to it, and will need to be able to print
    #information about the card. Ace is an unique example as it has values of both 1 and 11, depending.
    #This we tackle later
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = card_values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit


#the deck class will need the ability to fill with cards, shuffle and draw random cards
class Deck():
    def __init__(self):
        #here we create a deck of 52 cards
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))

    def shuffle_deck(self):
        shuffle(self.all_cards)

    def deal_card(self):
        return self.all_cards.pop(0)

    def __str__(self):
        #for debugging
        for card in self.all_cards:
            print(card)


#player class will need to have a set amount of money to start with, then the ability to add and
#remove money/chips for betting.
class Player():
    def __init__(self,name,funds):
        self.name = name
        self.funds = funds

    def bet(self):
        self.player_bet = 0
        while self.player_bet < 1:
            try:
                self.player_bet = int(input(f'You have ${self.funds}. How much would you like to bet?: $'))
                if self.player_bet > self.funds:
                    self.player_bet = 0
                    clear_output()
                    print("You don't have enough funds!")
                else:
                    self.funds -= self.player_bet
                    return self.player_bet
            except ValueError:
                clear_output()
                print('That is not a valid number!')

    def add_winnings(self,winnings):
        self.funds += winnings

    def __str__(self):
        return 'You have ' + str(self.funds) + '$.'


class Hand():
    #the hand class will serve to hold both player and dealer cards, it must be capable of adding cards
    #as well as removing them at the end of the round. We also need to add the ability to add 10 to the score
    #to account for an ace
    def __init__(self):
        self.cards = []
        self.score = 0

    def add_card(self,card):
        self.cards.append(card)
        self.score += card.value
        self.ace_score = self.score + 10
        #this is for reporting the possible ace score (to not change the player score)
    def round_end(self):
        self.cards = []
        self.score = 0
        self.ace_score = 0


def game_on(decision):
    if decision in ['yes', 'y','hit','h']:
        return True
    elif decision in ['no', 'n','stand','s']:
        return False


def ace_check(player):
    #if there is an ace in the player/dealer hand, the check terminates and returns true, else returns false
    for card in player.cards:
        if card.rank == 'Ace':
            return True
    return False


def blackjack():
    print('Welcome to blackjack!')
    player = Player(name = 'player1', funds = 500)
    blackjack_on = True
    while player.funds >  0 and blackjack_on:
        deck_of_cards = Deck()
        deck_of_cards.shuffle_deck()
        player_hand = Hand()
        dealer_hand = Hand()

        #first the player bets
        bet = player.bet()
        clear_output()
        for x in range(0,2):
                #deal 2 cards to dealer and player
            player_hand.add_card(deck_of_cards.deal_card())
            dealer_hand.add_card(deck_of_cards.deal_card())
        print(f'The dealer draws two cards, revealing the first: the \33[1m{dealer_hand.cards[0]}\33[0m')
        print(f'You are dealt two cards as well: the \33[1m{player_hand.cards[0]}\33[0m and \33[1m{player_hand.cards[1]}\33[0m')
        if ace_check(player_hand):
            print(f'\nYour current score is {player_hand.ace_score}, dealer has {dealer_hand.cards[0].value} and a hidden card.')
        else:
            print(f'\nYour current score is {player_hand.score}, dealer has {dealer_hand.cards[0].value} and a hidden card.')
        game_switch = game_on(input('Would you like to hit or stand?: '))
        while game_switch and player_hand.score <= 21:
            clear_output()
            #we create a temporary variable, card, to hold the card drawn each round
            player_hand.add_card(deck_of_cards.deal_card())
            if player_hand.cards[len(player_hand.cards) -1] in ['Eight', 'Ace']:
                #if the last card added, i.e the card dealt here is an eight or ace, we need to use 'an'
                print(f'You are dealt an \33[1m{player_hand.cards[len(player_hand.cards) -1]}\33[0m.')
            else:
                #else, we use 'a'
                print(f'You are dealt a \33[1m{player_hand.cards[len(player_hand.cards) -1]}\33[0m.')
            if ace_check(player_hand) and player_hand.ace_score <= 21:
                print(f'\nYour current score is {player_hand.ace_score}, dealer has {dealer_hand.cards[0].value} and a hidden card.')
            else:
                print(f'\nYour current score is {player_hand.score}, dealer has {dealer_hand.cards[0].value} and a hidden card.')
            if player_hand.score <= 21:
                game_switch = game_on(input('Would you like to hit or stand?: '))
            else:
                game_switch = False

        #if we're out of the loop, the player stood or busted, now we need to set the final player score
        #i.e. the better of the two if aces are present (this makes it easier to make comparisons later)
        if ace_check(player_hand) and player_hand.ace_score <= 21 and player_hand.ace_score > player_hand.score:
            #if the player has aces, the score at ace =11 is better and not leading to a bust, we use the ace = 11 score
            player_final_score = player_hand.ace_score
        else:
            #otherwise the final score is the ace = 1 score (or no aces)
            player_final_score = player_hand.score
        #then the dealer logic
        if player_hand.score > 21:
            print('\33[1mBust!\33[0m You lose!')
        else:
            clear_output()
            print(f'Your final score is {player_final_score}.')
            print(f'The dealer has the \33[1m{dealer_hand.cards[0]}\33[0m.')
            print(f'They reveal their hidden card. The \33[1m{dealer_hand.cards[1]}!\33[0m')


            dealer_draws = True
            #This one was hard to figure out. We start by running a loop that can be ended if dealer goes over 17 or has a better score than the player
            while dealer_draws == True:
                if ace_check(dealer_hand):
                    if dealer_hand.ace_score > player_final_score and dealer_hand.ace_score < 21:
                        #if the score is more than the player, and not a bust, we can stop drawing as dealer wins
                        dealer_draws = False
                    elif dealer_hand.ace_score > 17 and dealer_hand.ace_score < 21:
                        #if the ace score is > 17 and not a bust, dealer must use it, so no more cards drawn
                        dealer_draws = False

                    elif dealer_hand.ace_score < 21 and dealer_hand.ace_score < 17 and dealer_hand.ace_score < player_final_score:
                        dealer_hand.add_card(deck_of_cards.deal_card())
                        print(f'The dealer draws another card: the \33[1m{dealer_hand.cards[len(dealer_hand.cards)-1]}\33[0m')
                        if dealer_hand.ace_score < 21 and dealer_hand.ace_score > dealer_hand.score:
                            print(f'Their score is {dealer_hand.ace_score}')
                        else:
                            print(f'Their score is {dealer_hand.score}')
                elif ace_check(dealer_hand) == False or dealer_hand.ace_score > 21:
                    #if no aces or ace at 11 would be a bust, it is simpler:
                    if dealer_hand.score >21 or dealer_hand.score >17 or dealer_hand.score > player_final_score:
                        dealer_draws = False
                    else:
                        dealer_hand.add_card(deck_of_cards.deal_card())
                        print(f'The dealer draws another card: the \33[1m{dealer_hand.cards[len(dealer_hand.cards)-1]}\33[0m')
                        print(f'Their score is {dealer_hand.score}')
            if ace_check(dealer_hand) and dealer_hand.ace_score <= 21 and dealer_hand.ace_score > dealer_hand.score:
                dealer_final_score = dealer_hand.ace_score
            else:
                dealer_final_score = dealer_hand.score


            print(f'\nFinal scores: \nDealer: {dealer_final_score}')
            print(f'You: {player_final_score}')
            #so at this point, the dealer can't draw anymore and scores are final
            if dealer_final_score > 21:
                print(f'Dealer busts. You win {2*bet}$!')
                player.add_winnings(2*bet)
            elif dealer_final_score > player_final_score:
                print('Dealer wins!')
            elif player_final_score == dealer_final_score:
                print(f"It's a draw! You get back your {bet}$!")
                player.add_winnings(bet)
            elif player_final_score > dealer_final_score:
                print(f'You win! Winnings total: {2*bet}$!')
                player.add_winnings(2*bet)

        player_hand.round_end()
        dealer_hand.round_end()
        if player.funds <= 0:
            print("You're out of cash! Some tough-looking security guys are eyeing you. \nTime to head out friend. Better luck next time!")
        else:
            blackjack_on = game_on(input('Would you like to play again?: '))
            if blackjack_on == False:
                print('Alright! See you next time!')
            else:
                pass        
