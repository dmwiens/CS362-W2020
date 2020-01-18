# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 2020

@author: dwiens
"""

import Dominion
import testUtility as tU


# Get player names (and count)
player_names = tU.getPlayerNames()

# number of curses and victory cards
nV = tU.getNumberOfVictoryCards(len(player_names))
nC = tU.getNumberOfCurses(len(player_names))


# Define box and supply
box = tU.getFullBox(nV)
supply_order = tU.getSupplyOrder()
supply = tU.getSupplyFromBox(box, len(player_names), nV, nC)

# initialize the trash
trash = []

# Construct the Player objects
players = tU.getPlayers(player_names)

#########################
# TEST SCENARIO 1

supply["Province"] = []

#########################


# Play the game
turn = 0
while not Dominion.gameover(supply):
    turn += 1    
    print("\r")    
    for value in supply_order:
        print (value)
        for stack in supply_order[value]:
            if stack in supply:
                print (stack, len(supply[stack]))
    print("\r")
    for player in players:
        print (player.name,player.calcpoints())
    print ("\rStart of turn " + str(turn))    
    for player in players:
        if not Dominion.gameover(supply):
            print("\r")
            player.turn(players,supply,trash)
            

# Final score
dcs=Dominion.cardsummaries(players)
vp=dcs.loc['VICTORY POINTS']
vpmax=vp.max()
winners=[]
for i in vp.index:
    if vp.loc[i]==vpmax:
        winners.append(i)
if len(winners)>1:
    winstring= ' and '.join(winners) + ' win!'
else:
    winstring = ' '.join([winners[0],'wins!'])

print("\nGAME OVER!!!\n"+winstring+"\n")
print(dcs)