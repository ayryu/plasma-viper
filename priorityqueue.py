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

    def a_star_search(unobstructed_moves, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        distance_from_start = {} # actual g - distance b/w start and current
        came_from[start] = None
        distance_from_start[start] = 0
        
        while not frontier.empty():
            current_location = frontier.get()
            
            if current_location == goal:
                break
            
            for next in unobstructed_moves:
                new_cost = distance_from_start[current_location] + next.heuristic(current_location, next) # potential g
                if next not in distance_from_start or new_cost < distance_from_start[next]:
                    distance_from_start[next] = new_cost
                    priority = new_cost + next.heuristic(goal, next) # f
                    frontier.put(next, priority)
                    came_from[next] = current_location
        print(f"First step: {came_from[0]}")
        print(f"Full path to food: {came_from}")
        return came_from[0]