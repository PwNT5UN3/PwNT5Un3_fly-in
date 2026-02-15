import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

class Visualizer:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
    
    def run_gui(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # self.screen.fill("grey")
            pygame.draw.circle(self.screen, "green", (100, 100), 15)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
    
if __name__ == "__main__":
    gui = Visualizer()
    gui.run_gui()