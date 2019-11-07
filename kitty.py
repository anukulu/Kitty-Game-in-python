import random
import itertools
from collections import OrderedDict
import numpy as np

class Card:
	def __init__(self, name, color):
		self.name = name
		self.color = color

class Deck:
	def __init__(self):
		self.numberOfCards = 52
		self.colors = ['C', 'D', 'H', 'S']
		self.nameOfCards = [i for i in range(1,14)] # Here no 1 is card 2 and number 13 is an ace
		self.deck = []

	def MakeDeck(self):
		for i in self.colors:
			for j in self.nameOfCards:
				self.deck.append(Card(j,i))

	def ShuffleDeck(self):
		random.shuffle(self.deck)

	def ShowDeck(self):
		for card in self.deck:
			print(str(card.name) + card.color)

	def DistributeDeck(self):
		hand = []
		for x in range(0,9):
			hand.append(self.deck.pop())
		return hand


class Arrangement:
	def __init__(self):			# assignment of probabilities to the each possible combination of cards
		self.handProbabilities = {'Trio': 0.0022,
								  'PureSequence': 0.0024,
								  'Sequence': 0.0326,
								  'Color': 0.0496,
								  'Pair': 0.1694,
								  'HighCard': 0.7439}
	def SortCards(self, allArrangements):		# sorting three cards in ascending order of their name
		# customObjects.sort(key=lambda x: x.date, reverse=True)
		sortedPossibleCombinations = []
		for oneArrangement in allArrangements:
			arrangementToAdd = list(oneArrangement)
			arrangementToAdd.sort(key=lambda x: x.name, reverse=False)
			sortedPossibleCombinations.append(arrangementToAdd)
		return sortedPossibleCombinations

	def ClassifyCards(self, sortedCombinations):
		combinationsAndProbs = {}
		handType = ''
		i = 0
		for hand in sortedCombinations:
			condition1 = (hand[0].name == hand[1].name) and (hand[1].name == hand[2].name) # This one is for Trio
			condition2 = (hand[0].color == hand[1].color) and (hand[1].color == hand[2].color) # This one is for Color
			condition3 = (((hand[1].name - hand[0].name) == 1) and ((hand[2].name - hand[1].name) == 1)) # This one is for Sequence
			condition4 = ((hand[0].name == hand[1].name) or (hand[0].name == hand[2].name) or (hand[1].name == hand[2].name))
			if(condition1):
				handType = 'Trio'
			elif(condition2):
				handType = 'Color'
				if(condition3):
					handType = 'PureSequence'
			elif(condition3):
				handType = 'Sequence'
			elif(condition4):
				handType = 'Pair'
			else:
				handType = 'HighCard'
			combinationsAndProbs[i] = self.handProbabilities[handType]
			
			i = i + 1
		# sorted(key_value.items(), key = lambda kv:(kv[1], kv[0]))
		combinationsAndProbs = sorted(combinationsAndProbs.items(), key=lambda kv:(kv[1], kv[0]))
		return combinationsAndProbs


	def BestArrangement(self, cards):	# this function prints the best arrangement of the given cards grouped into three
		for givenCard in cards:
			print(str(givenCard.name) + givenCard.color, end=' ')
		print('\n')

		allPossibleCombinations = list(itertools.combinations(cards, 3))	# all the possible combinations are tuples
		sortedPosiibleCombinations = self.SortCards(allPossibleCombinations)
		combinationsAndProbs = self.ClassifyCards(sortedPosiibleCombinations)


		finalArrangement = []
		allProbs = [combinationsAndProbs[i][1] for i in range(0, len(combinationsAndProbs))]		
		previousProb = allProbs[0]
		keys = [combinationsAndProbs[i][0] for i in range(0, len(combinationsAndProbs))]
		for reqdCards in sortedPosiibleCombinations[keys[0]]:
			finalArrangement.append(reqdCards)
		for k in range(0,len(keys)):
			currentProb = allProbs[k]
			currentCombo = finalArrangement[-3:]
			nextCombo = sortedPosiibleCombinations[keys[k]]
			thirdpart = ( len(set(currentCombo).intersection(set(nextCombo))) == len(set(finalArrangement).intersection(set(nextCombo))) )
			conditionA = ((currentProb == previousProb) and (len(set(currentCombo).intersection(set(nextCombo))) > 0) and thirdpart)
			conditionB = ((currentProb == previousProb) and (len(set(currentCombo).intersection(set(nextCombo))) == 0) and thirdpart)
			conditionC = ((currentProb != previousProb) and (len(set(currentCombo).intersection(set(nextCombo))) == 0) and thirdpart)
			if(conditionA):
				sumCurrent = currentCombo[0].name + currentCombo[1].name + currentCombo[2].name
				sumNext = nextCombo[0].name + nextCombo[1].name + nextCombo[2].name
				if (sumCurrent >= sumNext):
					continue
				else:
					finalArrangement = finalArrangement[:len(finalArrangement)-3]
					for cardFinal in nextCombo:
						finalArrangement.append(cardFinal)
					previousProb = currentProb
			elif (conditionB):
				for cardFinal in nextCombo:
					finalArrangement.append(cardFinal)
				previousProb = currentProb
			elif (conditionC):
				for cardFinal in nextCombo:
					finalArrangement.append(cardFinal)
				previousProb = currentProb
		for eachCard in cards:
			if eachCard not in finalArrangement:
				finalArrangement.append(eachCard)

		for finalCard in finalArrangement:
			print(str(finalCard.name) + ' ' + finalCard.color)

		return finalArrangement

class Player:
	def __init__(self, hand):
		self.hand = hand
		arrange = Arrangement()
		self.arrangedHand = arrange.BestArrangement(self.hand)


n = int(input('How many players are playing ? The number should be less than 6 and greater than 1.'))
if ((n > 1) and (n < 6)) :		# This module plays games of Kitty with the number of players specified and decides the winner
	newDeck = Deck()
	newDeck.MakeDeck()
	newDeck.ShuffleDeck()		
	players = []
	arranger = Arrangement()
	for x in range(n):
		newPlayer = Player(newDeck.DistributeDeck())
		players.append(newPlayer)

	pointsTable = np.zeros((3,n), dtype=int)

	for roundNumber in range(3):
		eachRound = []
		for k in range(n):
			individualHand = players[k].arrangedHand[3*roundNumber : 3*(roundNumber+1)]
			eachRound.append(individualHand)
		combinationsSorted = arranger.SortCards(eachRound)	# this variable and eachround have same index
		indexInSortedComb = arranger.ClassifyCards(combinationsSorted)

		maxhand = [combinationsSorted[indexInSortedComb[0][0]]]
		maxIndex = [indexInSortedComb[0][0]]

		for indexAndProb in range(1, len(indexInSortedComb)):
			
			if(indexInSortedComb[0][1] == indexInSortedComb[indexAndProb][1]):
				currentHand = combinationsSorted[indexInSortedComb[indexAndProb][0]]
				sum1 = (maxhand[0][0].name + maxhand[0][1].name + maxhand[0][2].name)
				sum2 = (currentHand[0].name + currentHand[1].name + currentHand[2].name)
				if(sum2 > sum1):
					maxhand = [currentHand]
					maxIndex = [indexInSortedComb[indexAndProb][0]]
				if(sum1 == sum2):
					maxhand.append(currentHand)
					maxIndex.append(indexInSortedComb[indexAndProb][0])

		if(len(maxhand) == 1):
			pointsTable[roundNumber][maxIndex[0]] += 1
	print(pointsTable)

	tempPoints = np.zeros((1,n), dtype=int)
	for rounds in pointsTable:
		i = 0
		for point in rounds:
			if(point == 1):
				tempPoints[0][i] += 1
			else:
				tempPoints[0][i] = 0
			i = i + 1
		if (2 in tempPoints[0]):
			winnerIndex = np.where(tempPoints[0] == 2)
			print("The winner is the number : " + str(winnerIndex[0][0] + 1) + " player.")
		elif(3 in tempPoints[0]):
			winnerIndex = np.where(tempPoints[0] == 3)
			print("The winner also gets Salami.")
else:
	print('The game is not possible.')
