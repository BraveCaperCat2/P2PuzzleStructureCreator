import random

class location:
    def __init__(self, island):
        self.island = island
    def __str__(self):
        return f"Island {self.island}"

class object:
    def __init__(self, position):
        self.position = position

class portal(object):
    def __init__(self, type, position):
        object.__init__(self, position)
        self.type = type # Portal Type: None means that this portal hasn't been placed, Null means that this portal has been placed but the other hasn't and Linked means both portals have been placed.
        if type != "None":
            self.position = position
        else:
            self.position = None
    def __str__(self):
        type = ""
        position_text = f"\n      Current Position: {str(self.position)}"
        if self.type == "None":
            type = "Unplaced"
            position_text = ""
        elif self.type == "Null":
            type = "Unlinked"
        elif self.type == "Linked":
            type = "Linked"
        else:
            type = "Unknown"
        return f"      Status: {type}{position_text}"

class player(object):
    def __init__(self, position, id):
        object.__init__(self, position)
        self.portal1 = portal("None", None)
        self.portal2 = portal("None", None)
        self.starting_position = position
        self.id = id
    def __str__(self):
        return f"  Player {str(self.id)}:\n    Primary Portal:\n{str(self.portal1)}\n    Secondary Portal:\n{str(self.portal2)}\n    Starting Location: {str(self.starting_position)}\n    Current Location: {str(self.starting_position)}"

class cube(object):
    def __init__(self, position, has_dropper):
        object.__init__(self, position)
        self.hasdropper = has_dropper
        if has_dropper:
            self.dropper = position

class reflection_cube(cube):
    def __init__(self, position, has_dropper, orientation):
        cube.__init__(self, position, has_dropper)
        self.orientation = orientation

class connection:
    def __init__(self, position1, position2):
        self.allows_portals = True
        self.allows_lasers = True
        self.allows_cubes = False
        self.allows_players = False
        self.position1 = position1
        self.position2 = position2
    def __str__(self):
        return f"  Connection between Islands {str(self.position1.island)} and {str(self.position2.island)}:\n    Allows Portals: {str(self.allows_portals)}\n    Allows Lasers: {str(self.allows_lasers)}\n    Allows Players: {str(self.allows_players)}\n    Allows Cubes: {str(self.allows_cubes)}"

class island:
    def __init__(self, id, portal_surfaces):
        self.portal_surfaces = portal_surfaces
        self.id = id
        self.connected_to = []
    def __str__(self):
        return f"  Island {str(self.id)}:\n    Portal Surfaces: {str(self.portal_surfaces)}\n    Connected To: {str(self.connected_to)}"

class setup:
    def __init__(self, islands, branches, loops, connect_chance, starting_position):
        self.islands = []
        for i in range(0, islands):
            self.islands.insert(i, island(i, 1))
        self.connections = []
        if branches:
            for i in self.islands:
                for j in self.islands:
                    if i.id == j.id:
                        break
                    if (i.id not in j.connected_to) and (j.id not in i.connected_to):
                        would_be_loop = False
                        for k in j.connected_to:
                            if k in i.connected_to:
                                would_be_loop = True
                                break
                        if not (would_be_loop and not loops):
                            rand_number = random.random()
                            if rand_number <= connect_chance:
                                i.connected_to.append(j.id)
                                j.connected_to.append(i.id)
                                self.connections.append(connection(location(i.id), location(j.id)))
        else:
            for i in self.islands:
                if (i.id != 0) and (i.id - 1 not in i.connected_to):
                    i.connected_to.append(i.id - 1)
                    self.islands[i.id - 1].connected_to.append(i.id)
                    self.connections.append(connection(location(i.id), location(i.id - 1)))
                if (i.id != len(self.islands) - 1) and (i.id + 1 not in i.connected_to):
                    i.connected_to.append(i.id + 1)
                    self.islands[i.id + 1].connected_to.append(i.id)
                    self.connections.append(connection(location(i.id), location(i.id + 1)))
        self.player_count = 1
        self.players = []
        for i in range(self.player_count):
            self.players.append(player(starting_position, i + 1))
        self.branches = branches
        self.loops = loops
        self.connect_chance = connect_chance
        self.starting_position = starting_position
    def __str__(self):
        return f"Islands:\n{"\n".join([str(island) for island in self.islands])}\nConnections:\n{"\n".join([str(connection) for connection in self.connections])}\nPlayers:\n{"\n".join([str(player) for player in self.players])}\nPlayer Count: {str(self.player_count)}\nBranches Enabled: {str(self.branches)}\nLoops Enabled: {str(self.loops)}\nConnection Chance: {str(self.connect_chance)}\nStarting Position: {str(self.starting_position)}"

print(setup(3, False, False, 0.5, location(0)))