from functools import reduce

picks = []
moneyline = ""
count = 1
while True:
	moneyline = input(f"Pick {count}: ")
	if moneyline.lower() == "end":
		break
	try:
		ml = int(moneyline)
		probability = 0
		if ml > 0:
			probability = 1/(ml/100+1)
		else:
			probability = 1/(1+100/abs(ml))

		picks.append(probability)
		count = count + 1
		print('Current Probability: ', '{:.1%}'.format(reduce(lambda x, y: x*y, picks)))
	except Exception as e:
		print('you fucked something up')

print('Final Probability: ', '{:.1%}'.format(reduce(lambda x, y: x*y, picks)))
