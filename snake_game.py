"""Snake Game Engine for AI Training

Enhanced version of the classic Snake game designed for AI automation.
Supports both human play and AI agent control with comprehensive game state management.
"""

import random
import math
import time
from turtle import *
from freegames import square, vector


class SnakeGame:
    """Enhanced Snake game with AI automation support."""
    
    def __init__(self, width=400, height=400, speed=100):
        self.width = width
        self.height = height
        self.speed = speed  # milliseconds between moves
        self.reset_game()
        
    def reset_game(self):
        """Reset game to initial state."""
        self.food = vector(0, 0)
        self.snake = [vector(10, 0)]
        self.aim = vector(0, -10)
        self.score = 0
        self.moves = 0
        self.game_over = False
        self.won = False
        self.max_moves = 200  # Prevent infinite games
        self.place_food()
        
    def place_food(self):
        """Place food at random valid location."""
        attempts = 0
        while attempts < 100:  # Prevent infinite loop
            x = random.randrange(-15, 15) * 10
            y = random.randrange(-15, 15) * 10
            food_pos = vector(x, y)
            if food_pos not in self.snake:
                self.food = food_pos
                return
            attempts += 1

        
    def change_direction(self, x, y):
        """Change snake direction if valid move."""
        new_aim = vector(x, y)
        # Prevent 180-degree turns
        if len(self.snake) > 1:
            if new_aim.x == -self.aim.x and new_aim.y == -self.aim.y:
                return False
        self.aim = new_aim
        return True
        
    def inside(self, head):
        """Return True if head inside boundaries."""
        boundary = self.width // 2 - 10
        return -boundary < head.x < boundary and -boundary < head.y < boundary
        
    def get_game_state(self):
        """Get comprehensive game state for AI input."""
        if not self.snake:
            return None
            
        head = self.snake[-1]
        
        # Direction vectors for 8 directions
        directions = [
            vector(0, 10),   # Up
            vector(10, 10),  # Up-Right  
            vector(10, 0),   # Right
            vector(10, -10), # Down-Right
            vector(0, -10),  # Down
            vector(-10, -10),# Down-Left
            vector(-10, 0),  # Left
            vector(-10, 10)  # Up-Left
        ]
        
        # Distance to walls/body in 8 directions (normalized 0-1)
        distances = []
        for direction in directions:
            distance = self.get_distance_to_obstacle(head, direction)
            distances.append(distance / 20.0)  # Normalize to 0-1
            
        # Food direction (relative position, normalized)
        food_dx = (self.food.x - head.x) / (self.width / 2)
        food_dy = (self.food.y - head.y) / (self.height / 2)
        
        # Current direction (one-hot encoded)
        current_dir = [0, 0, 0, 0]  # Up, Right, Down, Left
        if self.aim.x == 0 and self.aim.y == 10:
            current_dir[0] = 1
        elif self.aim.x == 10 and self.aim.y == 0:
            current_dir[1] = 1
        elif self.aim.x == 0 and self.aim.y == -10:
            current_dir[2] = 1
        elif self.aim.x == -10 and self.aim.y == 0:
            current_dir[3] = 1
            
        # Snake length (normalized)
        snake_length = len(self.snake) / 50.0  # Assume max reasonable length
        
        # Combine all features
        state = distances + [food_dx, food_dy] + current_dir + [snake_length]
        return state
        
    def get_distance_to_obstacle(self, start, direction):
        """Get distance to wall or body in given direction."""
        pos = start.copy()
        distance = 0
        
        while distance < 20:  # Max check distance
            pos += direction
            distance += 1
            
            # Check wall collision
            if not self.inside(pos):
                return distance
                
            # Check body collision
            if pos in self.snake:
                return distance
                
        return distance
        
    def step(self, action=None):
        """Execute one game step. Returns (state, reward, done, info)."""
        if self.game_over:
            return self.get_game_state(), 0, True, {"reason": "already_over"}
            
        # Handle action if provided (for AI)
        if action is not None:
            directions = [
                (0, 10),   # Up
                (10, 0),   # Right  
                (0, -10),  # Down
                (-10, 0)   # Left
            ]
            if 0 <= action < len(directions):
                self.change_direction(*directions[action])
        
        # Move snake
        head = self.snake[-1].copy()
        head.move(self.aim)
        self.moves += 1
        
        reward = 0
        info = {}
        
        # Check collisions
        if not self.inside(head) or head in self.snake:
            self.game_over = True
            reward = -100  # Death penalty
            info["reason"] = "collision"
        else:
            self.snake.append(head)
            
            # Check food collision
            if head == self.food:
                self.score += 1
                reward = 100  # Food reward
                self.place_food()
                info["reason"] = "food"
            else:
                self.snake.pop(0)
                reward = -1  # Small penalty for each move
                
            # Check if moves exceeded
            if self.moves > self.max_moves:
                self.game_over = True
                reward = -50  # Timeout penalty
                info["reason"] = "timeout"
        
        return self.get_game_state(), reward, self.game_over, info
        
    def get_valid_actions(self):
        """Get list of valid actions (no 180-degree turns)."""
        valid = []
        directions = [(0, 10), (10, 0), (0, -10), (-10, 0)]  # Up, Right, Down, Left
        
        for i, (x, y) in enumerate(directions):
            # Check if this would be a 180-degree turn
            if len(self.snake) > 1:
                if x == -self.aim.x and y == -self.aim.y:
                    continue
            valid.append(i)
        return valid


# Visualization and Human Play Support
class SnakeGameVisual(SnakeGame):
    """Snake game with turtle graphics visualization."""
    
    def __init__(self, width=400, height=400, speed=100):
        super().__init__(width, height, speed)
        self.setup_graphics()
        
    def setup_graphics(self):
        """Initialize turtle graphics."""
        setup(self.width + 20, self.height + 20, 370, 0)
        hideturtle()
        tracer(False)
        listen()
        
        # Bind keys for human play
        onkey(lambda: self.change_direction(0, 10), 'Up')
        onkey(lambda: self.change_direction(10, 0), 'Right') 
        onkey(lambda: self.change_direction(0, -10), 'Down')
        onkey(lambda: self.change_direction(-10, 0), 'Left')
        
    def render(self):
        """Render current game state."""
        clear()
        
        # Draw snake
        for body in self.snake:
            square(body.x, body.y, 9, 'black')
            
        # Draw food
        square(self.food.x, self.food.y, 9, 'green')
        
        # Draw score
        penup()
        goto(-self.width//2 + 10, self.height//2 - 30)
        color('blue')
        write(f'Score: {self.score}', font=('Arial', 14, 'normal'))
        
        update()
        
    def play_human(self):
        """Start human-playable game."""
        def game_loop():
            if not self.game_over:
                self.step()
                self.render()
                ontimer(game_loop, self.speed)
            else:
                # Game over screen
                penup()
                goto(0, 0)
                color('red')
                write('GAME OVER!', align='center', font=('Arial', 24, 'bold'))
                
        self.render()
        game_loop()


# For backwards compatibility and quick testing
def change(x, y):
    """Legacy function for original snake game."""
    pass

def inside(head):
    """Legacy function for original snake game."""
    return True

def move():
    """Legacy function for original snake game."""
    pass


if __name__ == "__main__":
    # Quick test/demo
    game = SnakeGameVisual(speed=150)
    game.play_human()
    done()
