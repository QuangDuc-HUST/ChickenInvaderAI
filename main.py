# from algo import *
import numpy as np



class Object():

	def __init__(self, x:int=None, y:int=None, belong:'Space'=None, label:str=None):
		"""
		x: horizontal position of object
		y: vertical position of object
		belong: object belong a space
		Test github
		label: ....
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
		return (self.x, self.y)

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
		if dir in [1,2,'a', 'd', 'left', 'right']:
			if dir in ['left', 1, 'a'] and self.y >=1:
				self.y -=1
			elif dir in ['right', 2, 'd'] and self.y < self.belong.width -1:
				self.y +=1 
			self.available = True
		elif dir in [0, 'w']: 
			self.attack()
			self.available = not self.available
		# elif dir == 0 or dir == 'w':
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
		# return self.x >= self.belong.height -1 and self.collided == False
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



class Space():

	def __init__(self, height: int, width:int, num:int=0):
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
		self.invaders_num = num
		self.spaceship = None
		self.invaders = []
		self.eggs = []
		self.bullets = []
		self.figure = np.zeros((self.height, self.width), dtype=int)

	def show(self):
		"""
		Method show matrix represent position of all objects in space"""
		print(self.figure)
		


def invaders_initialize(space:'Space', num:int):
	"""
	Create <num> invaders satisfy restriction\\
	num: number of invaders"""
	cal = sorted(np.random.choice(range(space.width* 2), num, replace=False))
	for i in range(len(cal)):
		_ = Invader(cal[i]%2, cal[i]//2, space)


def environment_initialize(height:int, width:int, num:int):

	"""
	Create a space including ship, invaders satisfies restriction
	return space, ship, figure\\
		height: height of space
		width: 	width of space
		num:	number of invaders

	"""
	space = Space(height=height, width=width)
	ship_y = np.random.randint(width)
	space.spaceship = SpaceShip(x=height-1, y=ship_y, belong=space)
	invaders_initialize(space=space, num=num)

	return space, space.spaceship


def environment_changes(space:'Space', step:int):
	"""
	Action of all objects in space (excluding Agent)\\
	Actions of bullets, eggs, invaders\\ 
	Return None"""
	for egg in space.eggs.copy():
		egg.drop()
	for bullet in space.bullets.copy():
		bullet.move()
	
	#invader actions
	if step % 3 == 0:
		try:
			laying_invader = sorted(np.random.choice(range(len(space.invaders)), 3, replace=False))
			# if step % 3 == 0:
			for i in laying_invader:
				space.invaders[i].lay()
				
		except:
			for invader in space.invaders:
				invader.lay()


def check_collision(space:'Space'):
	"""
	Check for collision\\
	Remove object (excluding Agent) if any collision occurs\\
	Chech for collision of Agent
	Return True if Agent defeated\\
		 else Fasle (then continue game)"""
	for invader in space.invaders.copy():
		for bullet in space.bullets.copy():
			if bullet.collide(invader):
				space.bullets.remove(bullet)
				space.invaders.remove(invader)
				space.figure[bullet.x, bullet.y ] -=8
	for egg in space.eggs.copy():
		if space.spaceship.collide(egg):
			print(f'collision occurs at x= {space.spaceship.x} , y ={space.spaceship.y}')
			return True
	return False


def check_winning(space:'Space'):
	"""
	Check whether the Agent is winning
	Return True if not reach terminal state
		(Winning when number of invaders is 0)"""
	return space.invaders.__len__ == 0
