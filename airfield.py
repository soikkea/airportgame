# -*- coding: utf-8 -*-

import random
import math

class Airfield(object):
    """
    Airfield that contains runways.
    """
    FIELD_HEIGHT = 200
    FIELD_WIDTH = 400
    RUNWAY_LENGTH_SHORT = 70
    RUNWAY_LENGTH_MED = 100
    RUNWAY_LENGTH_LONG = 150
    MINIMUM_DISTANCE = 30

    def __init__(self):
        self.runway_list = []
        # TODO: airfield size based on difficulty
        self.max_runways = 10
        self.min_runways = 3

        self.create_airfield()
    
    def create_airfield(self):
        """
        Randomly fills the airfield with runways
        """
        number_of_runways = random.randint(self.min_runways,
            self.max_runways)
        
        # Initialize the list of runways
        # TODO: Why is this self.?
        self.runways = [0] * number_of_runways

        length = 0
        for i in range(number_of_runways):

            # Make sure that there is at least one runway of each length
            if i <= 2:
                length += 1
            else:
                length = random.randint(1,3)
            
            if length == 1:
                runway_length = self.RUNWAY_LENGTH_SHORT
            elif length == 2:
                runway_length = self.RUNWAY_LENGTH_MED
            elif length == 3:
                runway_length = self.RUNWAY_LENGTH_LONG
            
            start_point_found = False

            while not start_point_found:
                s_x = random.randint(0, self.FIELD_WIDTH)
                s_y = random.randint(0, self.FIELD_HEIGHT)

                start_point_found = self.compare_points((s_x, s_y), i)
            
            start = (s_x, s_y)

            end_point_found = False

            # Counter to prevent infinite loops
            temp = 0

            while not end_point_found:

                temp += 1

                angle = random.random() * math.pi * 2
                e_x = math.cos(angle) * runway_length
                e_y = math.sin(angle) * runway_length

                # Make sure the endpoints are inside the airfield
                if s_x + e_x > self.FIELD_WIDTH or s_x + e_x < 0:
                    e_x = s_x - e_x
                else:
                    e_x = s_x + e_x
                if s_y + e_y > self.FIELD_HEIGHT or s_y + e_y < 0:
                    e_y = s_y - e_y
                else:
                    e_y = s_y + e_y
                
                e_x = int(e_x)
                e_y = int(e_y)

                end = (e_x, e_y)
                end_point_found = self.compare_points(end, i)

                if temp == 10000:
                    # Just use this one if we actually end up here
                    end_point_found = True
            
            # start point should be to the left of end:
            if e_x < s_x:
                temp = start
                start = end
                end = start
            
            self.runways[i] = (start, end)

            # TODO: Add runway class
            new_runway = (start, end, i+1, length)
            # new_runway = Runway(start, end, i+1, length)

        return


    def get_runways(self):
        return self.runway_list


    def distance_between(self, a, b):
        """
        Calculates the distance between two points
        """
        a_x = a[0]
        a_y = a[1]
        b_x = b[0]
        b_y = b[1]
        distance = math.sqrt((a_x - b_x) ** 2 + (a_y - b_y) ** 2)
        return distance
        
    
    def compare_points(self, point, index):
        """
        Checks that the starting and ending points of all other runways are far enough
        of the one being tested.
        """
        if index == 0:
            return True
        
        for runway in range(index):
            for r_point in range(2):
                # TODO: Fix this using the runway class
                return True
