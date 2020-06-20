import os
import cherrypy
from priorityqueue import *
from vision import *
import random

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
        length = data["you"]["length"]
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
        
        # start, goal = tuple(head.values()), nearest_food
        start, goal = tuple(head.values()), self.change_targets(nearest_food, snakes, head, length, height, width, snake_locations)
        print(f"Start: {start}")
        print(f"Goal: {goal}")
        pq = PriorityQueue()
        best_path = pq.a_star_search(unobstructed_moves, start, goal, snake_locations, height, width)
        move = self.convert_xy_to_direction(best_path)
        print(f"MOVE: {move}")
        return move

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

    def change_targets(self, nearest_food, snakes, head, length, height, width, snake_locations):
      # food info
      current_target = nearest_food
      (food_x, food_y) = nearest_food

      # my info
      (my_head_x, my_head_y) = tuple(head.values())
      my_food_distance = abs(my_head_x - food_x) + abs(my_head_y - food_y)
      my_name = "plasma-viper"
      my_length = int(length) + 2
      print(f"My length at first: {my_length}")

      # enemy info
      longest_enemy = snakes[0]["length"]
      enemy_head = tuple(snakes[0]["head"].values())
      (enemy_head_x, enemy_head_y) = enemy_head
      enemy_food_distance = abs(enemy_head_x - food_x) + abs(enemy_head_y - food_y)

      for snake in snakes:
        if snake["name"] != my_name:
          (snake_head_x, snake_head_y) = tuple(snake["head"].values())
          snake_length = snake["length"]
          if snake_length >= longest_enemy:
            longest_enemy = snake_length

          # Check my distance vs enemy towards food
          snake_food_distance = abs(snake_head_x - food_x) + abs(snake_head_y - food_y)
          if my_food_distance >= snake_food_distance:
            continue
          if my_food_distance < snake_food_distance:
            enemy_head = tuple(snake["head"].values())
            enemy_food_distance = snake_food_distance

      # Go to random location if we're too close
      if int(longest_enemy) < my_length:
          print(f"Longest enemy length: {longest_enemy}")
          print("My length: {type(my_length)}")
          return enemy_head
      if int(longest_enemy) > my_length:
        if my_food_distance >= enemy_food_distance:
          rand_x = random.randint(0, width - 1)
          rand_y = random.randint(0, height - 1)
          rand_xy = (rand_x, rand_y)
          while rand_xy in snake_locations:
            rand_x = random.randint(0, width - 1)
            rand_y = random.randint(0, height - 1)
            rand_xy = (rand_x, rand_y)
          print(f"Random new location: {rand_xy}")
          return rand_xy
        if my_food_distance < enemy_food_distance:
          print("Grabbing food")
          return nearest_food
      
      # return current_target


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
