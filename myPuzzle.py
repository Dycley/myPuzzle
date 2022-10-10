import sys
import pygame
import random

FPS = 60
BACKCOLOR = (255, 255, 255)


class Button:
    button_group = []

    def __init__(self, text="button", left=0, top=0, width=60, height=60):
        Button.button_group.append(self)
        self.text = text
        self.rect = pygame.Rect(left, top, width, height)
        self.font = pygame.font.SysFont("华文行楷", 50)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center
        self.enabled = False

        self.margin_color = (0, 0, 255)
        self.fill_color = (100, 255, 255)
        self.margin_width = 1
        self.is_highlight = False
        self.highlight_color = (100, 255, 100)

    def draw(self, surface):
        if self.is_highlight:
            pygame.draw.rect(surface, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(surface, self.fill_color, self.rect)
        pygame.draw.rect(surface, self.margin_color, self.rect, self.margin_width)
        self.text_rect.center = self.rect.center
        screen.blit(self.text_surface, self.text_rect)

    def update(self):
        self.draw(screen)

    def is_hit(self, pos):  # 判断按钮是否被单机
        return self.rect.collidepoint(pos)

    def hide(self):
        self.fill_color = BACKCOLOR
        self.text_surface = self.font.render(self.text, False, BACKCOLOR)
        self.highlight_color = BACKCOLOR

    @staticmethod
    def highlight():
        for button in Button.button_group:
            if button.is_hit(event.pos):
                button.is_highlight = True
            else:
                button.is_highlight = False


class PuzzlePart(Button):
    def __init__(self, text="puzzle", left=0, top=0, width=60, height=60):
        super().__init__(text, left, top, width, height)
        self.id = -1


class Puzzle:
    def __init__(self):
        self.length = window_height - 40
        self.part_length = self.length
        self.rect = pygame.Rect(20, 20, self.length, self.length)
        self.group = []
        self.arr = []
        self.n = 3
        self.space_pos = -1  # 空格的位置
        self.reset()

    def reset(self, n=3):
        self.n = n
        self.group.clear()
        self.part_length = self.length // n
        for i in range(0, n * n):
            puzzle_part = PuzzlePart(str(i + 1), 20 + (i % n) * self.part_length, 20 + (i // n) * self.part_length,
                                     self.part_length, self.part_length)
            self.group.append(puzzle_part)
            puzzle_part.id = i
        self.new()

    def pos2num(self, pos):
        if self.rect.collidepoint(pos):
            pos = (pos[0] - 20, pos[1] - 20)
            return (pos[1] // self.part_length) * self.n + pos[0] // self.part_length
        return -1

    def num2rect(self, num):
        return pygame.Rect(20 + (num % self.n) * self.part_length, 20 + (num // self.n) * self.part_length,
                           self.part_length, self.part_length)

    def new(self):
        num = self.n ** 2
        self.group = random.sample([i for i in self.group], num)
        for i, part in enumerate(self.group):
            if part.id == num - 1:
                part.hide()
                self.space_pos = i
                # if i - self.n >= 0:
                #     self.group[i - self.n].set_enabled(True)
                # if i + self.n < num:
                #     self.group[i + self.n].set_enabled(True)
                # if i % self.n > 0:
                #     self.group[i - 1].set_enabled(True)
                # if i % self.n < self.n - 1:
                #     self.group[i + 1].set_enabled(True)
        # 数字华容道，必然有解，只存在于如下3个细分情形：
        #
        # 若格子列数为奇数，则逆序数必须为偶数；
        # 若格子列数为偶数，且逆序数为偶数，则当前空格所在行数与初始空格所在行数的差为偶数；
        # 若格子列数为偶数，且逆序数为奇数，则当前空格所在行数与初始空格所在行数的差为奇数。
        arr = [i.id for i in self.group]
        cnt = 0  # 求逆序数
        for i in range(1, num):
            for j in range(i):
                if arr[j] > arr[i]:
                    cnt += 1
        space_delta = self.n - self.space_pos // self.n - 1  # 当前空格所在行数与初始空格所在行数的差
        print(space_delta, (cnt % 2) ^ (space_delta % 2) ^ 1)
        if (self.n % 2 and cnt % 2) or (
                self.n % 2 == 0 and (cnt % 2 == 0 and space_delta % 2 or cnt % 2 and space_delta % 2 == 0)):
            if self.space_pos >= self.n:
                self.group[0], self.group[1] = self.group[1], self.group[0]
            else:
                self.group[self.n], self.group[self.n + 1] = self.group[self.n + 1], self.group[self.n]
        for i, part in enumerate(self.group):
            part.rect = self.num2rect(i)
        print(cnt, arr)

    def slide(self, pos):
        print(self.pos2num(pos))
        clicked_pos = self.pos2num(pos)
        if clicked_pos + self.n == self.space_pos or clicked_pos - self.n == self.space_pos or (
                self.space_pos % self.n < self.n and clicked_pos == self.space_pos - 1) or (
                self.space_pos % self.n >= 0 and clicked_pos == self.space_pos + 1):
            self.group[clicked_pos], self.group[self.space_pos] = self.group[self.space_pos], self.group[clicked_pos]
            self.space_pos = clicked_pos
        for i, part in enumerate(self.group):
            part.rect = self.num2rect(i)

    def judge_win(self):
        for i, part in enumerate(self.group):
            if i != part.id:
                return False
        print("win")
        return True

    def update(self):
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(19, 19, self.length, self.length), 2)
        for i, part in enumerate(self.group):
            part.update()


class Menu:
    def __init__(self):
        self.new_game = Button("新游戏", 610, 50, 150, 50)

    def update(self):
        self.new_game.update()


def screen_update():
    screen.fill(BACKCOLOR)
    menu.update()
    puzzle.update()
    pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    size = window_width, window_height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("MyPuzzle")
    icon = pygame.image.load("images/puzzle.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    menu = Menu()
    puzzle = Puzzle()
    screen_update()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                Button.highlight()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if puzzle.rect.collidepoint(event.pos):
                    puzzle.slide(event.pos)
                    puzzle.judge_win()
                elif menu.new_game.is_hit(event.pos):
                    print("new game")
                    puzzle.reset(2)
        screen_update()
