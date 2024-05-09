from food import Food
import pygame as py
from pygame.locals import *


class Snake:
    """
    Define the snake element of the game

    Attributes
    ----------
    block_size : int 
        Size of the screen pixel
    bounds : tuple[int]
        Width and height of game screen
    pixel : Rect
        Rect object of the Snake element
    direction : Tuple
        Direction of the snake
    lenght : int
        Lenght of the snake
    body : list[Rect]
        List of Rect Objects of the all snake body

    Methods
    -------
    respawn()
        Generate the start coordinates for the snake.pixel at
        the center of the screen and restore default values for the snake
        on the start of a new game
    draw(screen: Surface)
        Draw the snake on the game screen
    check_eat(food: Food)
        Checks if the snake has eaten the food
    move()
        Moves the snake in the game
    check_self_collision()
        Checks if the snake collide with its body
    check_bound_collision()
        Checks if the snake has collide with the game screen boundaries
    check_keys()
        Checks the keys pressed and change the direction of the snake
    """
    
    GREEN = (0, 255, 0)
    LIGHT_GREEN = (0, 200, 0)

    def __init__(self, block_size: int, bounds: tuple[int]) -> None:
        # Size of snake square
        self.block_size = block_size
        # Direction of the snake movement
        self.direction = ()
        # Size of snake
        self.lenght = None
        # Snake rect. pixel
        self.pixel = py.Rect(0, 0, self.block_size, self.block_size)
        # List of the (x,y) rects object of the snake
        self.body = []
        # Limits of the screen
        self.bounds = bounds
        self.respawn()

        # Directions
        self.UP = (0, -block_size)
        self.DOWN = (0, block_size)
        self.LEFT = (-block_size, 0)
        self.RIGHT = (block_size, 0)

    def respawn(self):
        self.lenght = 1
        # Middle of the screen
        x, y = (
            (self.bounds[0] // self.block_size // 2 * self.block_size),
            (self.bounds[1] // self.block_size // 2 * self.block_size),
        )
        self.direction = ()
        self.body = []
        self.pixel.topleft = (x, y)
        self.body.append(self.pixel.copy())

    def draw(self, screen: py.Surface):
        for n, segment in enumerate(self.body):
            py.draw.rect(
                screen,
                self.GREEN,
                segment,
                border_radius=10
            )
            py.draw.rect(
                screen,
                self.LIGHT_GREEN,
                (segment.x + 3, segment.y + 3,
                 segment.width - 6, segment.height - 6),
                border_radius=10
            )

    def check_eat(self, food: Food):
        head = self.pixel
        if food.pixel.contains(head):
            self.lenght += 1
            self.body.append(self.pixel.copy())
            food.respawn()
            return True
        return False

    def move(self):
        if not self.direction:
            return
        self.pixel.move_ip(self.direction)
        self.body.append(self.pixel.copy())
        self.body = self.body[-self.lenght:]

    def check_self_collision(self):
        head = self.pixel
        for segment in self.body[: self.lenght - 1]:
            if head.contains(segment):
                return True
        return False

    def check_bound_collision(self):
        head = self.pixel
        screen = Rect(0, 0, self.bounds[0], self.bounds[1])
        if not screen.contains(head):
            return True
        else:
            return False

    def check_keys(self):
        # check keys pressed
        keys = py.key.get_pressed()
        if (keys[K_UP] or keys[K_w]) and (self.direction != self.DOWN):
            self.direction = self.UP
        elif (keys[K_DOWN] or keys[K_s]) and (self.direction != self.UP):
            self.direction = self.DOWN
        elif (keys[K_LEFT] or keys[K_a]) and (self.direction != self.RIGHT):
            self.direction = self.LEFT
        elif (keys[K_RIGHT] or keys[K_d]) and (self.direction != self.LEFT):
            self.direction = self.RIGHT
