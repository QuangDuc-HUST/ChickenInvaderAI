import numpy as np
import timeit
from QD import heuristic

class NotExistSpace(Exception):
	pass

class GameNotIni(Exception):
	pass

class NotEnoughActions(Exception):
	pass

class Evaluate(object):

	def __init__(self, belong:'GameModel'):
		self._step = 0
		self._time = 0
		self._belong = belong
	
	def settime(self):
		'''
		Set time
		'''
		self._time = timeit.default_timer()
		
	def gettime(self):
		'''
		Get time
		'''
		return timeit.default_timer() - self._time
	def setstep(self, step):
		'''
		set step
		'''
		self._step = step

	def getstep(self):
		'''
		get step
		'''
		return self._step

	
	def evamultitime(self, algorithm:'function', isOnline , times):
		'''
		Evaluate multiple times
		times : int
		lst_time: lst of time
		lst_result: lst of results
		lst_actions: lst of actions
		'''
		lst_time = []
		lst_result = []
		lst_steps = []

		for _ in range(times):
			self._belong.reinitialize()
			result, time, steps, self._actions = self._belong.run(algorithm, isOnline)
			lst_time.append(time)
			lst_result.append(result)
			lst_steps.append(steps)
		
		print('-' * 30)
		print('Multitime Evaluation')
		print(f'List of times: {lst_time}')
		print(f'List of result: {lst_result}')
		print(f'List of steps: {lst_steps}')
		print(f'Mean time: {sum(lst_time) / len(lst_time) :.4f} seconds.')
		print(f'Mean steps: {sum(lst_steps) / len(lst_steps) :.2f} steps.')
		print('-' * 30)


class Object(object):

	def __init__(self, x:int=None, y:int=None, belong:'Space'=None, label:str=None):
		"""
		x: vertical position of object
		y: horizontol position of object
		belong: object belong a space
		"""

		self.x = x
		self.y = y 
		self.collided = False
		self.label = label
		self.belong = belong

	def collide(self, other:'Object'):
		"""
		function that check whether an object collides another object\\
		(2 objects have same label cannot collide)
			return True if collision occurs\\
			else False"""
		return self.y == other.y and self.x == other.x and self.label != other.label

	def get_position(self):
		"""
		return position of object (x,y)\\
		type: (tuple) """
		return self.x, self.y

	def move(self, dir=None):
		pass


class SpaceShip(Object):

	def __init__(self, x, y, belong:'Space'=None,  label='Ship', available:bool = True ):
		"""
		Object().__init__(x, y, belong, label)\\
		new: 
			(param) available:(bool) : whether an attack is available
				default: True (can attack from beginning)
			(instance) status:bool  whether still alive\\
				(default: True) False when collided"""
			
		super().__init__(x, y, belong, label)
		self.available = available
		self.status = True
		self.up()
	
	def move(self, dir=None):
		"""
		function that make the space ship a move\n
		dir:
			 'left'/1: move 1 to left
			 'right'/2: move 1 to right
			 if 0: the space ship try to attack
		make an attack available in next step 
		"""
		self.belong.figure[self.x, self.y] -= 2
		if dir in [1,2,'a', 'd', 'left', 'right', 'remain']:
			if dir in ['left', 1, 'a'] and self.y >=1:
				self.y -=1
			elif dir in ['right', 2, 'd'] and self.y < self.belong.width -1:
				self.y +=1 
			self.available = True
		elif dir in [0, 'w']: 
			self.attack()
			self.available = not self.available
		self.belong.figure[self.x, self.y] += 2

	def attack(self):
		"""
		function that:
			if available: space ship shot a bullet
			else: stays remain
		"""
		if self.available:
			#attack 
			_ = Bullet(self.x -1, self.y, belong=self.belong)
		
	def is_death(self):
		"""
		whether the space ship is damaged and died
			True if: ship.status == False\\
			else False
		"""
		return not self.status

	def up(self):
		self.belong.figure[self.x, self.y] +=2
		self.belong.spaceship = self


class Bullet(Object):

	def __init__(self, x, y, belong: 'Space', label='Bullet'):
		"""
		Object().__init__(x=x, y=y, belong=belong, label=label)\\
	
		"""
		super().__init__(x=x, y=y, belong=belong, label=label)
		self.up()
	
	def move(self):
		"""
		bullet tries to move 2 upward\\
		if collides with an invader, both invader and bullet disappear 
		"""
		self.belong.figure[self.x, self.y] -= 7 
		if self.belong.figure[self.x-1, self.y ] ==1:
			self.x -=1
		else:
			self.x -=2

		if self.x >= 0:
			self.belong.figure[self.x, self.y] += 7			
		else:
			self.belong.bullets.remove(self)
			
	def up(self):
		"""
		append the bullet to list of bullets where it belongs to when created"""
		self.belong.bullets.append(self)
		self.belong.figure[self.x, self.y ] +=7

	
class Egg(Object):

	def __init__(self, x, y, belong: 'Space', label='Egg'):
		"""
		Object().__init__(x=x, y=y, belong=belong, label=label)\\
		call method self.up()"""
		super().__init__(x=x, y=y, belong=belong, label=label)
		self.up()
	
	def drop(self):
		"""
		Egg drop 1 each time if have not been broken \\
		if the egg is broken (do not collide with ship),\\ 
		then remove from eggs list of space
		"""
		if not self.is_break():
			self.belong.figure[self.x, self.y] -=4
			self.x +=1
			self.belong.figure[self.x, self.y] +=4
		else:
			self.belong.figure[self.x, self.y] -=4
			self.belong.eggs.remove(self)

	def is_break(self) :
		"""
		Function that return whether an egg is break
		\tTrue: if y postion of egg is at the bottom
		\tFalse: elsewhere
		"""
		return self.x >= self.belong.height -1
	
	def up(self):
		"""
		append the egg to list of eggs of space where it belongs to when created"""
		self.belong.eggs.append(self)
		self.belong.figure[self.x, self.y ] +=4


class Invader(Object):

	def __init__(self, x, y, belong: 'Space', label="Invader"):
		"""
		Object().__init__(x=x, y=y, belong=belong, label=label)\\
		call method self.up()"""
		super().__init__(x=x, y=y, belong=belong, label=label)
		self.up()
	
	def lay(self):
		"""
		invader drop an egg:'Egg'
		"""
		_ = Egg(self.x+1, self.y , belong=self.belong )

	def up(self):
		"""
		append the invader to list of invaders of space\\
		where it belongs to when created"""
		self.belong.invaders.append(self)
		self.belong.figure[self.x, self.y] +=1
				
	def death(self):
		"""
		khong biet co can hay khong"""


class Space(object):

	def __init__(self, height:int, width:int):
		"""
		Environment for a space fight between invaders and our space ship
			height: maximum y-distance from space ship to invader
			width: maximum x-distance that space ship can move along
			num: number of invaders, since depend on environment's width
		(instance):
			spaceship: (type:Space) a ship \\ 
			invaders: (type:list) list contains all invaders remaining\\
			eggs: (type:list) list contains all eggs remaining\\
			bullets: (type:list) list contains all bullets remaining\\
			figure: (type: np.array, shape(height, width)) show position of each object\\
				in space by a matrix
		"""

		self.height = height
		self.width = width
		self.num = 0
		


		self.step = -1

		self.spaceship = None
		self.invaders = []
		self.eggs = []
		self.bullets = []
		self.figure = np.zeros((self.height, self.width), dtype=int)

	def show(self):
		"""
		Method show matrix represent position of all objects in space"""
		print(self.figure)


	## for initialize

	def invaders_initialize(self):
		"""
		Create <num> invaders satisfy restriction\\
		num: number of invaders
		"""
		cal = sorted(np.random.choice(range(self.width* 2), self.num, replace=False))
		for i in range(len(cal)):
			Invader(cal[i]%2, cal[i]//2, self)
	

	def invader_actions(self):
		'''
		Control actions of the invaders
		
		'''
		acting_possible_invaders = []

		for invader in self.invaders:
			x, y = invader.get_position()
			if self.figure[x+ 1, y ] != 1:
				acting_possible_invaders.append(invader)

		if self.step % 3 == 0 : 
			if len(acting_possible_invaders) > 3: 
				laying_invader = sorted(np.random.choice(range(len(acting_possible_invaders)), 3, replace=False))
				for i in laying_invader:
					acting_possible_invaders[i].lay()
			else:
				for i in acting_possible_invaders:
					i.lay()

	def initialize(self, num:int):
		'''
		initialize by itself like environment_initialize

		Create a space including ship, invaders satisfies restriction
		return space, ship, figure\\
		height: height of space
		width: 	width of space
		num:	number of invaders

		'''
		self.num = num

		ship_y = np.random.randint(self.width)

		# ship_y = space.width //2  
		# ship_y = 0
		SpaceShip(x=self.height-1, y=ship_y, belong=self)

		self.invaders_initialize()

	
	def check_collision(self):
		"""
		Check for collision\\
		Remove object (excluding Agent) if any collision occurs\\
		Chech for collision of Agent
		Return True if Agent defeated\\
		else Fasle (then continue game)
		"""
		for invader in self.invaders.copy():
			for bullet in self.bullets.copy():
				if bullet.collide(invader):
					self.bullets.remove(bullet)
					self.invaders.remove(invader)

					self.figure[bullet.x, bullet.y ] -=8
		for egg in self.eggs.copy():
			if self.spaceship.collide(egg):
				print(f'collision occurs at x= {self.spaceship.x} , y ={self.spaceship.y}')
				return True
		return False


	def check_winning(self):
		"""
		Check whether the Agent is winning
		Return True if not reach terminal state
			(Winning when number of invaders is 0)"""
		return len(self.invaders) == 0


class GameModel(object):
	'''
	main model of the game in order to : evaluate, environment, control the ship
	'''
	def __init__(self):
		'''
		Input:
		Variables
		_space (SPACE)
		_actions(list)
		_states(list)
		'''
		self._space = None
		self._actions = []
		self._states = []
		self._evaluate = Evaluate(self)
		self._isinit = False

	
	def initialize(self, height, width, num):
		'''
		Initialize the space
		evaluate
		'''
		## This part for evaluate
		self._height = height
		self._width = width
		self._num = num
		##
		self._space = Space(height, width)
		self._space.initialize(num)
		self._isinit = True
	
	def reinitialize(self):
		if not self._isinit:
			raise GameNotIni("Don't forget to initialize game before reinit.")

		self._space = Space(self._height, self._width)
		self._space.initialize(self._num)


	def getSpace(self):
		return self._space

	def getEvaluate(self):
		return self._evaluate
	
	def restartEvaluate(self):
		self._evaluate = Evaluate(self)
		return self._evaluate
	
	def run(self, algorithm:'function', isOnline = True):
		'''
		algorithm: if isOnline = True, return one action of ship
				   if isOffline = False, return list of actions
		times: the number of evaluation

		return: True if win else False

		Example
		def test(space):
			`` space: Space``
			return an action, time, steps, actions

		'''
		

		if isOnline:
			space = self.getSpace()

			if space is None:
				raise NotExistSpace("Don't forget to initialize game.")


			result = None		
			self._evaluate.settime()
			self._evaluate.setstep(0)

			self._states.append(space.figure)
			
			print(space.figure)
			print('-+-+'*20)

			
			while True:
				space.step += 1
				print(f'Step {space.step + 1}: Do ', end='')

				# for bullet in space.bullets.copy():	
				for bullet in space.bullets:	
					bullet.move()

				# for invader in space.invaders.copy():
				# 	for bullet in space.bullets.copy():
				# 		if bullet.collide(invader):
				# 			space.bullets.remove(bullet)
				# 			space.invaders.remove(invader)
				# 			space.figure[bullet.x, bullet.y ] -=8

				for invader in space.invaders:
					for bullet in space.bullets:
						if bullet.collide(invader):
							space.bullets.remove(bullet)
							space.invaders.remove(invader)
							space.figure[bullet.x, bullet.y ] -=8


				temp = algorithm(space)
				## For evaluate
				self._actions.append(temp)

				print(f'You choose: {temp}')
				########################
				space.spaceship.move(temp)
				########################
				self._evaluate.setstep(space.step)

				for egg in space.eggs.copy():
					egg.drop()
				ret = False
				for egg in space.eggs.copy():
					if space.spaceship.collide(egg):
						result = False
						print('LOSING')
						print(f'Collision occurs at x = {space.spaceship.x} , y = {space.spaceship.y}')
						ret = True
				if ret:
					break

				space.invader_actions()

				if space.check_winning():
					result = True
					print('WINNING')
					break
				self._states.append(space.figure.copy())

				################ Just for testing
				print(f'Invaders: {[x.get_position() for x in space.invaders]}')
				print(f'Spaceship: {space.spaceship.get_position()}')
				print(f'Bullets: {[x.get_position() for x in space.bullets]}')
				print(f'Eggs: {[x.get_position() for x in space.eggs]}')
				# print(heuristic(space))
				################
				## Display each step
				space.show()
				print('---'*10)

			## Display

			time = self._evaluate.gettime()
			steps = self._evaluate.getstep()


			print(f'Running time: {time}')
			print(f'Number of steps: {steps + 1}')

			return result, time, steps, self._actions
		
		else:
			##Offline
			space = self.getSpace()

			if space is None:
				raise NotExistSpace("Don't forget to initialize game.")


			result = None		
			self._evaluate.settime()
			self._evaluate.setstep(0)

			self._states.append(space.figure.copy())
			
			print(space.figure)
			print('-+-+'*20)


			temp = []
			while True:
				space.step += 1

				for bullet in space.bullets:	
					bullet.move()

				for invader in space.invaders:
					for bullet in space.bullets:
						if bullet.collide(invader):
							space.bullets.remove(bullet)
							space.invaders.remove(invader)
							space.figure[bullet.x, bullet.y ] -=8

				## temp: list of actions
				if not space.step % 3:
					# print(f'Step {space.step}: Do for the next 3 steps: ', end='')
					print(f'Current heuristic: {heuristic(space)}')
					temp = algorithm(space , 1)
					actionnow = temp
					# if len(temp) != 3:
						# raise NotEnoughActions('3 Actions Please.')
				elif not (space.step % 3 - 1):
					temps = algorithm(space, 1)
					print(temps)
				
				
				if space.step % 3 :
					actionnow = temps[space.step % 3 - 1]

				## For evaluate
				self._actions.append(actionnow)

				print(f'You choose: {actionnow}')
				########################
				space.spaceship.move(actionnow)
				########################
				self._evaluate.setstep(space.step)

				for egg in space.eggs.copy():
					egg.drop()
				ret = False
				for egg in space.eggs.copy():
					if space.spaceship.collide(egg):
						result = False
						print('LOSING')
						print(f'collision occurs at x= {space.spaceship.x} , y ={space.spaceship.y}')
						ret = True
				if ret:
					break

				space.invader_actions()

				if space.check_winning():
					result = True
					print('WINNING')
					break

				self._states.append(space.figure)

				## Display each step
				space.show()
				print('---'*10)

			## Display

			time = self._evaluate.gettime()
			steps = self._evaluate.getstep()


			print(f'Running time: {time}')
			print(f'Number of steps: {steps + 1}')

			return result, time, steps, self._actions
	
	def getStatesStatistic(self):
		return self._states
	
	
	def getActionsStatistic(self):
		return self._actions

