# Example file showing a basic pygame "game loop"
import pygame
from entities.Tower import MainTower
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


class Game:
    def __init__(self) -> None:
        self.screen = screen


game = Game()

# define your objects here
player = MainTower("red", x=300, y=300, game=game, life_points=100)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    player.draw()
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
