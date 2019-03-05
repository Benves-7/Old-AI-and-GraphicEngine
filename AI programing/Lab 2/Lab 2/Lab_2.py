from os import system
from Manager import *


Manager.Start()
clear = lambda: os.system('cls')

tick = 0
tickstart = 0

timeaverage = 0
loops = 0



tickstart = perf_counter()
BaseGameEntityClass.window.window.update()
while True:
	tick = perf_counter()
	t = perf_counter()
	Manager.Update()
	t = perf_counter() - t
	timeaverage += t
	loops += 1

	if tick - tickstart > 4:
		BaseGameEntityClass.window.window.update()
		tickstart = perf_counter()
		clear()
		print("|---------------------------------------------|")
		print("num of loops: " + str(loops))
		print("total time spent: " + str(timeaverage))
		print("average time per loop: " + str(timeaverage / loops))
		timeaverage = 0
		loops = 0
		print("wood in kingdom: " + str(BaseGameEntityClass.townHall.wood))
		print("coal in kingdom: " + str(BaseGameEntityClass.townHall.charcoal))
