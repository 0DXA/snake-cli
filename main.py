import os
import random
import keyboard
import time


class GameObject(object):

    def __init__(self, x, y):
        self.x, self.y = x, y

    def get_coordinates(self):
        return self.x, self.y

    def set_coordinates(self, x, y):
        self.x, self.y = x, y


class Snake(GameObject):

    def __init__(self, x, y, age):
        super().__init__(x, y)
        self.age = age

    def set_age(self, age):
        self.age = age

    def get_age(self):
        return self.age


class Food(GameObject):

    def __init__(self, x, y, points=1):
        super().__init__(x, y)
        assert points > 0
        self.points = points

    def get_points(self):
        return self.points


class Player(object):

    def __init__(self, x, y, rotation="N", segments=3):
        self.snake = []
        for i in range(segments):
            self.snake.append(Snake(x, y - segments, segments - i))
        self.rotation = rotation
        self.age = segments
        for i in range(segments):
            self.move()

    def turn(self, rotation):
        assert rotation in ["N", "S", "W", "E"]
        self.rotation = rotation

    def move(self):
        head_x, head_y = self.snake[0].get_coordinates()
        if self.rotation == "S":
            new_x, new_y = head_x, head_y + 1
        elif self.rotation == "N":
            new_x, new_y = head_x, head_y - 1
        elif self.rotation == "W":
            new_x, new_y = head_x - 1, head_y
        elif self.rotation == "E":
            new_x, new_y = head_x + 1, head_y
        else:
            raise ValueError

        for i in self.snake:
            if i.get_coordinates() == (new_x, new_y) and i.get_age() > 0:
                return 1
            i.set_age(i.get_age() - 1)
            if i.get_age() == -1:
                self.snake.remove(i)
        self.snake.insert(0, Snake(new_x, new_y, self.age))
        return 0

    def grow(self):
        self.age += 1
        for i in self.snake:
            i.set_age(i.get_age() + 1)

    def get_coordinates(self):
        return self.snake[0].get_coordinates()

    def kill(self):
        self.age -= 1
        for i in self.snake:
            i.set_age(i.get_age() - 1)
        if self.age == 0:
            return 1
        else:
            return 0

    def check_coordinates(self, x, y):
        for i in self.snake:
            if i.get_coordinates() == (x, y):
                return True
        else:
            return False


class Game(object):

    def __init__(self, width, height):
        self.player = Player(width // 2, height // 2)
        self.width, self.height = width, height

        self.score = 0
        self.food = None

    def spawn_food(self):
        self.food = Food(random.randint(1, self.width - 2), random.randint(1, self.height - 2))
        x, y = self.food.get_coordinates()
        if self.player.check_coordinates(x, y):
            return 1
        else:
            return 0

    def food_check(self):
        x, y = self.food.get_coords()
        if self.player.check_coordinates(x, y):
            self.player.grow()
            self.score += 1
            self.food = None

    def wall_death(self):
        x, y = self.player.get_coordinates()
        if (x in range(0, self.width)) and (y in range(0, self.height)):
            return 0
        else:
            self.score = -1

    def draw(self):
        field = [["◌" for _ in range(self.width)] for _ in range(self.height)]
        for i in self.player.snake:
            if i.get_age() > 0:
                x, y = i.get_coordinates()
                field[y][x] = "◍"
        x, y = self.food.get_coordinates()
        field[y][x] = "●"
        os.system("clear")
        print(self.score, self.player.get_coordinates(), self.food.get_coords())
        for i in field:
            print(*i)

    def run(self, rotation=None):
        if self.food is None:
            temp = 1
            while temp == 1:
                temp = self.spawn_food()
        self.draw()
        if rotation is not None:
            self.player.turn(rotation)
        response = self.player.move()
        self.wall_death()
        self.food_check()
        if response > 0:
            self.score = -1
        return self.score


class Keyboard(object):

    @staticmethod
    def handler():
        if keyboard.is_pressed("w"):
            a = "N"
        elif keyboard.is_pressed("a"):
            a = "W"
        elif keyboard.is_pressed("s"):
            a = "S"
        elif keyboard.is_pressed("d"):
            a = "E"
        else:
            a = 1

        return a


if __name__ == "__main__":
    score = 0
    app = Game(30, 30)
    key = Keyboard()
    cnt = 0
    flag = True
    while score > -1:
        time.sleep(0.001)
        cnt += 1
        if flag:
            last_key = key.handler()
            if last_key is not None:
                flag = False
        if last_key is None:
            flag = True

        if cnt == 200 // (1 + 0.1 * score):
            cnt = 0
            score = app.run(last_key)
            last_key = None
            flag = True
    print("GAME OVER")
