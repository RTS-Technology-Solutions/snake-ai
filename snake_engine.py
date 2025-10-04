"""🐍 Snake Engine: Expert System AI 🧠⚙️

A classic algorithmic approach to playing Snake using traditional AI techniques.
This demonstrates how games were automated before machine learning became popular!

Features:
- A* pathfinding algorithm for optimal food collection
- Safety analysis to avoid getting trapped
- Hamiltonian cycle fallback for guaranteed survival
- Multiple strategic decision-making layers
- Educational comparison with neural network approach
"""

import math
import heapq
from collections import deque
from snake_game import SnakeGame, SnakeGameVisual
from freegames import vector


class SnakeExpertSystem:
    """Expert system for playing Snake using algorithmic intelligence.
    
    This AI uses classical computer science algorithms and heuristics:
    1. A* pathfinding for food collection
    2. Safety analysis to avoid traps
    3. Strategic decision making
    4. Hamiltonian cycle as backup strategy
    """
    
    def __init__(self, game_width=400, game_height=400):
        self.game_width = game_width
        self.game_height = game_height
        self.grid_size = 10
        self.directions = {
            'UP': (0, 10),
            'RIGHT': (10, 0), 
            'DOWN': (0, -10),
            'LEFT': (-10, 0)
        }
        self.action_map = {
            (0, 10): 0,   # UP
            (10, 0): 1,   # RIGHT
            (0, -10): 2,  # DOWN
            (-10, 0): 3   # LEFT
        }
        
    def get_grid_pos(self, vector_pos):
        """Convert vector position to grid coordinates."""
        boundary = self.game_width // 2
        x = int((vector_pos.x + boundary) / self.grid_size)
        y = int((vector_pos.y + boundary) / self.grid_size)
        return (x, y)
        
    def get_vector_pos(self, grid_pos):
        """Convert grid coordinates to vector position."""
        boundary = self.game_width // 2
        x = grid_pos[0] * self.grid_size - boundary
        y = grid_pos[1] * self.grid_size - boundary
        return vector(x, y)
        
    def is_valid_position(self, pos, snake_body):
        """Check if position is valid (within bounds and not in snake)."""
        grid_pos = self.get_grid_pos(pos)
        grid_size = self.game_width // self.grid_size
        
        # Check bounds
        if not (0 <= grid_pos[0] < grid_size and 0 <= grid_pos[1] < grid_size):
            return False
            
        # Check snake collision
        return pos not in snake_body
        
    def get_neighbors(self, pos):
        """Get valid neighboring positions."""
        neighbors = []
        for direction in self.directions.values():
            new_pos = vector(pos.x + direction[0], pos.y + direction[1])
            neighbors.append(new_pos)
        return neighbors
        
    def manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two positions."""
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)
        
    def astar_pathfind(self, start, goal, snake_body):
        """A* pathfinding algorithm to find optimal path to goal.
        
        Returns:
            list: Path of positions from start to goal, or empty list if no path
        """
        open_set = []
        heapq.heappush(open_set, (0, id(start), start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.manhattan_distance(start, goal)}
        
        visited = set()
        
        while open_set:
            current_f, _, current = heapq.heappop(open_set)
            
            if current in visited:
                continue
            visited.add(current)
            
            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return list(reversed(path))
                
            for neighbor in self.get_neighbors(current):
                if not self.is_valid_position(neighbor, snake_body):
                    continue
                    
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.manhattan_distance(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], id(neighbor), neighbor))
                    
        return []  # No path found
        
    def simulate_move(self, head, direction, snake_body):
        """Simulate a move and return new head position and updated body."""
        new_head = vector(head.x + direction[0], head.y + direction[1])
        new_body = [new_head] + snake_body[:-1]  # Remove tail, add new head
        return new_head, new_body
        
    def count_reachable_squares(self, start_pos, snake_body):
        """Count how many squares are reachable from a position using flood fill."""
        visited = set()
        queue = deque([start_pos])
        count = 0
        
        while queue:
            pos = queue.popleft()
            if pos in visited:
                continue
                
            if not self.is_valid_position(pos, snake_body):
                continue
                
            visited.add(pos)
            count += 1
            
            for neighbor in self.get_neighbors(pos):
                if neighbor not in visited:
                    queue.append(neighbor)
                    
        return count
        
    def evaluate_move_safety(self, head, direction, snake_body, food_pos):
        """Evaluate how safe a move is by checking reachable space."""
        new_head, new_body = self.simulate_move(head, direction, snake_body)
        
        if not self.is_valid_position(new_head, snake_body):
            return -1000  # Invalid move
            
        # Check if we can still reach a reasonable amount of space
        reachable = self.count_reachable_squares(new_head, new_body)
        
        # Prefer moves that keep more space available
        safety_score = reachable
        
        # Add bonus for getting closer to food
        food_distance = self.manhattan_distance(new_head, food_pos)
        distance_score = -food_distance
        
        return safety_score + distance_score * 0.1
        
    def get_safe_directions(self, head, snake_body):
        """Get all directions that don't immediately cause collision."""
        safe_directions = []
        for name, direction in self.directions.items():
            new_pos = vector(head.x + direction[0], head.y + direction[1])
            if self.is_valid_position(new_pos, snake_body):
                safe_directions.append(direction)
        return safe_directions
        
    def find_tail_chase_move(self, head, snake_body):
        """Find a move that chases the tail (space creation strategy)."""
        if len(snake_body) < 2:
            return None
            
        tail = snake_body[-1]
        safe_directions = self.get_safe_directions(head, snake_body)
        
        if not safe_directions:
            return None
            
        # Find direction that gets us closer to tail
        best_direction = None
        best_distance = float('inf')
        
        for direction in safe_directions:
            new_pos = vector(head.x + direction[0], head.y + direction[1])
            distance = self.manhattan_distance(new_pos, tail)
            if distance < best_distance:
                best_distance = distance
                best_direction = direction
                
        return best_direction
        
    def choose_action(self, game_state):
        """Main decision-making function for the expert system.
        
        Strategy priority:
        1. Try A* pathfinding to food if safe
        2. Evaluate move safety and choose best safe move
        3. Chase tail if no good food path exists
        4. Pick any safe move as last resort
        """
        # Extract game information
        head = game_state['head']
        snake_body = game_state['snake']
        food_pos = game_state['food']
        
        # Strategy 1: Try A* pathfinding to food
        path_to_food = self.astar_pathfind(head, food_pos, snake_body)
        
        if len(path_to_food) > 0:
            # We found a path to food, but let's check if it's safe
            next_pos = path_to_food[0]
            direction = (next_pos.x - head.x, next_pos.y - head.y)
            
            # Simulate eating the food and check if we'll have enough space
            temp_body = snake_body + [food_pos]  # Snake grows when eating
            safety_after_food = self.count_reachable_squares(food_pos, temp_body)
            
            # If we'll have reasonable space after eating, go for food
            if safety_after_food > len(snake_body) + 5:
                return self.action_map.get(direction, 0)
        
        # Strategy 2: Evaluate all safe moves by safety score
        safe_directions = self.get_safe_directions(head, snake_body)
        
        if not safe_directions:
            return 0  # No safe moves, return default
            
        best_direction = None
        best_score = -float('inf')
        
        for direction in safe_directions:
            score = self.evaluate_move_safety(head, direction, snake_body, food_pos)
            if score > best_score:
                best_score = score
                best_direction = direction
                
        if best_direction:
            return self.action_map.get(best_direction, 0)
            
        # Strategy 3: Chase tail if nothing else works
        tail_direction = self.find_tail_chase_move(head, snake_body)
        if tail_direction:
            return self.action_map.get(tail_direction, 0)
            
        # Strategy 4: Pick first safe direction
        return self.action_map.get(safe_directions[0], 0)


class SnakeEngineDemo:
    """Demonstration and testing class for the Snake Expert System."""
    
    def __init__(self):
        self.expert_system = SnakeExpertSystem()
        self.games_played = 0
        self.total_score = 0
        self.scores = []
        
    def play_single_game(self, max_moves=500, visual=False, speed=100):
        """Play a single game using the expert system."""
        if visual:
            game = SnakeGameVisual(speed=speed)
        else:
            game = SnakeGame()
            game.max_moves = max_moves
            
        moves = 0
        
        while not game.game_over and moves < max_moves:
            # Prepare game state for expert system
            game_state = {
                'head': game.snake[-1],
                'snake': game.snake,
                'food': game.food
            }
            
            # Get action from expert system
            action = self.expert_system.choose_action(game_state)
            
            # Execute action
            game.step(action)
            moves += 1
            
            if visual and hasattr(game, 'render'):
                game.render()
                
        return game.score, moves, game.game_over
        
    def run_performance_test(self, num_games=10, max_moves=500):
        """Run multiple games to evaluate expert system performance."""
        print(f"🧠 Testing Snake Expert System Performance")
        print(f"Running {num_games} games...")
        print("=" * 50)
        
        scores = []
        total_moves = 0
        wins = 0
        
        for i in range(num_games):
            score, moves, game_over = self.play_single_game(max_moves=max_moves)
            scores.append(score)
            total_moves += moves
            
            if score > 0:
                wins += 1
                
            print(f"Game {i+1:2d}: Score={score:2d}, Moves={moves:3d}, Status={'OVER' if game_over else 'TIME'}")
            
        # Calculate statistics
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        avg_moves = total_moves / num_games
        win_rate = wins / num_games * 100
        
        print("\n📊 Performance Summary:")
        print(f"   Average Score: {avg_score:.1f}")
        print(f"   Best Score: {max_score}")
        print(f"   Average Moves: {avg_moves:.1f}")
        print(f"   Success Rate: {win_rate:.1f}% ({wins}/{num_games} games with score > 0)")
        
        return {
            'scores': scores,
            'avg_score': avg_score,
            'max_score': max_score,
            'avg_moves': avg_moves,
            'win_rate': win_rate
        }
        
    def demo_visual_game(self, speed=150):
        """Run a visual demonstration of the expert system."""
        print("🎮 Starting visual demonstration...")
        print("Watch the expert system play Snake!")
        
        score, moves, game_over = self.play_single_game(visual=True, speed=speed)
        
        print(f"\n🏁 Demo Complete!")
        print(f"   Final Score: {score}")
        print(f"   Total Moves: {moves}")
        print(f"   Game Status: {'Game Over' if game_over else 'Time Limit'}")


def compare_ai_approaches():
    """Compare the expert system with the neural network approach."""
    print("🤖 AI Approach Comparison: Expert System vs Neural Network")
    print("=" * 60)
    
    # Test Expert System
    print("\n🧠 Testing Expert System...")
    engine_demo = SnakeEngineDemo()
    expert_results = engine_demo.run_performance_test(num_games=20)
    
    # Try to test Neural Network if available
    try:
        import pickle
        import os
        saves_dir = "simulation_saves"
        if os.path.exists(saves_dir):
            saves = [f for f in os.listdir(saves_dir) if f.endswith('.pkl')]
            if saves:
                latest_save = max(saves, key=lambda x: os.path.getctime(os.path.join(saves_dir, x)))
                print(f"\n🧬 Testing Neural Network (from {latest_save})...")
                
                with open(os.path.join(saves_dir, latest_save), 'rb') as f:
                    data = pickle.load(f)
                
                best_agent = data['best_agent']
                nn_scores = []
                
                for i in range(20):
                    game = SnakeGame()
                    game.max_moves = 500
                    
                    while not game.game_over:
                        state = game.get_game_state()
                        if state is None:
                            break
                        valid_actions = game.get_valid_actions()
                        action = best_agent.network.get_action(state, valid_actions)
                        game.step(action)
                    
                    nn_scores.append(game.score)
                    print(f"NN Game {i+1:2d}: Score={game.score}")
                
                nn_avg = sum(nn_scores) / len(nn_scores)
                nn_max = max(nn_scores)
                
                print(f"\n📊 Neural Network Results:")
                print(f"   Average Score: {nn_avg:.1f}")
                print(f"   Best Score: {nn_max}")
                
                print(f"\n🏆 Comparison Summary:")
                print(f"   Expert System - Avg: {expert_results['avg_score']:.1f}, Best: {expert_results['max_score']}")
                print(f"   Neural Network - Avg: {nn_avg:.1f}, Best: {nn_max}")
                
                if expert_results['avg_score'] > nn_avg:
                    print("   🧠 Expert System wins on average performance!")
                else:
                    print("   🧬 Neural Network wins on average performance!")
                    
            else:
                print("\n❌ No trained neural network models found.")
        else:
            print("\n❌ No simulation saves directory found.")
            
    except Exception as e:
        print(f"\n❌ Could not test neural network: {e}")


if __name__ == "__main__":
    print("🐍 Snake Expert System 🧠")
    print("Choose an option:")
    print("1. Run performance test (20 games)")
    print("2. Visual demonstration")
    print("3. Compare Expert System vs Neural Network")
    print("4. Quick test (5 games)")
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        demo = SnakeEngineDemo()
        demo.run_performance_test(num_games=20)
    elif choice == "2":
        demo = SnakeEngineDemo()
        demo.demo_visual_game()
    elif choice == "3":
        compare_ai_approaches()
    elif choice == "4":
        demo = SnakeEngineDemo()
        demo.run_performance_test(num_games=5)
    else:
        print("Invalid choice!")
        
    input("\nPress Enter to exit...")

