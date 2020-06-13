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
        board_height = data["board"]["height"]
        board_width = data["board"]["width"]
        all_snakes = data["board"]["snakes"]

        for snake in all_snakes:
          name = snake["name"]
          print(f"This snake is: {name}")
        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        data = cherrypy.request.json
        head = data["you"]["head"]
        body = data["you"]["body"]
        board_height = data["board"]["height"]
        board_width = data["board"]["width"]
        all_food_locations = data["board"]["food"]
        turn = data["turn"]

        # print(f"The head's current position is: {head}")

        possible_moves = ["up", "down", "left", "right"]
        appropriate_moves = []
        nearest_food_index = 0

        for move in possible_moves:
          potential_move = self.check_potential_move(move, head)
          if self.out_of_bounds(potential_move, board_height, board_width) == True or self.collides_with_body(potential_move, body) == True:
            continue
          else:
            nearest_food_index = self.find_closest_food(head, all_food_locations)
            print(f"Turn number: {turn}")
            print(f"Closest food is: {all_food_locations[nearest_food_index]}")
            print(f"The head is currently located at {head}")
            print(f"MOVE: {move}")
            return {
              "move": move
            }
        
        for section in body:
          print(f"The body seems to be at: {section}")


    # Returns future position of snake's head
    def check_potential_move(self, move, head):
      if move == "up":
          return {"x": head["x"],"y": head["y"] + 1} 
      elif move == "down":
          return {"x": head["x"],"y": head["y"] - 1}
      elif move == "left":
          return {"x": head["x"] - 1, "y": head["y"]}
      elif move == "right": 
          return {"x": head["x"] + 1, "y": head["y"]}

    def out_of_bounds(self, potential_move, height, width):
      if (potential_move["x"] < 0):
          return True
      if (potential_move["y"] < 0):
          return True
      if (potential_move["x"] >= width):
          return True
      if (potential_move["y"] >= height):
          return True
      return False

    def collides_with_body(self, potential_move, body):
      for section in body:
        if potential_move["x"] == section["x"] and potential_move["y"] == section["y"]:
          print("True")
          return True;
      return False

    def find_closest_food(self, head, all_food_locations):
      closest_food = abs(all_food_locations[0]["x"] - head["x"]) + abs(all_food_locations[0]["y"]- head["y"])
      closest_food_index = 0
      for index, food in enumerate(all_food_locations):
        value_of_potential = abs(food["x"] - head["x"]) + abs(food["y"] - head["y"])
        if(value_of_potential <= closest_food):
          closest_food = value_of_potential
          closest_food_index = index

      return closest_food_index

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
