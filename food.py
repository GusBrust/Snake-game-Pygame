import pygame as py
from pathlib import Path
from random import randrange


class Food:
    """
    A class that define the food element of the game.
    
    Attributes
    ----------
    block_size : int 
        Size of the screen pixel
    bounds : tuple[int]
        Width and height of game screen
    pixel : Rect
        Rect object of the food element

    Methods
    -------
    Draw(screen: pygame.Surface, asset_folder: Path)
        draw the apple image on the game screen
    Respawn()
        Generate a new random (x,y) coordinate for the food.pixel
        

    """

    def __init__(self, block_size: int, bounds: tuple[int]) -> None:
        """   
        Parameters
        ----------
        block_size : int 
            Size of the screen pixel
        bounds : tuple[int]
            Width and height of game screen
        """
        self.block_size = block_size
        self.bounds = bounds
        self.pixel = None
        self.respawn()
    
    def draw(self, screen: py.Surface, asset_folder: Path) -> None:
        """   
        Parameters
        ----------
        screen : Surface
            Surface of the game 
        asset_folder : Path
            Path of the asset folder
        """
        img = py.image.load(asset_folder/"apple.png")
        apple = py.transform.scale(img, (self.block_size, self.block_size))
        screen.blit(apple, self.pixel.topleft)

    def respawn(self) -> None:
        x, y = randrange(0, self.bounds[0], self.block_size), randrange(
            0, self.bounds[1], self.block_size
        )
        self.pixel = py.Rect(x, y, self.block_size, self.block_size)
