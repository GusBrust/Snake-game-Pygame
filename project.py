import pygame as py
from pygame.locals import *
import sys
from button import Button
from pathlib import Path
from snake import Snake
from food import Food


class Main:
    WHITE_score = (255, 255, 255, 120)
    LIGHT_GREEN = (0, 200, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (2, 69, 27)
    LIGHT_GRAY = (128, 128, 128, 64)
    PURPLE = (81, 0, 97)
    block_size = 50
    screen_size = (1280, 720)
    # Ajust the size to a multiplicator of block size
    screen_size = (
        (screen_size[0] - screen_size[0] % block_size),
        (screen_size[1] - screen_size[1] % block_size),
    )
    global asset_folder
    asset_folder = Path("assets/")
    FPS = 10

    def __init__(self) -> None:
        py.init()
        self.surface = py.Surface(self.screen_size, py.SRCALPHA)
        self.screen = py.display.set_mode(self.screen_size)
        self.clock = py.time.Clock()
        global food
        food = Food(self.block_size, self.screen_size)
        global snake
        snake = Snake(self.block_size, self.screen_size)

    def new_game(self):
        py.display.set_caption("Snake Game")
        run = True
        while run:
            self.clock.tick(self.FPS)
            # Check for events of quit and <esc> to go back to menu
            for event in py.event.get():
                if event.type == QUIT:
                    py.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    run = False

            self.screen.fill(self.DARK_GREEN)
            self.screen.blit(self.surface, (0, 0))
            self.grid()

            snake.draw(self.screen)
            food.draw(self.screen, asset_folder)
            snake.check_keys()
            snake.move()
            eat = snake.check_eat(food)
            if snake.check_bound_collision():
                self.game_over()
            if snake.check_self_collision() and not eat:
                self.game_over()

            self.score()
            py.display.update()

    def get_font(self, size):
        return py.font.Font(asset_folder/"font.ttf", size)

    def score(self):
        font = self.get_font(30)
        # if snake.lenght == None
        score = f"Score: {(snake.lenght-1)*10}"
        text = font.render(score, True, self.WHITE_score)
        text_rect = text.get_rect()
        text_rect.topright = (self.screen_size[0] - 20, 20)
        self.screen.blit(text, text_rect)

    def main_menu(self):
        WINDOW_NAME = "Snake Menu"
        SCREEN_MENU = py.display.set_mode(self.screen_size)
        IMAGE_BACKGROUND = py.image.load(asset_folder/"backgroud.jpg")
        py.display.set_caption(WINDOW_NAME)

        run = True
        while run:
            SCREEN_MENU.blit(IMAGE_BACKGROUND, (0, 0))
            MENU_MOUSE_POS = py.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render(
                "Main Menu", True, self.PURPLE)
            MENU_RECT = MENU_TEXT.get_rect(
                center=(self.screen_size[0] / 2, self.screen_size[1] * 0.2)
            )

            PLAY_BUTTON = Button(
                image=py.image.load(asset_folder/"Rect.png"),
                pos=(self.screen_size[0] / 2, self.screen_size[1] * 0.45),
                text_input="PLAY",
                font=self.get_font(75),
                base_color=self.PURPLE,
                hovering_color="White",
            )
            QUIT_BUTTON = Button(
                image=py.image.load(asset_folder/"Rect.png"),
                pos=(self.screen_size[0] / 2, self.screen_size[1] * 0.7),
                text_input="QUIT",
                font=self.get_font(75),
                base_color=self.PURPLE,
                hovering_color="White",
            )

            SCREEN_MENU.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN_MENU)

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                if event.type == py.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.new_game()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        py.quit()
                        sys.exit()
            py.display.flip()

    def game_over(self):
        WINDOW_NAME = "Snake Game"
        py.display.set_caption(WINDOW_NAME)

        run = True
        while run:
            MENU_MOUSE_POS = py.mouse.get_pos()
            MENU_TEXT = self.get_font(100).render(
                "Game over", True, self.PURPLE)
            MENU_RECT = MENU_TEXT.get_rect(
                center=(self.screen_size[0] / 2, self.screen_size[1] * 0.3)
            )
            rect_image = py.image.load(asset_folder/"Rect.png")
            rect_image = py.transform.scale(rect_image, (520, 110))
            PLAY_BUTTON = Button(
                image=rect_image,
                pos=(self.screen_size[0] * 0.3, self.screen_size[1] * 0.6),
                text_input="PLAY AGAIN",
                font=self.get_font(50),
                base_color=self.PURPLE,
                hovering_color="White",
            )
            QUIT_BUTTON = Button(
                image=py.image.load(asset_folder/"Rect.png"),
                pos=(self.screen_size[0] * 0.75, self.screen_size[1] * 0.6),
                text_input="QUIT",
                font=self.get_font(50),
                base_color=self.PURPLE,
                hovering_color="White",
            )

            self.score()
            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                if event.type == py.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        snake.respawn()
                        food.respawn()
                        self.new_game()
                        run = False
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        py.quit()
                        sys.exit()
            py.display.update()

    def grid(self):
        """Draw a grid"""
        for y in range(0, self.screen_size[1], self.block_size):
            py.draw.line(
                self.surface,
                self.LIGHT_GRAY,
                start_pos=(0, y),
                end_pos=(self.screen_size[0], y),
            )
        for x in range(self.block_size, self.screen_size[0], self.block_size):
            py.draw.line(
                self.surface,
                self.LIGHT_GRAY,
                start_pos=(x, 0),
                end_pos=(x, self.screen_size[1]),
            )

    def run(self):
        self.main_menu()


if __name__ == "__main__":
    game = Main()
    game.run()
