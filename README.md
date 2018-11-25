# Connect4
========================================================

My version of a C4 game. 

- click-based column slot for turn based play
- is_position_winner() converted to suit my implementation of C4
- rudimentary computer algorithm for counter moves
- TODO: some more help/instructions and loops for continuing play 

The is_position_winner() is what I like most about this implementation. Elegant and fast, I fumbled through others' versions 
of itertool, groupby, etc... and then found this. Problem solved. I'm sure it's a style of algorithm with it's own name, I've updated this function now (duplicated) to return consecutive tiles as a value for 'strength' of moves or potential counter moves. 

# Blackjack
========================================================

A small implementation of a blackjack game against computer. First semester 'project'. 
Notably:
- Theoretically player hand can hold up to 21 aces. 
- Hand value calculates highest hand value with aces.

Reasonably happy with the overall program, though we weren't assessed on the code, only the planning, I like that I got a full running game with the potential for multiple games (with multiple aces!) as per the specs originally published by the lecturers.
Don't think I'll update this.
