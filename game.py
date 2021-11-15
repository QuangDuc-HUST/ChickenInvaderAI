# import algo, main
from main import *

### Test github

# main
def ship_run(space:'Space'):
	"""
	given space.figure"""
	inv_num = len(space.invaders)
	bul_num = len(space.bullets)
	a_star = inv_num - bul_num
	


if __name__ == "__main__":
	space, ship = environment_initialize(10,7,8)
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