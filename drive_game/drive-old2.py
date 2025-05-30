import pygame
import sys
import config
import robot_api  # Import robot control functions
from config import colors
import vision


# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, font, text_color):
        self.label = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.font = font
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        text_surf = self.font.render(self.label, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Main Game class
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(config.WINDOW_TITLE)
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        # Create and center image surface
        #self.image_surface = pygame.Surface((config.IMAGE_SIZE, config.IMAGE_SIZE))
        #self.image_surface.fill(colors.PLACEHOLDER)
        #self.image_rect = self.image_surface.get_rect()
        #self.image_rect.midtop = (config.WINDOW_WIDTH // 2, 20)

        self.image_surface = pygame.Surface((config.IMAGE_WIDTH, config.IMAGE_HEIGHT))
        self.image_surface.fill(colors.PLACEHOLDER)
        self.image_rect = self.image_surface.get_rect()
        self.image_rect.midtop = (config.WINDOW_WIDTH // 2, 20)


        # Create control buttons
        self.buttons = self.create_buttons()
        
        # Image courndown for grabbing next image from RTSP feed
        self.last_image_time = pygame.time.get_ticks()

    def create_buttons(self):
        labels = [
            config.BTN_LABEL_LEFT,
            config.BTN_LABEL_UP,
            config.BTN_LABEL_STOP,          
            config.BTN_LABEL_DOWN,
            config.BTN_LABEL_RIGHT,
        ]

        total_width = config.BUTTON_WIDTH * len(labels) + config.BUTTON_MARGIN * (len(labels) - 1)
        start_x = (config.WINDOW_WIDTH - total_width) // 2
        y = config.WINDOW_HEIGHT - config.BUTTON_HEIGHT - config.BUTTON_MARGIN

        buttons = []
        for i, label in enumerate(labels):
            x = start_x + i * (config.BUTTON_WIDTH + config.BUTTON_MARGIN)
            button = Button(
                label, x, y, config.BUTTON_WIDTH, config.BUTTON_HEIGHT,
                colors.BLUE if label != config.BTN_LABEL_STOP else (200, 50, 50),  # Stop button red
                self.font, 
                colors.WHITE
            )
            buttons.append(button)
        return buttons

    def handle_input(self, pos=None, key=None):
        direction = None

        if pos:
            for btn in self.buttons:
                if btn.is_clicked(pos):
                    direction = btn.label
                    break  # No need to check others
        elif key:
            key_map = {
                pygame.K_LEFT: config.BTN_LABEL_LEFT,
                pygame.K_UP: config.BTN_LABEL_UP,
                pygame.K_SPACE: config.BTN_LABEL_STOP,
                pygame.K_DOWN: config.BTN_LABEL_DOWN,
                pygame.K_RIGHT: config.BTN_LABEL_RIGHT,
            }
            direction = key_map.get(key)

        if direction:
            print(f"Direction triggered: {direction}")
            robot_api.send_command(direction)

    def run(self):
        running = True
        while running:
            self.screen.fill(colors.BLACK)

            # Draw image
            self.screen.blit(self.image_surface, self.image_rect)

            # Draw buttons
            for button in self.buttons:
                button.draw(self.screen)

            # Check if it's time to refresh the image
            current_time = pygame.time.get_ticks()
            if current_time - self.last_image_time >= config.IMAGE_REFRESH_MS:
                new_surface = vision.snap()
                if new_surface:
                    self.image_surface = new_surface
                self.last_image_time = current_time


            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_input(pos=event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_input(key=event.key)

            self.clock.tick(60)

        vision.release_camera()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
