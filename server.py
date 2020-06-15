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
        body = data["you"]["body"]
        height = data["board"]["height"]
        width = data["board"]["width"]
        all_food_locations = data["board"]["food"]
        turn = data["turn"]
        nearest_food_index = 0

        print(f"Turn number: {turn}")

        nearest_food_position = self.find_closest_food(head, all_food_locations)
        # testing find_food_path
        food_path = self.find_food_path(head, nearest_food_position)
        self.switch_path_to_food(food_path, body)

        possible_moves = ["up", "down", "left", "right"]
        for move in possible_moves:
          potential_move = self.check_potential_move(move, head)

          if self.out_of_bounds(potential_move, height, width) == True or self.collides_with_body(potential_move, body) == True or self.moves_away_from_food(nearest_food_position, head, potential_move) == True:
            continue
        # else: 
          if self.out_of_bounds(potential_move, height, width) == False or self.collides_with_body(potential_move, body) == False or self.moves_away_from_food(nearest_food_position, head, potential_move) == False:
            print(f"Closest food is: {nearest_food_position}")
            print(f"Food positions: {all_food_locations}")
            print(f"The head is currently located at {head}")
            print(f"The body is at: {body}")
            print(f"MOVE: {move}")
            return {
              "move": move
            }

    def switch_path_to_food(self, food_path, body):
      # Snake coils if collision is predicted
      print(f"The collision points are: {[collision for collision in body if collision in food_path]}")

    def moves_away_from_food(self, nearest_food_position, head, potential_move):
      x_moves_away = self.check_food_distance(head["x"], nearest_food_position["x"], potential_move["x"])
      y_moves_away = self.check_food_distance(head["y"], nearest_food_position["y"], potential_move["y"])

      if x_moves_away == True or y_moves_away == True:
        return True
      if x_moves_away == False and y_moves_away == False:
        return False

    def check_food_distance(self, head, nearest_food_position, potential_move):
      # check collision and OOB here
      head_difference = abs(nearest_food_position - head)
      potential_difference = abs(nearest_food_position - potential_move)
      if head_difference < potential_difference:
        return True # Head is closer to food than potential_move
      if potential_difference <= head_difference:
        return False # Potential_move is closer or doesn't change position

    # Returns future position of snake's head
    def check_potential_move(self, movement, head):
      if movement == "up":
          return {"x": head["x"],"y": head["y"] + 1} 
      elif movement == "down":
          return {"x": head["x"],"y": head["y"] - 1}
      elif movement == "left":
          return {"x": head["x"] - 1, "y": head["y"]}
      elif movement == "right": 
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
          return True;
      return False

    # filters through list of available food
    def find_closest_food(self, head, all_food_locations):
      closest_food = abs(all_food_locations[0]["x"] - head["x"]) + abs(all_food_locations[0]["y"]- head["y"]) # total number of squares that you travel to reach food
      closest_food_index = 0

      for index, food in enumerate(all_food_locations):
        value_of_potential = abs(food["x"] - head["x"]) + abs(food["y"] - head["y"])
        if(value_of_potential <= closest_food):
          closest_food = value_of_potential
          closest_food_index = index

      return all_food_locations[closest_food_index]
    
    # Outputs array of every square's coordinates in shortest path
    def find_food_path(self, head, closest_food): 
      path_of_x = []
      path_of_y = []
      shortest_path = []
      # closest_food = self.find_closest_food(head, all_food_locations)

      if closest_food["y"] - head["y"] != 0: 
        path_of_y = self.add_path_coordinates(closest_food["y"], head["y"])
        for y in path_of_y:
          shortest_path.append({"x": head["x"], "y": y})

      if closest_food["x"] - head["x"] != 0:
        path_of_x = self.add_path_coordinates(closest_food["x"], head["x"])
        for x in path_of_x:
          shortest_path.append({"x": x, "y": closest_food["y"]})

      print(f"The following are in the shortest path: \n {shortest_path}")
      return shortest_path

    def add_path_coordinates(self, closest_food, head):
      # if x is +ve, food is up. If x is -ve, food is down
      # if y is +ve, food is right. If y is -ve, food is left
      i = 0
      axis_coordinates = [] # if stationary on axis, return current position
      if closest_food - head < 0:
        while(i > closest_food - head):
          i = i - 1
          axis_coordinates.append(head + i) # every axis position in path
      if closest_food - head > 0:
        while(i < closest_food - head):
          i = i + 1
          axis_coordinates.append(head + i) # every axis position in path
      return axis_coordinates

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
