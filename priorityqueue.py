import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def locate_snakes(self, snakes):
      snake_bodies = []
      for snake in snakes:
        for body in snake["body"]:
        list = [(k, v) for k, v in body.items()]
        snake_bodies.extend(list)
      return snake_bodies

    def check_collisions(self, snake_locations, potential_moves):
      collisions = [collision for collision in snake_locations if collision in potential_moves]
      return collisions
    
    def out_of_bounds(self, potential_moves, height, width):
      (x, y) = potential_moves
      if (x < 0? or (y < 0) or (x >= width) or (y >= height):
          return True
      return False

    def check_potential_moves(self, head, snakes, height, width):
      potential_moves = [(head["x"] - 1, head["y"]), (head["x"] + 1, head["y"]), (head["x"], head["y"] - 1), (head["x"], head["y"] - 1)]
      snake_locations = self.locate_snakes(snakes)
      moves = filter(self.check_collisions(snake_locations, potential_moves), moves)
      moves = filter(self.out_of_bounds(potential_moves, height, width), moves)
      return moves
