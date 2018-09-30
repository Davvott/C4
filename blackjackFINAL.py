# blackjack.py
import random

# draws random number value for each of 13 cards
def draw_card():
	random_num = random.randint(1, 13)
	return random_num

def get_card_name(num):
	index = num - 1
	cardnames = ["Ace",2,3,4,5,6,7,8,9,10,"Jack","Queen","King"]
	return cardnames[index]

def calc_hand_value(hand):
	total_value = 0
	aces = 0
	
	for card_value in hand:
		if card_value >= 10:
			total_value += 10
		elif card_value == 1:
			total_value += 11
			aces += 1
		else:
			total_value += card_value

	while total_value > 21 and aces != 0:
		total_value -= 10
		aces -= 1

	return total_value


def display_winner(playername, playertotal, computertotal):
	if playertotal > 21:
		print("You've gone BUST! Sorry {}. House always wins.".format(
			playername))
	elif computertotal > 21:
		print("The computer has gone BUST! Lady-luck smiles upon you.")
	elif playertotal == computertotal:
		print("It's a draw! Play again to prove your skill")
	elif playertotal > computertotal:
		print("You WIN!. Play again to double your money?")
	else:
		print("You lose! Better luck next time {}".format(playername))


def main():
	print(\
"Welcome to Online BlackJack where all your dreams can come \
true as long as lady-luck is with you. To get started please \
enter your name: ")
	player_name = input().title()

	game_loop = True
	start_menu = True
	game_hands = []

	print(\
"Welcome {}! The next round of BlackJack is about to commence.".format(player_name))

	while start_menu is True:
		print(\
"Please choose from the following: \
(P)lay, (I)nstructions, (Q)uit")

		user_input = input().upper()
		if user_input == "P":
			start_menu = False
		elif user_input == "Q":
			start_menu = False
			game_loop = False
		else:
			print(\
"""You will be dealt two cards, and so will the computer.
The goal of the game is to get a combined card total of <=21.
The player achieving the closest to 21 without going over will 
be the winner of that hand.
The value of Aces in your hand will be determined to maximise
the value of your hand as a whole.""")

	while game_loop == True:
		# initialize all variables for new game
		player_hand = []
		player_cardnames = []
		computer_hand =[]
		computer_cardnames  = []
		player_turn = True
		computer_turn = True

		# game start - Deal two cards to Player and COmputer Hands
		for num in range(0, 2):
			player_hand.append(draw_card())
			player_cardnames.append(get_card_name(player_hand[-1]))
			computer_hand.append(draw_card())
			computer_cardnames.append(get_card_name(computer_hand[-1]))
		
		player_score = calc_hand_value(player_hand)
		computer_score = calc_hand_value(computer_hand)


	# Player turn

	
		print("You have drawn two cards. {0} and {1}".format(
			player_cardnames[0], player_cardnames[1]))

		print("The current value of your hand is {}".format(
			player_score))

		while player_turn == True:
			print()
			user_play = input("Would you like to (H)it or (S)tand?: ").upper()

			if user_play == "H":
				player_hand.append(draw_card())
				player_cardnames.append(get_card_name(player_hand[-1]))
				player_score = calc_hand_value(player_hand)
				print("You have drawn a {}".format(player_cardnames[-1]))
				print("The current value of your hand is {}".format(player_score))

			elif user_play == "S":
				print("You have chosen to stand on {}".format(player_score))
				player_turn = False

			if player_score > 21:
				computer_turn = False
				player_turn = False

		# Computer Turn
		if computer_turn == True:
			print("The computer has been dealt two cards. {0} and {1}".format(
				computer_cardnames[0], computer_cardnames[1]))
			print("The computer's total hand value is {}".format(computer_score))

		while computer_score < 17 and computer_turn == True:
			computer_hand.append(draw_card())
			computer_cardnames.append(get_card_name(computer_hand[-1]))
			computer_score = calc_hand_value(computer_hand)
			print("The computer requests another card.")
			print("The computer has drawn a {}.".format(computer_cardnames[-1]))
			print("The computer's total hand value is {}.".format(computer_score))
			
		if computer_score  >= 17 and computer_score <= 21:
			print("The computer stands on {}.".format(computer_score))

		game_hands.append([player_score, computer_score])

		display_winner(player_name, player_score, computer_score)
		
		# End of Game selection Y/N
		print()
		play_again = input("Would you like to play again? (Y/N)").upper()
		
		if play_again == "N":
			
			game_loop = False
			print("Thanks for playing IT@JCU BlackJack")
			print("Your playing history from today is as follows:")

			#  for sublist in game_hands: ???
			for index in range(len(game_hands)):
				print("Hand {}:".format(index + 1))
				print("You scored {}".format(game_hands[index][0]))
				print("The computer scored {}".format(game_hands[index][1]))
				
				if game_hands[index][0] > game_hands[index][1]:
					print("You WON that hand!")
				elif game_hands[index][1] > game_hands[index][0]:
					print("You lost that hand!")
				else:
					print("That hand was a DRAW")
# main()