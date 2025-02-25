import random
import time

class Obstacles:
    #Class representing obstacles in the environment
    
    def __init__(self, position, size=1):
        self.position = position  # (x, y) coordinates
        self.size = size  # Size of the obstacle
    
    def is_in_path(self, position, threshold=1):
        #Check if the given position is too close to the obstacle
        distance = ((self.position[0] - position[0])**2 + 
                   (self.position[1] - position[1])**2)**0.5
        return distance < (self.size + threshold)


class LineFollowingRobot:
    #Robot that follows a line and avoids obstacles
    
    def __init__(self, start_position=(0, 0), line_path=None):
        self.position = start_position
        self.direction = 0  # Angle in degrees (0 is forward)
        self.speed = 1.0
        self.sensors = {
            'left': None,
            'center': None,
            'right': None,
            'obstacle_detector': None
        }
        
        # If no line path is provided, create a simple one
        self.line_path = line_path if line_path else self._create_default_path()
        
        # List of obstacles in the environment
        self.obstacles = []
        
        # Robot state
        self.state = "FOLLOW_LINE"  # States: FOLLOW_LINE, AVOID_OBSTACLE, FIND_LINE
        
        # PID controller parameters for line following
        self.kp = 0.5  # Proportional gain
        self.ki = 0.01  # Integral gain
        self.kd = 0.2  # Derivative gain
        self.integral = 0
        self.previous_error = 0
    
    def _create_default_path(self):
        #Create a default path for the robot to follow
        path = []
        for i in range(100):
            # Create a slightly curved path
            x = i
            y = 10 * (i // 20 % 2) + 5 * (i % 20) * (i // 20 % 2) - 5 * (i % 20) * ((i // 20 + 1) % 2)
            path.append((x, y))
        return path
    
    def add_obstacle(self, position, size=1):
        #Add an obstacle to the environment"""
        self.obstacles.append(Obstacles(position, size))
    
    def generate_random_obstacles(self, count=5, max_size=2):
        """Generate random obstacles in the environment"""
        for _ in range(count):
            # Generate obstacles near but not directly on the line
            line_point = random.choice(self.line_path)
            offset_x = random.randint(-10, 10)
            offset_y = random.randint(-10, 10)
            
            # Make sure obstacle is not directly on the line but close enough to be relevant
            while abs(offset_x) < 2 and abs(offset_y) < 2:
                offset_x = random.randint(-10, 10)
                offset_y = random.randint(-10, 10)
            
            position = (line_point[0] + offset_x, line_point[1] + offset_y)
            size = random.uniform(1, max_size)
            self.add_obstacle(position, size)
    
    def read_sensors(self):
        """Read sensor values based on current position"""
        # Find the closest point on the line
        closest_point_idx = self._find_closest_line_point()
        closest_point = self.line_path[closest_point_idx]
        
        # Calculate sensor readings based on distance to line
        # Center sensor
        distance_to_line = ((self.position[0] - closest_point[0])**2 + 
                           (self.position[1] - closest_point[1])**2)**0.5
        self.sensors['center'] = max(0, 1 - (distance_to_line / 2))
        
        # Left and right sensors (offset from center)
        left_pos = (self.position[0] - 1, self.position[1])
        right_pos = (self.position[0] + 1, self.position[1])
        
        # Find closest points for left and right sensors
        left_distance = min(((left_pos[0] - p[0])**2 + (left_pos[1] - p[1])**2)**0.5 
                           for p in self.line_path[max(0, closest_point_idx-5):min(len(self.line_path), closest_point_idx+5)])
        right_distance = min(((right_pos[0] - p[0])**2 + (right_pos[1] - p[1])**2)**0.5 
                            for p in self.line_path[max(0, closest_point_idx-5):min(len(self.line_path), closest_point_idx+5)])
        
        self.sensors['left'] = max(0, 1 - (left_distance / 2))
        self.sensors['right'] = max(0, 1 - (right_distance / 2))
        
        # Obstacle detection
        self.sensors['obstacle_detector'] = False
        for obstacle in self.obstacles:
            if obstacle.is_in_path(self.position, threshold=3):
                self.sensors['obstacle_detector'] = True
                break
    
    def _find_closest_line_point(self):
        """Find the index of the closest point on the line to the current position"""
        min_distance = float('inf')
        closest_idx = 0
        
        for i, point in enumerate(self.line_path):
            distance = ((self.position[0] - point[0])**2 + 
                       (self.position[1] - point[1])**2)**0.5
            if distance < min_distance:
                min_distance = distance
                closest_idx = i
        
        return closest_idx
    
    def follow_line(self):
        """PID controller for line following"""
        # Calculate error (difference between left and right sensors)
        error = self.sensors['left'] - self.sensors['right']
        
        # PID calculation
        self.integral += error
        derivative = error - self.previous_error
        
        # Calculate steering adjustment
        steering = self.kp * error + self.ki * self.integral + self.kd * derivative
        
        # Update direction with steering
        self.direction += steering
        
        # Save error for next iteration
        self.previous_error = error
        
        return steering
    
    def avoid_obstacle(self):
        """Logic for obstacle avoidance"""
        # Simple obstacle avoidance: turn right and move forward
        self.direction += 30  # Turn right by 30 degrees
        
        # Check if we're clear of obstacles after turning
        test_position = (
            self.position[0] + self.speed * 2 * (self.direction / 360),
            self.position[1] + self.speed * 2 * (1 - self.direction / 360)
        )
        
        for obstacle in self.obstacles:
            if obstacle.is_in_path(test_position):
                # Still in path of obstacle, turn more
                return False
        
        # Clear of obstacles
        return True
    
    def find_line(self):
        """Logic to find the line again after avoiding an obstacle"""
        # Spiral search pattern to find the line
        self.direction += 10
        
        # Check if any sensor detects the line
        if (self.sensors['left'] > 0.5 or 
            self.sensors['center'] > 0.5 or 
            self.sensors['right'] > 0.5):
            return True
        
        return False
    
    def update(self):
        """Update robot state and position"""
        # Read sensor values
        self.read_sensors()
        
        # State machine for robot behavior
        if self.state == "FOLLOW_LINE":
            if self.sensors['obstacle_detector']:
                self.state = "AVOID_OBSTACLE"
                print("Obstacle detected! Avoiding...")
            else:
                steering = self.follow_line()
                print(f"Following line. Left: {self.sensors['left']:.2f}, Center: {self.sensors['center']:.2f}, Right: {self.sensors['right']:.2f}, Steering: {steering:.2f}")
        
        elif self.state == "AVOID_OBSTACLE":
            if self.avoid_obstacle():
                self.state = "FIND_LINE"
                print("Cleared obstacle. Searching for line...")
            else:
                print("Still avoiding obstacle...")
        
        elif self.state == "FIND_LINE":
            if self.find_line():
                self.state = "FOLLOW_LINE"
                print("Line found! Resuming line following.")
            else:
                print("Searching for line...")
        
        # Update position based on direction and speed
        dx = self.speed * (self.direction / 360)
        dy = self.speed * (1 - abs(self.direction) / 360)
        
        self.position = (self.position[0] + dx, self.position[1] + dy)
    
    def run_simulation(self, steps=100):
        """Run the robot simulation for a specified number of steps"""
        print("Starting robot simulation...")
        print(f"Initial position: {self.position}")
        
        for step in range(steps):
            print(f"\nStep {step+1}/{steps}")
            self.update()
            print(f"Position: {self.position}, Direction: {self.direction:.1f}°, State: {self.state}")
            time.sleep(0.1)  # Slow down simulation for readability
        
        print("\nSimulation complete!")


# Example usage
if __name__ == "__main__":
    # Create robot
    robot = LineFollowingRobot()
    
    # Generate random obstacles
    robot.generate_random_obstacles(count=8)
    
    # Run simulation
    robot.run_simulation(steps=200)
