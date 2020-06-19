import heapq
import os
import cherrypy

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

    def a_star_search(self, unobstructed_moves, start, goal):
        # frontier = PriorityQueue()
        # frontier.put(start, 0)
        self.put(start, 0)
        came_from = {}
        distance_from_start = {} # actual g - distance b/w start and current
        came_from[start] = None
        distance_from_start[start] = 0
        
        while not self.empty():
            current_location = self.get()
            
            if current_location == goal:
                break
            
            for next in unobstructed_moves:
                new_cost = distance_from_start[current_location] + self.heuristic(current_location, next) # potential g
                if next not in distance_from_start or new_cost < distance_from_start[next]:
                    distance_from_start[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next) # f
                    self.put(next, priority)
                    came_from[next] = current_location
        # print(f"First step: {came_from[0]}")
        print(f"Full path to food: {came_from}")
        return came_from