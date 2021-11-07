# import algo, main
from main import *



# main
space, ship = environment_initialize(10,7,3)
print(space.figure)
print('-+-+'*20)
i = 0
while True:
	i +=1 
	print(f'Step {i}: Do ', end='')


	environment_changes(space=space, step=i)

	# call or do action to Agent 
	n = input()
	ship.move(n)
	# end action

	if check_collision(space=space):
		break
	if check_winning(space=space):
		print('Winning')
		break
	
	space.show()
