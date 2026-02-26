*This project has been created as part of the 42 curriculum by mawelsch*

## Description
The project focuses on steering a swarm of drones through a network of nodes, called zones, and connections that have multiple constraints of capacity. The goal is to find the most efficient route for the entire swarm to navigate through the graph in the fewest turns possible.

### Zone Types
The zones have different types, each with specific behaviors:

- **Normal**: The drone takes **1 turn** to fly to this node.
- **Priority**: The drone takes **1 turn** to fly to this node but is prioritized over a normal node if the path length is the same.
- **Restricted**: The drone takes **2 turns** to fly to this node and must stop once in between.
- **Blocked**: Entry and exit of this node are impossible.

### Connection Capacity
Connections between zones also have capacities. Once the capacity of a node or connection is fully utilized, it cannot be entered again until:
- A drone has exited (for nodes).
- The turn is over (for connections).

---

## Algorithm Description
The implemented algorithm is an adaptation of **Dijkstra's algorithm**. Here’s how it works:

1. **Per Turn Calculations**: Each drone calculates the shortest path from its current node to the end node.
   - **Closed List**: Contains all nodes where the cheapest path is known.
   - **Open List**: Contains known nodes where the cheapest path is not guaranteed.

2. **Initialization**: The drone adds its current node to the closed list and all connected nodes to the open list. Costs are calculated as:
   - **f = n + c + d**
     - **f**: Total cost
     - **n**: Cost of traveling to the node (1 turn for normal and priority nodes, 2 turns for restricted nodes, with priority nodes having a slight preference).
     - **c**: Equals **1** if the node cannot be traveled to in this turn.
     - **d**: Equals **0.01** if a drone is present on the node.

3. **Node Selection**: Always select the node with the lowest cost from the open list, adding newly discovered nodes and updating costs if a lower cost is found using:
   - **f = n + i**
     - **i**: Cost associated with the currently examined tile.

4. **Displacement Phenomenon**: c and d are irrelevant for further nodes, as their capacities most likely have changed and should be recalculated.

5. **Pathfinding**: Once the examined node is the end goal, the shortest path is found, and the path is reconstructed for the drone's movement. If the drone chooses to move to a currently full node, it will opt not to move at all.

6. **Scout Drone**: Before the swarm starts moving, a simulated scout drone checks if a route to the goal exists, throwing an exception if it does not.

---

## Visual Representation
Using the `--visual` flag when executing the program allows for a visual representation of the graph through color-coded logging output. It will open a new window using **Pygame** to show:
- The current state of drone positions after each turn (turn **x** can be adjusted using the left and right arrow keys).
- The window can be closed by pressing **Escape**, **Q**, or clicking the **X** on the window bar.

The GUI helps visualize drone movements effectively.

---

## Instructions
To configure the project, run:
```bash
make install
```
This will install **UV** and **Python 3** if they aren't already installed, create a new virtual environment, and install all necessary packages.

### Running the Program
Execute the program using:
```bash
make run *map_file*
```
or
```bash
uv run python3 main.py *map_file*
```

**Note**: Passing more than one map file is not supported and will cause the program to exit. The `--visual` flag can be added, but it should only be used with `uv run` to avoid crashing the makefile.

### Map File Format
Map files must be text files containing lines in the following formats:
- Comments starting with `#`
- Empty lines
- **nb_drones: x**, where **x** is the number of drones.
- **start_hub: n x y**, declaring the starting node with name **n** and coordinates **x/y**.
- **end_hub: n x y**, declaring the end node with name **n** and coordinates **x/y**.
- **hub: n x y**, declaring a node with name **n** and coordinates **x/y**.
- **connection: x-y**, declaring a connection between the nodes with names **x** and **y**.

### Constraints
- **nb_drones** must be in the first line, excluding comments and empty lines.
- **nb_drones**, **start_hub**, and **end_hub** can each be defined once only.
- Both nodes of a connection must be defined in the file.

### Metadata
Some metadata can be added in brackets `[]`:
- **color (color=x)**: Sets the color used with the zone when using the `--visual` flag (defaults to white if not given).
- **capacity (max_drones=x)**: Describes how many drones can occupy a map part at once (defaults to 1 if not specified).
- **zone (zone=x)**: Sets the zone type (defaults to normal if not specified).

---

## Output Logging
With a valid map file, the program will print movement logs in the format:
```
D<drone id>-<new position>
```
Where:
- **drone id** is a number between 1 and **nb_drones**.
- **new position** indicates the new position or a connection if the drone stopped midway due to a restriction.

When using the `--visual` flag, node names are colored based on the specified color, with defaults applied where necessary, while connections will be **gray**.

---

## Resources
- [Dijkstra's Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [A* Search Algorithm - Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Rich Documentation](https://rich.readthedocs.io/en/stable/)

---

## AI Usage
- Initial planning and structure
- Reconfiguring from A* to Dijkstra
- README structure and wording