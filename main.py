import random
import itertools
from collections import OrderedDict

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
		for x in range(0,18):
			hand.append(self.deck.pop())
		return hand


class Kitty:
	def __init__(self, noOfPlayers):			# assignment of probabilities to the each possible combination of cards
		self.noOfPlayers = noOfPlayers
		self.handProbabilities = {'Trio': 0.0022,
								  'PureSequence': 0.0024,
								  'Sequence': 0.0326,
								  'Color': 0.0496,
								  'Pair': 0.1694,
								  'HighCard': 0.7439}
		self.combinationsAndProbs = {}
		self.arrangementsAndProbs = {}
	def SortCards(self, oneArrangement):		# sorting three cards in ascending order of their name
		# customObjects.sort(key=lambda x: x.date, reverse=True)
		oneArrangement.sort(key=lambda x: x.name, reverse=False)
		return oneArrangement

	def BestArrangement(self, cards):	# this function prints the best arrangement of the given cards grouped into three
		for givenCard in cards:
			print(str(givenCard.name) + givenCard.color, end=' ')
		print('\n')
		allPossibleCombinations = list(itertools.combinations(cards, 3))
		sortedPosiibleCombinations = []
		
		for singleCombination in allPossibleCombinations:
			sortedCombination = self.SortCards(list(singleCombination))
			sortedPosiibleCombinations.append(sortedCombination)

		handType = ''
		i = 0
		for hand in sortedPosiibleCombinations:
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
			self.combinationsAndProbs[i] = self.handProbabilities[handType]
			givenName = str(hand[0].name)+hand[0].color+str(hand[1].name)+hand[1].color+str(hand[2].name)+hand[2].color
			self.arrangementsAndProbs[givenName] = self.handProbabilities[handType]
			i = i + 1
		# sorted(key_value.items(), key = lambda kv:(kv[1], kv[0]))
		self.combinationsAndProbs = sorted(self.combinationsAndProbs.items(), key=lambda kv:(kv[1], kv[0]))
		self.arrangementsAndProbs = sorted(self.arrangementsAndProbs.items(), key=lambda kv:(kv[1], kv[0]))
		print(self.arrangementsAndProbs)

		finalArrangement = []
		allProbs = [self.combinationsAndProbs[i][1] for i in range(0, len(self.combinationsAndProbs))]		
		previousProb = allProbs[0]
		keys = [self.combinationsAndProbs[i][0] for i in range(0, len(self.combinationsAndProbs))]
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
		for finalCard in finalArrangement:
			print(str(finalCard.name) + ' ' + finalCard.color)

newDeck = Deck()
newDeck.MakeDeck()
newDeck.ShuffleDeck()

newGame = Kitty(4)
newGame.BestArrangement(newDeck.DistributeDeck())



