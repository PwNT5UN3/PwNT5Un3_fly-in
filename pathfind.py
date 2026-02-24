from graph import Zone, Connection, ZoneType, Drone, Graph


class Pathfinder:
    @staticmethod
    def get_best_next_tile(drone: Drone, network: Graph) -> str:
        open_list: list[str] = []
        closed_list: list[str] = []
        costs: dict[str, float] = {}
        parents: dict[str, str] = {}
        closed_list.append(drone.current_zone)
        costs[drone.current_zone] = 0
        for node in network.get_links(drone.current_zone):
            if (
                network.get_zone(node).is_not_available()
                or network.get_connection(
                    drone.current_zone, node
                ).is_not_available()
            ):
                # print(network.get_zone(node).current_drone_count)
                continue
            open_list.append(node)
            costs[node] = network.get_zone(node).get_zone_cost()
            parents[node] = drone.current_zone
        if network.end_node is None:
            raise ValueError("something unexpected happened")
        while network.end_node.name not in closed_list:
            print(open_list)
            if len(open_list) == 0:
                raise ValueError("GRAPH IS SEVERED")
            open_list.sort(key=lambda x: costs.get(x, 0), reverse=True)
            examined = open_list.pop()
            closed_list.append(examined)
            for node in network.get_links(examined):
                if (
                    node in closed_list
                    or network.get_zone(node).is_not_available()
                    or network.get_connection(
                        examined, node
                    ).is_not_available()
                ):
                    continue
                cost = (
                    costs.get(examined, 0)
                    + network.get_zone(node).get_zone_cost()
                )
                if node in open_list:
                    if costs.get(node, float("inf")) > cost:
                        costs[node] = cost
                        parents[node] = examined
                else:
                    open_list.append(node)
                    costs[node] = cost
                    parents[node] = examined
        path = [network.end_node.name]
        while drone.current_zone not in path:
            last = path.pop()
            next_node = parents.get(last, "")
            path.append(last)
            path.append(next_node)
            print(path)
        return path[::-1][1]

    @staticmethod
    def move_to_next_tile(drone: Drone, network: Graph) -> None:
        if drone.found_target:
            return
        drone_zone = network.get_zone(drone.current_zone)
        if drone_zone is None:
            raise ValueError("Drone zone must exist")
        if drone_zone.type == ZoneType.RESTRICTED and not drone.has_waited:
            drone.has_waited = True
            drone.path.append(drone.current_zone)
            return
        print(network.get_zone(drone.current_zone).current_drone_count)
        next_node = Pathfinder.get_best_next_tile(drone, network)
        print(next_node)
        drone.has_waited = False
        network.get_zone(drone.current_zone).current_drone_count -= 1
        drone.current_zone = next_node
        if network.end_node is None:
            raise ValueError("something unexpected happened")
        if drone.current_zone == network.end_node.name:
            drone.found_target = True
        network.get_zone(drone.current_zone).current_drone_count += 1
        drone.path.append(drone.current_zone)
