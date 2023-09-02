# Example file showing a basic pygame "game loop"
import pygame

#define your classes here
class Player(pygame.Rect):
    def __init__(self, x, y):
        self.left = x
        self.top = y
        self.width = 100
        self.height = 100

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.screen.fill((128, 0, 200)) #Purple color
        
        #Render game here
    def run(self):
        while self.running:
            self.handle_events()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

#Create an instance of the Game class and run the game loop
if __name__ == "__main__":
    game = Game(1280, 720)
    game.run()