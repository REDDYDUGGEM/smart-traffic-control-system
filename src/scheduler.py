# src/scheduler.py

class TrafficScheduler:
    """
    Your custom optimization engine responsible for computing dynamic time allocations
    for primary through-phases and protected left-turn extensions.
    """
    def __init__(self):
        pass

    def compute_green_duration(self, bottleneck_lane_count, total_intersection_count):
        """
        Calculates a dynamic green light duration based on the through-lane worst-case.
        - <= 7 vehicles: 15 seconds (Minimum floor)
        - >= 14 vehicles: 30 seconds (Maximum ceiling)
        - Between 8 and 13 vehicles: Fluctuates linearly between 15 and 30 seconds
        """
        if bottleneck_lane_count <= 7:
            return 15
        if bottleneck_lane_count >= 14:
            return 30
            
        min_count_bound, max_count_bound = 7, 14
        min_time_bound, max_time_bound = 15, 30
        
        proportion = (bottleneck_lane_count - min_count_bound) / (max_count_bound - min_count_bound)
        calculated_time = min_time_bound + (proportion * (max_time_bound - min_time_bound))
        return int(calculated_time)

    def compute_left_turn_extension(self, worst_left_turn_count):
        """
        Calculates an extra protected left-turn green arrow time.
        
        Rules:
        - <= 3 vehicles: 5 seconds (Minimum clearance arrow)
        - >= 8 vehicles: 15 seconds (Maximum protection arrow)
        - Between 4 and 7 vehicles: Fluctuates linearly between 5 and 15 seconds
        """
        # Lower boundary constraint
        if worst_left_turn_count <= 3:
            return 5
            
        # Upper boundary constraint
        if worst_left_turn_count >= 8:
            return 15
            
        # Linear Interpolation for left turns
        min_left_bound, max_left_bound = 3, 8
        min_arrow_time, max_arrow_time = 5, 15
        
        proportion = (worst_left_turn_count - min_left_bound) / (max_left_bound - min_left_bound)
        calculated_arrow = min_arrow_time + (proportion * (max_arrow_time - min_arrow_time))
        return int(calculated_arrow)