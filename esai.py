lst = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

def Combinations(lst, p):
	if p > len(lst):
		return
	else:
		allCombinations = []
		for item in range(len(lst)):
			if (lst[-p:] in allCombinations):
				break
			else:
				auxList = []
				firstGroup = 1
				secondGroup = p - firstGroup
				increment = 1
				while (firstGroup != p):
					i = item
					j = i + increment
					while(lst[-1] not in auxList and (j+secondGroup-1)<len(lst)):
						for y in range(i, i + firstGroup):
							auxList.append(lst[y])
						# print(auxList)
						for x in range(j, j+secondGroup):
							auxList.append(lst[x])
						# print(auxList)
						j = j + 1
						allCombinations.append(auxList)
						auxList = []
					increment = increment + 1
					firstGroup = firstGroup + 1
					secondGroup = secondGroup - 1
		print(allCombinations)
		print(len(allCombinations))
		
Combinations(lst, 3)



