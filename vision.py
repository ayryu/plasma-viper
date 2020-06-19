class Vision:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def locate_snakes(self, snakes):
      snake_bodies = []
      for snake in snakes:
        for body in snake["body"]:
          snake_bodies.append(tuple(body.values()))
      return snake_bodies

    def locate_food(self, head, all_food_locations):
      closest_food = abs(all_food_locations[0]["x"] - head["x"]) + abs(all_food_locations[0]["y"]- head["y"]) # total number of squares that you travel to reach food
      closest_food_index = 0

      for index, food in enumerate(all_food_locations):
        value_of_potential = abs(food["x"] - head["x"]) + abs(food["y"] - head["y"])
        if(value_of_potential <= closest_food):
          closest_food = value_of_potential
          closest_food_index = index
      nearest_food = (tuple(all_food_locations[closest_food_index].values()))

      return nearest_food

    # snake_locations value comes from self.locate_snakes
    def check_collisions(self, snake_locations, potential_moves):
      collisions = [collision for collision in snake_locations if collision in potential_moves]
      return collisions
    
    def out_of_bounds(self, potential_moves, height, width):
      (x, y) = potential_moves
      if (x < 0? or (y < 0) or (x >= width) or (y >= height):
          return True
      return False

    def check_potential_moves(self, snakes, head, closest_food, height, width):
      potential_moves = [(head["x"] - 1, head["y"]), (head["x"] + 1, head["y"]), (head["x"], head["y"] - 1), (head["x"], head["y"] - 1)]
      snake_locations = self.locate_snakes(snakes)
      moves = filter(self.check_collisions(snake_locations, potential_moves), moves)
      moves = filter(self.out_of_bounds(potential_moves, height, width), moves)
      return moves

    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)
