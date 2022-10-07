import sys
import pygame
import random

FPS = 60


class Button:
    button_group = []

    def __init__(self, text="button", left=0, top=0, width=60, height=60):
        Button.button_group.append(self)
        self.text = text
        self.rect = pygame.Rect(left, top, width, height)
        self.font = pygame.font.SysFont(None, 50)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center
        self.enabled = False

        self.margin_color = (0, 0, 255)
        self.fill_color = (100, 255, 255)
        self.margin_width = 1
        self.is_highlight = False
        self.highlight_color = (100, 255, 100)

    def set_rect(self, rect: pygame.Rect):
        self.rect = rect

    def set_margin_color(self, margin_color):
        self.margin_color = margin_color

    def set_fill_color(self, fill_color):
        self.fill_color = fill_color

    def set_is_highlight(self, is_highlight: bool):
        self.is_highlight = is_highlight

    def set_highlight_color(self, highlight_color):
        self.highlight_color = highlight_color

    def draw(self, surface):
        if self.is_highlight:
            pygame.draw.rect(surface, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(surface, self.fill_color, self.rect)
        pygame.draw.rect(surface, self.margin_color, self.rect, self.margin_width)
        screen.blit(self.text_surface, self.text_rect)

    def update(self):
        self.draw(screen)

    def is_hit(self, pos):  # 判断按钮是否被单机
        return self.rect.collidepoint(pos)

    def clicked(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("1")
        elif event.type == pygame.MOUSEBUTTONUP:
            print("2")
        elif event.type == pygame.MOUSEMOTION:
            print("3")


class PuzzlePart(Button):
    def __init__(self, text="puzzle", left=0, top=0, width=60, height=60):
        super().__init__(text, left, top, width, height)


class Puzzle:
    def __init__(self):
        self.length = window_height - 40
        self.part_length = self.length
        self.rect = pygame.Rect(20, 20, self.length, self.length)
        self.group = []
        self.n = 3
        self.reset()

    def reset(self, n=3):
        self.n = n
        self.group.clear()
        self.part_length = self.length // n
        for i in range(0, n * n - 1):
            self.group.append(
                PuzzlePart(str(i + 1), 20 + (i % n) * self.part_length, 20 + (i // n) * self.part_length,
                           self.part_length, self.part_length))

    def pos2num(self, pos):
        if self.rect.collidepoint(pos):
            pos = (pos[0] - 20, pos[1] - 20)
            return (pos[1] // self.part_length) * self.n + pos[0] // self.part_length
        return -1

    def num2rect(self, num):
        return pygame.Rect(20 + (num % self.n) * self.part_length, 20 + (num // self.n) * self.part_length,
                           self.part_length, self.part_length)

    def update(self):
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(19, 19, self.length, self.length), 2)
        for part in self.group:
            part.update()


def screen_update():
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
    screen.fill((255, 255, 255))
    puzzle = Puzzle()
    puzzle.update()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                for button in Button.button_group:
                    if button.is_hit(event.pos):
                        button.set_is_highlight(True)
                    else:
                        button.set_is_highlight(False)
                print(puzzle.pos2num(event.pos))
        screen_update()
