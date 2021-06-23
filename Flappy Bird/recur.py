def converges(test) :

	i = 1

	conv = 0

	while True :

		if conv == test :
			break;

		else :

			conv = 1 / (2 * i)

			print(conv)

			i = i + 1

converges(0.00001 )