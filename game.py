import pygame
from entities.Tower import MainTower, SecondaryTower
from messages import welcome_message, game_over_message, tower_placement_limit_exceeded_message, tower_placement_available_message

# Define your classes here
class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize Pygame
        pygame.init()

        # Create a font object and store it as an instance variable
        self.font = pygame.font.Font(None, 72)  # Choose font and font size

        # Welcome message variables
        self.display_welcome_message = True  # Display the welcome message initially
        self.initial_display_done = False  # Flag to control the initial display
        self.welcome_message_display_duration = 2000  # 2000 milliseconds (2 seconds)
        self.welcome_message_start_time = pygame.time.get_ticks()  # Initialize with current time
        self.welcome_message_delay = 1000  # Delay in milliseconds (1 second)

        # Create a MainTower object and set its game attribute
        self.player = MainTower((50, 125, 207), x=300, y=300, life_points=100)

        self.secondary_towers = []  # List to store secondary towers

        # Create SecondaryTower limit
        self.tower_placement_limit = 1
        self.tower_placement_cooldown = 20000
        self.last_tower_placement_time = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_tower_placement_time >= self.tower_placement_cooldown:
                    # Left mouse button clicked
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Create a SecondaryTower object at the mouse click position
                    secondary_tower = SecondaryTower((64, 50, 66), x=mouse_x, y=mouse_y, life_points=50)
                    self.secondary_towers.append(secondary_tower)
                    self.last_tower_placement_time = current_time
                else:
                    pass

    def update(self):
        # Check for elapsed time and update tower placement limit
        current_time = pygame.time.get_ticks()
        if current_time - self.last_tower_placement_time >= self.tower_placement_cooldown:
            self.tower_placement_limit += 1
            self.last_tower_placement_time = current_time

    def render(self):
        self.screen.fill((204, 193, 163))  # Background color
        # Render game here
        self.player.draw(self.screen)  # Pass the screen to the draw method
        # Render secondary towers
        for secondary_tower in self.secondary_towers:
            secondary_tower.draw(self.screen)  # Pass the screen to the draw method

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
            text_render = self.font.render(welcome_message, True, (255, 255, 255))
            text_rect = text_render.get_rect()
            text_rect.center = (self.width // 2, self.height // 2)  # Center the text on the screen

            # Blit (draw) the text surface onto the screen
            self.screen.blit(text_render, text_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(60)

# Run the game loop
if __name__ == "__main__":
    game = Game(1280, 720)
    game.run()
