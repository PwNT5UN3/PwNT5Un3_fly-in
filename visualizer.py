import os

from rich.console import Console
from rich.text import Text
from graph import Graph, Drone, ZoneType

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"
import pygame  # noqa: E402


class Visualizer:
    """The visual aspects (gui and log prints)"""

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
        "violet": "dark_violet",
    }

    rainbow: list[str] = [
        "bright_red",
        "orange3",
        "bright_yellow",
        "bright_green",
        "bright_blue",
        "blue_violet",
    ]

    colors_rgb: dict[str, tuple[int, int, int]] = {
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "red": (255, 0, 0),
        "yellow": (255, 255, 0),
        "orange": (255, 165, 0),
        "cyan": (0, 255, 255),
        "purple": (128, 0, 128),
        "brown": (165, 42, 42),
        "lime": (50, 205, 50),
        "magenta": (255, 0, 255),
        "black": (0, 0, 0),
        "maroon": (128, 0, 0),
        "gold": (255, 215, 0),
        "darkred": (139, 0, 0),
        "crimson": (220, 20, 60),
        "violet": (175, 0, 215),
        "bg": (30, 30, 30),
        "drone": (167, 166, 186),
    }

    def __init__(self) -> None:
        """Inits the gui aspects like the pygame display"""
        pygame.init()
        self.x_len = 1600
        self.y_len = 900
        self.screen = pygame.display.set_mode((self.x_len, self.y_len))
        self.clock = pygame.time.Clock()

    def buffer_zone_positions(self, network: Graph) -> None:
        """readjusts all zone coordinates to fit evenly on the screen"""
        all_x_pos = list(
            enumerate(sorted(set(map(lambda x: x.x, network.get_all_zones()))))
        )
        all_y_pos = list(
            enumerate(sorted(set(map(lambda x: x.y, network.get_all_zones()))))
        )
        scale_factor_x = int(self.x_len / (len(all_x_pos) + 1))
        scale_factor_y = int(self.y_len / (len(all_y_pos) + 1))
        scaled_x_pos = {}
        scaled_y_pos = {}
        for pos in all_x_pos:
            scaled_x_pos[pos[1]] = (pos[0] + 1) * scale_factor_x
        for pos in all_y_pos:
            scaled_y_pos[pos[1]] = (pos[0] + 1) * scale_factor_y
        for node in network.get_all_zones():
            node.x = scaled_x_pos[node.x]
            node.y = scaled_y_pos[node.y]

    @classmethod
    def print_coloured(cls, drone_id: str, network: Graph, node: str) -> None:
        """prints a log in color"""
        console = Console()
        console.print(drone_id, "-", sep="", end="")
        zone = Text()
        for letter in range(len(node)):
            if "-" in node:
                zone.append(node[letter], style="grey54")
            elif network.get_zone(node).color == "rainbow":
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
    ) -> None:
        """
        prints the movement logs,
        uses print_coloured() if couloured is set to True
        """
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

    @staticmethod
    def avg_rgb_bigger_than_80(rgb: tuple[int, int, int]) -> bool:
        """
        returns True if the aberage of the rgb values given is bigger than 80
        """
        avg = (rgb[0] + rgb[1] + rgb[2]) / 3
        return avg >= 80

    def run_gui(self, drones: list[Drone], network: Graph) -> None:
        """runs the visual representation using pygame"""
        running = True
        rainbow = [255.0, 0.0, 0.0]
        rainbow_smooth = [0, 0, 0]
        self.clock.tick(60)
        self.buffer_zone_positions(network)
        turn = 0
        font = pygame.font.Font(None, size=32)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        turn = 0
                    elif (
                        event.key == pygame.K_RIGHT
                        and turn < len(drones[0].path) - 1
                    ):
                        turn += 1
                    elif event.key == pygame.K_LEFT and turn > 0:
                        turn -= 1
            turn_text = f"Positions after turn: {turn}"
            turn_sign = font.render(turn_text, True, (255, 255, 255))
            self.screen.fill(color=Visualizer.colors_rgb["bg"])
            self.screen.blit(turn_sign, (10, 10))
            for zone in network.get_all_zones():
                if zone.color == "rainbow":
                    rainbow_smooth.clear()
                    for num in rainbow:
                        rainbow_smooth.append(num.__floor__())
                    pygame.draw.circle(
                        self.screen,
                        tuple(rainbow_smooth),
                        (zone.x, zone.y),
                        16,
                    )
                    if rainbow[0] == 255:
                        if rainbow[1] == 255:
                            rainbow[0] -= 1.5
                        elif rainbow[2] != 0:
                            rainbow[2] -= 1.5
                        else:
                            rainbow[1] += 1.5
                    elif rainbow[1] == 255:
                        if rainbow[0] != 0:
                            rainbow[0] -= 1.5
                        elif rainbow[2] == 255:
                            rainbow[1] -= 1.5
                        else:
                            rainbow[2] += 1.5
                    else:
                        if rainbow[1] != 0:
                            rainbow[1] -= 1.5
                        else:
                            rainbow[0] += 1.5
                else:
                    pygame.draw.circle(
                        self.screen,
                        Visualizer.colors_rgb.get(zone.color, (255, 255, 255)),
                        (zone.x, zone.y),
                        16,
                    )
                if zone.type == ZoneType.PRIO:
                    text = "P"
                elif zone.type == ZoneType.RESTRICTED:
                    text = "R"
                elif zone.type == ZoneType.BLOCKED:
                    text = "B"
                else:
                    text = "N"
                text_surface = font.render(
                    text,
                    True,
                    (
                        (0, 0, 0)
                        if self.avg_rgb_bigger_than_80(
                            Visualizer.colors_rgb.get(
                                zone.color, (255, 255, 255)
                            )
                        )
                        else (255, 255, 255)
                    ),
                )
                self.screen.blit(text_surface, (zone.x - 7, zone.y - 8))
            for connection in network.get_all_links():
                pygame.draw.aaline(
                    self.screen,
                    (100, 100, 100),
                    (
                        network.get_zone(connection.zone_1).x,
                        network.get_zone(connection.zone_1).y,
                    ),
                    (
                        network.get_zone(connection.zone_2).x,
                        network.get_zone(connection.zone_2).y,
                    ),
                )
            for drone in drones:
                if "-" in drone.path[turn]:
                    lower_pos_x = min(
                        [
                            network.get_zone(drone.path[turn].split("-")[1]).x,
                            network.get_zone(drone.path[turn].split("-")[0]).x,
                        ]
                    )
                    lower_pos_y = min(
                        [
                            network.get_zone(drone.path[turn].split("-")[1]).y,
                            network.get_zone(drone.path[turn].split("-")[0]).y,
                        ]
                    )
                    pygame.draw.circle(
                        self.screen,
                        self.colors_rgb["drone"],
                        (
                            int(
                                abs(
                                    (
                                        network.get_zone(
                                            drone.path[turn].split("-")[1]
                                        ).x
                                        - network.get_zone(
                                            drone.path[turn].split("-")[0]
                                        ).x
                                    )
                                )
                                / 2
                            )
                            + lower_pos_x,
                            int(
                                abs(
                                    (
                                        network.get_zone(
                                            drone.path[turn].split("-")[1]
                                        ).y
                                        - network.get_zone(
                                            drone.path[turn].split("-")[0]
                                        ).y
                                    )
                                )
                                / 2
                            )
                            + lower_pos_y,
                        ),
                        5,
                    )
                else:
                    pygame.draw.circle(
                        self.screen,
                        self.colors_rgb["drone"],
                        (
                            network.get_zone(drone.path[turn]).x,
                            network.get_zone(drone.path[turn]).y,
                        ),
                        5,
                    )
            pygame.display.flip()
            pygame.event.pump()
        pygame.quit()
