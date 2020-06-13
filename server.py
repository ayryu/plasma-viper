import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
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
        body = data["you"]["body"]
        board_height = data["board"]["height"]
        board_width = data["board"]["width"]

        print(f"The head's current position is: {head}")

        # Choose a random direction to move in
        possible_moves = ["up", "down", "left", "right"]
        if head["x"] == 0:
          move = "right"
        if head["y"] == 11:
          move = "right"  
        else:
          move = random.choice(possible_moves)

        for section in body:
          print(f"The body seems to be at: {section}")

        print(f"MOVE: {move}")
        return {"move": move}

    def make_next_move(self, move, body):
      if move == "up":
          return {"x": head["x"],"y": head["y"] + 1} 
      elif move == "down":
          return {"x": head["x"],"y": head["y"] - 1}
      elif move == "left":
          return {"x": head["x"] + 1, "y": head["y"]}
      elif move == "right": 
          return {"x": head["x"] - 1, "y": head["y"]}


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
