import pygame
import sys
import config
import robot_api
from config import colors
from ipcam import IPCamera
import cv2
from vision import detect_people, draw_boxes

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

        # Start IP camera
        self.camera = IPCamera(config.RTSP_URL)
        self.camera.start()

        # Image surface
        self.image_surface = pygame.Surface((config.IMAGE_SIZE, config.IMAGE_SIZE))
        self.image_rect = self.image_surface.get_rect()
        self.image_rect.midtop = (config.WINDOW_WIDTH // 2, 20)

        # Buttons
        self.buttons = self.create_buttons()

        self.frame_counter = 0
        self.detection_interval = config.DETECTION_INTERVAL  # Add to config.py, e.g., 5
        self.cached_boxes = []


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
                colors.BLUE, self.font, colors.WHITE
            )
            buttons.append(button)
        return buttons

    def handle_input(self, pos=None, key=None):
        direction = None

        if pos:
            for btn in self.buttons:
                if btn.is_clicked(pos):
                    direction = btn.label
                    break
        elif key:
            key_map = {
                pygame.K_LEFT: config.BTN_LABEL_LEFT,
                pygame.K_UP: config.BTN_LABEL_UP,
                pygame.K_DOWN: config.BTN_LABEL_DOWN,
                pygame.K_RIGHT: config.BTN_LABEL_RIGHT,
                pygame.K_SPACE: config.BTN_LABEL_STOP,
            }
            direction = key_map.get(key)

        if direction:
            print(f"Direction triggered: {direction}")
            robot_api.send_command(direction)

    #def update_image(self):
    #    frame = self.camera.get_frame()
    #    if frame is not None:
    #        self.frame_counter += 1
    #        if self.frame_counter % self.detection_interval == 0:
    #            frame = detect_people(frame)  # Only detect every N frames
    #        
    #        frame = cv2.resize(frame, (config.IMAGE_SIZE, config.IMAGE_SIZE))
    #        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #        pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    #        self.image_surface.blit(pygame_frame, (0, 0))
    def update_image(self):
        frame = self.camera.get_frame()
        if frame is None:
            return

        self.frame_counter += 1

        # Resize for detection (optional, or use full frame)
        detection_frame = cv2.resize(frame, (config.IMAGE_SIZE, config.IMAGE_SIZE))

        # Every N frames: run detection
        if self.frame_counter % self.detection_interval == 0:
            self.cached_boxes = detect_people(detection_frame)

        # Always draw (even on skipped frames)
        annotated = draw_boxes(detection_frame, self.cached_boxes)

        # Convert BGR to RGB for Pygame
        rgb_frame = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        pygame_frame = pygame.surfarray.make_surface(rgb_frame.swapaxes(0, 1))

        self.image_surface.blit(pygame_frame, (0, 0))


    def run(self):
        running = True
        while running:
            self.screen.fill(colors.BLACK)

            self.update_image()
            self.screen.blit(self.image_surface, self.image_rect)

            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_input(pos=event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_input(key=event.key)

            self.clock.tick(30)  # ~30 FPS

        self.camera.stop()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
