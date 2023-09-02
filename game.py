# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#define your classes here
class Player(pygame.Rect):
    def __init__(self, x, y):
        self.left = x
        self.top = y
        self.width = 100
        self.height = 100

        

#define your objects here
player = Player(500, 350)
player2 = Player(40, 600)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen, "blue", player)
    pygame.draw.rect(screen, "red", player2)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()   