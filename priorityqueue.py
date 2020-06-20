import heapq
import os
import cherrypy
from vision import *

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star_search(self, unobstructed_moves, start, goal, snake_locations, height, width):
        cardinals = Vision(height, width)
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        distance_from_start = {} # actual g - distance b/w start and current
        came_from[start] = None
        distance_from_start[start] = 0
        movement_direction = []
        
        while not frontier.empty():
            current_location = frontier.get()
            movement_direction.append(current_location)
            if current_location == goal:
                print("current_location == goal!")
                break
            
            # for x in FUNCTION because the potential_moves change
            # when the current_location changes
            for next in cardinals.check_potential_moves(snake_locations, current_location, height, width):
                new_cost = distance_from_start[current_location] + self.heuristic(current_location, next) # potential g
                if next not in distance_from_start or new_cost < distance_from_start[next]:
                    distance_from_start[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next) # f
                    frontier.put(next, priority)
                    came_from[next] = current_location
        return movement_direction