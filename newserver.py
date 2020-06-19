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
            "color": "#888888",  # TODO: Personalize
            "head": "default",  # TODO: Personalize
            "tail": "default",  # TODO: Personalize
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
        head = data["you"]["head"]
        snakes = data["board"]["snakes"]
        height = data["board"]["height"]
        width = data["board"]["width"]
        all_food_locations = data["board"]["food"]
        turn = data["turn"]

        snake_locations = self.locate_snakes(snakes)

        # Choose a random direction to move in
        possible_moves = ["up", "down", "left", "right"]

        start, goal = 
        best_move = a_star_search(diagram4, start, goal)

        print(f"MOVE: {move}")
        return {"move": move}

    def convert_xy_to_direction(self):

      
    def convert_direction_to_xy(self):
        if movement == "up":
          return {"x": head["x"],"y": head["y"] + 1} 
      elif movement == "down":
          return {"x": head["x"],"y": head["y"] - 1}
      elif movement == "left":
          return {"x": head["x"] - 1, "y": head["y"]}
      elif movement == "right": 
          return {"x": head["x"] + 1, "y": head["y"]}


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