import os

from rich.console import Console
from rich.text import Text
from graph import Graph, Drone

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"
import pygame  # noqa: E402


class Visualizer:

    colors: dict[str, str] = {
        "green": "bright_green",
        "blue": "bright_blue",
        "red": "bright_red",
        "yellow": "bright_yellow",
        "orange": "orange3",
        "cyan": "bright_cyan",
        "purple": "blue_violet",
        "brown": "orange4",
        "lime": "chartreuse1",
        "magenta": "deep_pink3",
        "black": "black",
        "maroon": "dark_red",
        "gold": "gold3",
        "darkred": "red",
        "crimson": "dark_red",
    }

    rainbow: list[str] = [
        "bright_red",
        "orange3",
        "bright_yellow",
        "bright_green",
        "bright_blue",
        "blue_violet",
    ]

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

    @classmethod
    def print_coloured(cls, drone_id: str, network: Graph, node: str) -> None:
        console = Console()
        console.print(drone_id, "-", sep="", end="")
        zone = Text()
        for letter in range(len(node)):
            if network.get_zone(node).color == "rainbow":
                zone.append(
                    node[letter], style=cls.rainbow[letter % len(cls.rainbow)]
                )
            elif network.get_zone(node).color in cls.colors.keys():
                zone.append(
                    node[letter],
                    style=cls.colors[network.get_zone(node).color],
                )
            else:
                zone.append(node[letter])
        console.print(zone, end=" ")

    @staticmethod
    def print_movement_logs(
        drones: list[Drone], network: Graph, coloured: bool
    ):
        steps = len(drones[0].path) - 1
        for step in range(steps):
            for drone in drones:
                if drone.path[step] == drone.path[step + 1]:
                    continue
                if not coloured:
                    print(f"{drone.drone_id}-{drone.path[step + 1]}", end=" ")
                else:
                    Visualizer.print_coloured(
                        drone.drone_id, network, drone.path[step + 1]
                    )
            print()

    def run_gui(self) -> None:
        running = True
        self.clock.tick(60)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
            pygame.draw.circle(self.screen, "green", (100, 100), 15)
            pygame.display.flip()
            pygame.event.pump()
        pygame.quit()


if __name__ == "__main__":
    gui = Visualizer()
    gui.run_gui()
