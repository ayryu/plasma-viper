import os
import cherrypy


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
        body = data["you"]["body"]
        height = data["board"]["height"]
        width = data["board"]["width"]
        all_food_locations = data["board"]["food"]
        turn = data["turn"]
        nearest_food_index = 0

        print(f"Turn number: {turn}")

        nearest_food_position = self.find_closest_food(head, all_food_locations)
        food_path = self.find_food_path(head, nearest_food_position)
        self.switch_path_to_food(all_food_locations, food_path, head, body)
        self.find_surrounding_area(body)

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


    def switch_path_to_food(self, all_food_locations, food_path, head, body):
      # Snake coils if collision is predicted
      possible_moves = ["up", "down", "left", "right"]
      potential_moves = []

      # For checking immediate head directions
      # for move in possible_moves:
      #   potential_moves.append(self.check_potential_move(move, head))
      # body_collision = [collision for collision in body if collision in potential_moves]
      # if body_collision:
      #   for illegal_move in body_collision:
      #     potential_moves.remove(illegal_move) 
      
      # Checks food path for body collisions
      # nearest_food_position = self.find_closest_food(head, all_food_locations)
      # food_path = self.find_food_path(head, nearest_food_position)
      # self.find_food_path(head, nearest_food_position)
      # body_in_food_path_collision = [collision for collision in body if collision in food_path]

      # if body_in_food_path_collision:

      print(f"The collision points are: {[collision for collision in body if collision in food_path]}")
        
      # return {
      #     "move": move
      #   } 


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

      # This adds end space for the head and the tail
    def add_end_spaces(self, body):
    # x: +ve goes right, -ve goes left
    # y: +ve goes up, -ve goes down
      extended_body = []
      extended_head = body[:]
      extended_tail = body[:]
      head_padding = 0
      tail_padding = 0

      head_direction_x = body[0]["x"] - body[1]["x"]
      head_direction_y = body[0]["y"] - body[1]["y"]

      if head_direction_x != 0:
        head_padding = self.help_add_spaces(head_direction_x, extended_head[0]["x"])
        extended_head.insert(0, {"x": head_padding,"y": extended_head[0]["y"]})
        print(f"Head Padding: {head_padding}")
      if head_direction_y != 0:
        head_padding = self.help_add_spaces(head_direction_y, extended_head[0]["y"])
        extended_head.insert(0, {"x": extended_head[0]["x"],"y": head_padding})
        print(f"Head Padding: {head_padding}")
      
      tail_direction_x = body[-1]["x"] - body[-2]["x"]
      tail_direction_y = body[-1]["y"] - body[-2]["y"]

      if tail_direction_x != 0:
        tail_padding = self.help_add_spaces(tail_direction_x, extended_tail[-1]["x"])
        extended_tail.append({"x": tail_padding,"y": extended_tail[-1]["x"]})
        print(f"Tail Padding: {tail_padding}")
      if tail_direction_y != 0:
        tail_padding = self.help_add_spaces(tail_direction_y, extended_tail[-1]["y"])
        extended_tail.append({"x": extended_tail[-1]["x"],"y": tail_padding})
        print(f"Tail Padding: {tail_padding}")
      
      extended_body.append(extended_head)
      extended_body.append(extended_tail)
      print(f"Extended head array: {extended_head}")
      print(f"Extended tail array: {extended_tail}")
      return extended_body
  
    # Adds spaces to head or tail
    def help_add_spaces(self, section_direction, section_position):
      section_extra_space = 0
      if section_direction < 0:
        section_extra_space = section_position - 1
      if section_direction > 0:
        section_extra_space = section_position + 1
      
      print(f"Section extra space: {section_extra_space}")

      return section_extra_space


# Iterate through entire snake body plus head and tail buffer
# Compare first and second section of body as you iterate through full body
# Find the axis with the changing value, and plot surrounding area of static axis value
# Return full surrounding area 
    def find_surrounding_area(self, body):
      body_buffer = self.add_end_spaces(body)
      head_space = body_buffer[0]
      tail_space = body_buffer[1]
      side_a = []
      side_b = []
      real_a = []
      real_b = []
      answer = []

      for (head_list,tail_list) in zip(head_space, tail_space):
        compare_x = head_list["x"] - tail_list["x"]
        compare_y = head_list["y"] - tail_list["y"]

        # Plotting space above and below (add to y) snake's body section
        if compare_x != 0:
          side_a.append({"x": head_list["x"],"y": head_list["y"] - 1})
          side_a.append({"x": tail_list["x"],"y": tail_list["y"] - 1})
          side_b.append({"x": head_list["x"],"y": head_list["y"] + 1})
          side_b.append({"x": tail_list["x"],"y": tail_list["y"] + 1})

        # Plotting space left and right (add to x) of snake's body section
        if compare_y != 0:
          side_a.append({"x": head_list["x"] - 1,"y": head_list["y"]})
          side_a.append({"x": tail_list["x"] - 1,"y": tail_list["y"]})
          side_b.append({"x": head_list["x"] + 1,"y": head_list["y"]})
          side_b.append({"x": tail_list["x"] + 1,"y": tail_list["y"]})
          
        real_a = [duplicate for duplicate in side_a if duplicate not in body]
        real_b = [duplicate for duplicate in side_b if duplicate not in body]
        answer.append(real_a)
        answer.append(real_b)

        return answer

      print(f"This is real a: {real_a}")
      print(f"This is real b: {real_b}")


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
