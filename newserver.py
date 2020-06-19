import os
import random
from priorityqueue import *
from vision import *

import cherrypy


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
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

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json
        head = tuple(data["you"]["head"].values())
        snakes = data["board"]["snakes"]
        height = tuple(data["board"]["height"].values())
        width = (data["board"]["width"].values())
        all_food_locations = data["board"]["food"]
        turn = data["turn"]

        snake_locations = locate_snakes(snakes)
        nearest_food = locate_food(self, head, food_locations)
        potential_moves = check_potential_moves(snake_locations, head, nearest_food, height, width)
        start, goal = head, nearest_food

        best_move = a_star_search(potential_moves, start, goal)
        move = self.convert_xy_to_direction(head, best_move)
        print(f"MOVE: {move}")
        return move

    def convert_xy_to_direction(self, head, best_move):
      (x1, y1) = head
      (x2, y2) = best_move
      if x1 - x2 < 0:
        return {"move": "left"}
      if x1 - x2 > 0:
        return {"move": "right"}
      if y1 - y2 < 0:
        return {"move": "down"}
      if y1 - y2 > 0:
        return {"move": "up"}

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