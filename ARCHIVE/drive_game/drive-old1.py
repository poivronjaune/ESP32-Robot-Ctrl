import pygame
import config

# Alias for color constants
colors = config.colors

class Button:
    def __init__(self, x, y, width, height, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.highlight = False

    def draw(self, surface, font):
        color = colors.BTN_HIGHLIGHT if self.highlight else colors.BTN
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text_surf = font.render(self.label, True, colors.TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption(config.WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.running = True

        self.image_rect = self._create_image_rect()
        self.buttons = self._create_buttons()

    def _create_image_rect(self):
        x = (config.WINDOW_WIDTH - config.IMAGE_SIZE) // 2
        y = 30
        return pygame.Rect(x, y, config.IMAGE_SIZE, config.IMAGE_SIZE)

    def _create_buttons(self):
        labels = [
            config.BTN_LABEL_LEFT,
            config.BTN_LABEL_UP,
            config.BTN_LABEL_DOWN,
            config.BTN_LABEL_RIGHT
        ]
        btn_y = config.WINDOW_HEIGHT - config.BUTTON_HEIGHT - 30
        spacing = 20
        total_width = config.BUTTON_WIDTH * 4 + spacing * 3
        start_x = (config.WINDOW_WIDTH - total_width) // 2

        buttons = []
        for i, label in enumerate(labels):
            x = start_x + i * (config.BUTTON_WIDTH + spacing)
            button = Button(x, btn_y, config.BUTTON_WIDTH, config.BUTTON_HEIGHT, label)
            buttons.append(button)
        return buttons

    def draw_image_placeholder(self):
        pygame.draw.rect(self.screen, colors.PLACEHOLDER, self.image_rect, border_radius=12)
        text = self.font.render("Image Here", True, (200, 200, 200))
        rect = text.get_rect(center=self.image_rect.center)
        self.screen.blit(text, rect)

    def handle_input(self, pos=None, key=None):
        direction = None

        if pos:
            for btn in self.buttons:
                if btn.is_clicked(pos):
                    direction = btn.label
        elif key:
            key_map = {
                pygame.K_LEFT: config.BTN_LABEL_LEFT,
                pygame.K_UP: config.BTN_LABEL_UP,
                pygame.K_DOWN: config.BTN_LABEL_DOWN,
                pygame.K_RIGHT: config.BTN_LABEL_RIGHT,
            }
            direction = key_map.get(key)

        if direction:
            print(f"Direction triggered: {direction}")

    def update_highlights(self):
        keys = pygame.key.get_pressed()
        for btn in self.buttons:
            if btn.label == config.BTN_LABEL_LEFT:
                btn.highlight = keys[pygame.K_LEFT]
            elif btn.label == config.BTN_LABEL_UP:
                btn.highlight = keys[pygame.K_UP]
            elif btn.label == config.BTN_LABEL_DOWN:
                btn.highlight = keys[pygame.K_DOWN]
            elif btn.label == config.BTN_LABEL_RIGHT:
                btn.highlight = keys[pygame.K_RIGHT]
            else:
                btn.highlight = False

    def run(self):
        while self.running:
            self.screen.fill(colors.BG)
            self.draw_image_placeholder()
            self.update_highlights()

            for btn in self.buttons:
                btn.draw(self.screen, self.font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_input(key=event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_input(pos=event.pos)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    Game().run()
