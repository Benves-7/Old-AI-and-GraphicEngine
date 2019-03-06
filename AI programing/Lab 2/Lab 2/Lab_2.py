from os import system
from Manager import *


Manager.Start()
clear = lambda: os.system('cls')

totTime = 0
loops = 0



BaseGameEntityClass.window.window.update()

while True:
	t = perf_counter()
	Manager.Update()
	t = perf_counter() - t

	totTime += t
	loops += 1

	if totTime > 1:
		if loops < 30 and BaseGameEntityClass.window.window.autoflush:
		    BaseGameEntityClass.window.window.autoflush = False
		if not BaseGameEntityClass.window.window.autoflush:
			pass
		    #BaseGameEntityClass.window.window.update()

		clear()
		print("|---------------------------------------------|")
		print("num of loops: " + str(loops))
		print("total time spent: " + str(totTime))
		print("average time per loop: " + str(totTime / loops))
		print("wood in kingdom: " + str(BaseGameEntityClass.townHall.wood))
		print("coal in kingdom: " + str(BaseGameEntityClass.townHall.charcoal))
		totTime = 0
		loops = 0