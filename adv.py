from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Create dict with reverse for each direction
reverse_directions = {'n': 's', 's': 'n', 'e':'w', 'w':'e'}

# Create dict for transversal graph
traversalGraph = {}

# initialize stack, previous room and prev cardinal
stack = Stack()
prev_room = None
prev_cardinal = None

while len(traversalGraph) < len(room_graph):

    # get player current room
    currentRoom = player.current_room.id

    # if the room has not been transvered
    if currentRoom not in traversalGraph:
        # get all the exits in the room and set it to '?'
        exits = {direction: '?' for direction in player.current_room.get_exits()}
        # add the rooms exits to the traversal room 
        traversalGraph[currentRoom] = exits

    # if there is a previous room
    if prev_room:
        # update the previous room traveled cardinal to the current room id
        traversalGraph[prev_room][prev_cardinal] = currentRoom
        # get the reverse of the traveled cardinal
        reverse_cardinal = reverse_directions[prev_cardinal]
        # for the current room set the reverse cardinal to the previous room
        traversalGraph[currentRoom][reverse_cardinal] = prev_room
    # update the previous room to the current room
    prev_room = currentRoom

    next_room = False

    # for each room hold if there is a movement from that room
    movement = False
   
    for exit_cardinal, room in traversalGraph[currentRoom].items():
        # if it is unexplored
        if room == "?":
            prev_cardinal = exit_cardinal
            stack.push(exit_cardinal)
            traversal_path.append(exit_cardinal)
            # move to next room
            # next_room = True
            player.travel(exit_cardinal)
            # set there was a movement
            movement = True
            break
    # if there was no place to go
    if not movement:
        # go back the earlier moved direction
        exit_cardinal = reverse_directions[stack.pop()]
        traversal_path.append(exit_cardinal)
        prev_cardinal = exit_cardinal
        player.travel(exit_cardinal)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
