class Vision:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    # outputs list of snake position tuples
    def locate_snakes(self, snakes):
      snake_bodies = []
      for snake in snakes:
        for body in snake["body"]:
          snake_bodies.append(tuple(body.values()))
      return snake_bodies

    # outputs tuple of closest food xy
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

      collisions = [collision for collision in potential_moves if collision not in snake_locations]
      return collisions
    
    def out_of_bounds(self, potential_moves, height, width):
      within_bounds = []
      for move in potential_moves:
        (x, y) = move
        if x < 0 or y < 0 or x >= width or y >= height:
          continue
        within_bounds.append(move)
      return within_bounds

    def check_potential_moves(self, snake_locations, head, height, width):
      (x, y) = head
      moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
      collision_free = self.check_collisions(snake_locations, moves)
      potential_moves = self.out_of_bounds(collision_free, height, width)
      return potential_moves
