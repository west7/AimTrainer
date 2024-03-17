import pygame
import math
import random
import time

pygame.init()

WIDTH, HEIGHT = 1200, 800

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 800
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30

LIVES = 5

FONT = pygame.font.SysFont("Arial", 22, True)
HEADER_HEIGHT = 40

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE
        
    def draw_target(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(window, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(window, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)


    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return dis <= self.size
    

def format_time(secs):
    millisec = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    min = int(secs // 60)

    return f"{min:02d}:{seconds:02d}.{millisec}"

def draw_header(window, targets_pressed, targets_missed, elapsed_time):
    pygame.draw.rect(window, "grey", (0, 0, WIDTH, HEADER_HEIGHT))

    time_label = FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")
    hits_label = FONT.render(f"Hits: {targets_pressed}", 1, "black" )
    lives_label = FONT.render(f"Lives: {LIVES - targets_missed}", 1, "black")

    window.blit(time_label, (5, 5))
    window.blit(hits_label, (180, 5))
    window.blit(lives_label, (285, 5))

def end_screen(window, elapsed_time, targets_pressed, targets_missed):
    window.fill("black")

    accuracy = round(targets_pressed / (targets_pressed + targets_missed) * 100, 1)

    time_label = FONT.render(f"Total Time: {format_time(elapsed_time)}", 1, "white")
    hits_label = FONT.render(f"Total Hits: {targets_pressed}", 1, "white" )
    accuracy_label = FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    window.blit(time_label, (get_middle(time_label), 200))
    window.blit(hits_label, (get_middle(hits_label), 300))
    window.blit(accuracy_label, (get_middle(accuracy_label), 400))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()


def get_middle(string):
    return WIDTH/2 - string.get_width()/2

def draw(window, targets):
    window.fill("black")

    for target in targets:
        target.draw_target(window)

def main():
    run = True

    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    targets_missed = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT: 
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + HEADER_HEIGHT, HEIGHT - TARGET_PADDING)

                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)  
                targets_missed += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

            if targets_missed >= LIVES:
                end_screen(window, elapsed_time, targets_pressed, targets_missed)


        draw(window, targets)
        draw_header(window, targets_pressed, targets_missed, elapsed_time)
        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()