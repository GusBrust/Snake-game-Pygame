from project import *

def test_Snake():
    snake = Snake(50, (1280, 720))
    assert snake.block_size == 50
    assert snake.bounds == (1280,720)
    assert snake.body == [Rect(600,350,50,50)]
    assert snake.lenght == 1
    assert snake.direction == ()
    assert type(snake.pixel) == Rect

def test_Food():
    food = Food(50, (1280, 720))
    assert food.block_size == 50
    assert food.bounds == (1280,720)
    assert type(food.pixel) == Rect

def test_Main():
    game = Main()

def test_food_respawn():
    food = Food(50, (1280, 720))
    assert type(food.pixel) == type(py.Rect(1, 1, 1, 1))
    food_coords = food.pixel.topleft
    assert food.pixel.topleft == food_coords
    food.respawn()
    assert food.pixel.topleft != food_coords

def test_snake_check_eat():
    snake = Snake(50, (1280, 720))
    food = Food(50, (1280, 720))
    food_pixel_old = food.pixel
    assert snake.lenght == 1
    snake.pixel = food.pixel
    assert snake.check_eat(food) == True
    assert food.pixel != food_pixel_old
    assert snake.lenght == 2

def test_snake_direction():
    snake = Snake(50, (1280, 720))
    assert snake.direction == ()
    snake.direction = snake.DOWN
    assert snake.direction == (0, 50)

def test_snake_check_bound_collision1():
    snake = Snake(50, (1280, 720))
    assert snake.check_bound_collision() == False

def test_snake_check_bound_collision2():
    snake = Snake(50, (1280, 720))
    snake.pixel.topleft = (1300, 720)
    assert snake.check_bound_collision() == True

def test_snake_check_self_collision1():
    snake = Snake(50, (1280, 720))
    assert snake.check_self_collision() == False

def test_snake_check_self_collision2():
    snake = Snake(50, (1280, 720))
    snake.body.append(snake.pixel.copy())
    snake.lenght += 1
    assert snake.check_self_collision() == True