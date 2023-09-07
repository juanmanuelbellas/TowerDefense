import pygame
from entities.Tower import MainTower, SecondaryTower
from messages import welcome_message, game_over_message, tower_placement_limit_exceeded_message, tower_placement_available_message
from entities.enemies import Enemy


# Define your classes here
class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks=pygame.time.get_ticks()
        self.running = True
        self.entities = []
        self.secondary_towers = [] 
        self.bullets=[] # List to store secondary towers
        self.cantupdates=0

        # Initialize Pygame
        pygame.init()

        # Create a font object and store it as an instance variable
        self.font = pygame.font.Font(None, 72)  # Choose font and font size

        # Welcome message variables
        self.display_welcome_message = True  # Display the welcome message initially
        self.initial_display_done = False  # Flag to control the initial display
        # 2000 milliseconds (2 seconds)
        self.welcome_message_display_duration = 2000
        # Initialize with current time
        self.welcome_message_start_time = pygame.time.get_ticks()
        self.welcome_message_delay = 1000  # Delay in milliseconds (1 second)

        # Create a MainTower object and set its game attribute
        self.player = MainTower((50, 125, 207), x=300, y=300, life_points=100)



        # Create SecondaryTower limit
        self.tower_placement_limit = 1
        self.tower_placement_cooldown = 20
        self.last_tower_placement_time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                current_time = pygame.time.get_ticks()
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if current_time - self.last_tower_placement_time >= self.tower_placement_cooldown:
                    # Left mouse button clicked

                    # Create a SecondaryTower object at the mouse click position
                    secondary_tower = SecondaryTower(
                        (64, 50, 66), x=mouse_x, y=mouse_y, life_points=50, game=self)
                    self.secondary_towers.append(secondary_tower)
                    self.last_tower_placement_time = current_time
                else:
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # for dev purposes only
                self.entities.append(
                    Enemy("red", 10, self, x=mouse_x, y=mouse_y))

    def update(self):

        # Check for elapsed time and update tower placement limit
        current_time = pygame.time.get_ticks()
        if current_time - self.last_tower_placement_time >= self.tower_placement_cooldown:
            self.tower_placement_limit += 1
            self.last_tower_placement_time = current_time

    def render(self):
        self.screen.fill((204, 193, 163))  # Background color
        # Render game here

        for entity in self.entities:
            entity.update()
            entity.draw()
        self.player.draw(self.screen)  # Pass the screen to the draw method
        # Render secondary towers
        for bullet in self.bullets:
            bullet.update()
            bullet.draw()

        for secondary_tower in self.secondary_towers:
            # Pass the screen to the draw method
            secondary_tower.draw(self.screen)
            secondary_tower.update()

        # Check if it's time to display the welcome message
        current_time = pygame.time.get_ticks()

        if self.display_welcome_message:
            elapsed_time = current_time - self.welcome_message_start_time

            if not self.initial_display_done:
                # Display the message initially for the specified duration
                if elapsed_time >= self.welcome_message_display_duration:
                    self.initial_display_done = True
                    self.welcome_message_start_time = current_time
            else:
                # After the initial display, hide the message after the delay
                if elapsed_time >= self.welcome_message_delay:
                    self.display_welcome_message = False

            # Render the message with a constant alpha value
            text_render = self.font.render(
                welcome_message, True, (255, 255, 255))
            text_rect = text_render.get_rect()
            # Center the text on the screen
            text_rect.center = (self.width // 2, self.height // 2)

            # Blit (draw) the text surface onto the screen
            self.screen.blit(text_render, text_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.cantupdates+=1
            self.handle_events()
            self.render()
            self.clock.tick(60)


# Run the game loop
if __name__ == "__main__":
    game = Game(1280, 720)
    game.run()
