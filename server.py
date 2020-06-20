import os
import cherrypy
from priorityqueue import *
from vision import *
# import sys

# sys.path.append(".")

class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "",  # TODO: Your Battlesnake Username
            "color": "#66ffb3",  # TODO: Personalize
            "head": "shac-workout",  # TODO: Personalize
            "tail": "bwc-flake",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json
        board_height = data["board"]["height"]
        board_width = data["board"]["width"]
        all_snakes = data["board"]["snakes"]

        # for snake in all_snakes:
        #   name = snake["name"]
        #   print(f"This snake is: {name}")
        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        data = cherrypy.request.json
        head = data["you"]["head"]
        snakes = data["board"]["snakes"]
        height = data["board"]["height"]
        width = data["board"]["width"]
        all_food_locations = data["board"]["food"]
        turn = data["turn"]
        print(f"Turn {turn}")

        potential_moves = Vision(height, width)
        snake_locations = potential_moves.locate_snakes(snakes)
        nearest_food = potential_moves.locate_food(head, all_food_locations)
        unobstructed_moves = potential_moves.check_potential_moves(snake_locations, tuple(head.values()), height, width)
        
        start, goal = tuple(head.values()), nearest_food
        print(f"Start: {start}")
        print(f"Goal: {goal}")
        pq = PriorityQueue()
        best_path = pq.a_star_search(unobstructed_moves, start, goal, snake_locations, height, width)
        move = self.convert_xy_to_direction(best_path)
        print(f"MOVE: {move}")
        return move
        # print(f"MOVE: left")
        # return {"move": "left"}

    def convert_xy_to_direction(self, best_path):
        (x1, y1) = best_path[0]
        print(f"Best path [0]: {best_path[0]}")
        (x2, y2) = best_path[1]
        print(f"Best path [1]: {best_path[1]}")
        if x1 - x2 > 0:
          return {"move": "left"}
        if x1 - x2 < 0:
          return {"move": "right"}
        if y1 - y2 < 0:
          return {"move": "up"}
        if y1 - y2 > 0:
          return {"move": "down"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
