"""🐍 Snake AI: Neural Network + Genetic Algorithm Adventure! 🧠🧬

A fun educational project showing how artificial intelligence can learn to play Snake!
This implementation uses a simple feedforward neural network trained with genetic algorithms.

Features:
- Population-based learning (watch many snakes learn together!)
- Real-time visualization of AI decision making
- Genetic evolution over generations
- Performance tracking and statistics
"""

import numpy as np
import random
import pickle
import time
from datetime import datetime
import os
from snake_game import SnakeGame, SnakeGameVisual


class SimpleNeuralNetwork:
    """Lightweight feedforward neural network for Snake AI.
    
    Architecture: Input Layer → Hidden Layer → Output Layer
    - Input: Game state features (distances, food direction, etc.)
    - Hidden: ReLU activation  
    - Output: Action probabilities (Up, Right, Down, Left)
    """
    
    def __init__(self, input_size=15, hidden_size=12, output_size=4):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Initialize weights and biases with small random values
        self.weights1 = np.random.randn(input_size, hidden_size) * 0.5
        self.bias1 = np.random.randn(hidden_size) * 0.5
        self.weights2 = np.random.randn(hidden_size, output_size) * 0.5
        self.bias2 = np.random.randn(output_size) * 0.5
        
    def forward(self, inputs):
        """Forward pass through the network."""
        # Input to hidden layer
        hidden = np.dot(inputs, self.weights1) + self.bias1
        hidden = np.maximum(0, hidden)  # ReLU activation
        
        # Hidden to output layer
        outputs = np.dot(hidden, self.weights2) + self.bias2
        
        # Softmax for probability distribution
        exp_outputs = np.exp(outputs - np.max(outputs))  # Numerical stability
        probabilities = exp_outputs / np.sum(exp_outputs)
        
        return probabilities
        
    def get_action(self, game_state, valid_actions=None):
        """Get action from network output."""
        probabilities = self.forward(game_state)
        
        # If valid actions provided, mask invalid ones
        if valid_actions:
            masked_probs = np.zeros_like(probabilities)
            for action in valid_actions:
                masked_probs[action] = probabilities[action]
            
            # Renormalize
            if np.sum(masked_probs) > 0:
                probabilities = masked_probs / np.sum(masked_probs)
        
        # Choose action based on probabilities
        return np.random.choice(len(probabilities), p=probabilities)
        
    def mutate(self, mutation_rate=0.1, mutation_strength=0.3):
        """Apply random mutations to network weights."""
        # Mutate weights1
        mask = np.random.random(self.weights1.shape) < mutation_rate
        self.weights1[mask] += np.random.randn(*self.weights1[mask].shape) * mutation_strength
        
        # Mutate bias1
        mask = np.random.random(self.bias1.shape) < mutation_rate
        self.bias1[mask] += np.random.randn(*self.bias1[mask].shape) * mutation_strength
        
        # Mutate weights2
        mask = np.random.random(self.weights2.shape) < mutation_rate
        self.weights2[mask] += np.random.randn(*self.weights2[mask].shape) * mutation_strength
        
        # Mutate bias2
        mask = np.random.random(self.bias2.shape) < mutation_rate
        self.bias2[mask] += np.random.randn(*self.bias2[mask].shape) * mutation_strength
        
    def copy(self):
        """Create a deep copy of this network."""
        new_network = SimpleNeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        new_network.weights1 = self.weights1.copy()
        new_network.bias1 = self.bias1.copy()
        new_network.weights2 = self.weights2.copy()
        new_network.bias2 = self.bias2.copy()
        return new_network
        
    def crossover(self, other, crossover_rate=0.5):
        """Create offspring by mixing two parent networks."""
        child = self.copy()
        
        # Crossover weights1
        mask = np.random.random(self.weights1.shape) < crossover_rate
        child.weights1[mask] = other.weights1[mask]
        
        # Crossover bias1
        mask = np.random.random(self.bias1.shape) < crossover_rate
        child.bias1[mask] = other.bias1[mask]
        
        # Crossover weights2
        mask = np.random.random(self.weights2.shape) < crossover_rate
        child.weights2[mask] = other.weights2[mask]
        
        # Crossover bias2
        mask = np.random.random(self.bias2.shape) < crossover_rate
        child.bias2[mask] = other.bias2[mask]
        
        return child


class SnakeAI:
    """Snake AI agent using neural network."""
    
    def __init__(self, network=None):
        self.network = network or SimpleNeuralNetwork()
        self.fitness = 0
        self.score = 0
        self.moves = 0
        self.game_time = 0
        
    def play_game(self, max_moves=200, speed=1):
        """Play a complete game and return fitness score."""
        game = SnakeGame(speed=speed)
        game.max_moves = max_moves
        
        start_time = time.time()
        total_reward = 0
        
        while not game.game_over:
            state = game.get_game_state()
            if state is None:
                break
                
            valid_actions = game.get_valid_actions()
            action = self.network.get_action(state, valid_actions)
            
            _, reward, done, info = game.step(action)
            total_reward += reward
            
        self.game_time = time.time() - start_time
        self.score = game.score
        self.moves = game.moves
        
        # Calculate fitness (encourage longer survival and food collection)
        self.fitness = (
            game.score * 100 +           # Food bonus
            game.moves * 0.1 +           # Survival bonus
            total_reward * 0.5           # Reward bonus
        )
        
        return self.fitness


class GeneticAlgorithm:
    """Genetic algorithm for evolving Snake AI population."""
    
    def __init__(self, population_size=50, elite_size=10, mutation_rate=0.1):
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generation = 0
        
        # Create initial population
        self.population = [SnakeAI() for _ in range(population_size)]
        
        # Statistics tracking
        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.best_score_history = []
        
    def evaluate_population(self, max_moves=200, verbose=True):
        """Evaluate fitness of entire population."""
        if verbose:
            print(f"\n🧬 Generation {self.generation + 1} - Evaluating {self.population_size} snakes...")
            
        fitnesses = []
        scores = []
        
        for i, agent in enumerate(self.population):
            fitness = agent.play_game(max_moves=max_moves, speed=1)
            fitnesses.append(fitness)
            scores.append(agent.score)
            
            if verbose and (i + 1) % 10 == 0:
                print(f"   Evaluated {i + 1}/{self.population_size} snakes...")
                
        # Update statistics
        best_fitness = max(fitnesses)
        avg_fitness = np.mean(fitnesses)
        best_score = max(scores)
        
        self.best_fitness_history.append(best_fitness)
        self.avg_fitness_history.append(avg_fitness)
        self.best_score_history.append(best_score)
        
        if verbose:
            best_agent = self.population[np.argmax(fitnesses)]
            print(f"   🏆 Best: Score={best_agent.score}, Moves={best_agent.moves}, Fitness={best_fitness:.1f}")
            print(f"   📊 Average Fitness: {avg_fitness:.1f}")
            
        return best_fitness, avg_fitness, best_score
        
    def selection_and_reproduction(self):
        """Select best agents and create next generation."""
        # Sort population by fitness
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        # Keep elite agents
        new_population = []
        for i in range(self.elite_size):
            new_population.append(SnakeAI(self.population[i].network.copy()))
            
        # Create offspring through crossover and mutation
        while len(new_population) < self.population_size:
            # Tournament selection for parents
            parent1 = self.tournament_selection()
            parent2 = self.tournament_selection()
            
            # Crossover
            child_network = parent1.network.crossover(parent2.network)
            
            # Mutation
            child_network.mutate(self.mutation_rate)
            
            new_population.append(SnakeAI(child_network))
            
        self.population = new_population
        self.generation += 1
        
    def tournament_selection(self, tournament_size=5):
        """Select parent using tournament selection."""
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        return max(tournament, key=lambda x: x.fitness)
        
    def get_best_agent(self):
        """Get the best performing agent."""
        return max(self.population, key=lambda x: x.fitness)
        
    def save_progress(self, filename=None):
        """Save training progress and best agent."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"snake_ai_results_{timestamp}_G-{self.generation}.pkl"
            
        # Create simulation_saves directory if it doesn't exist
        os.makedirs("simulation_saves", exist_ok=True)
        filepath = os.path.join("simulation_saves", filename)
        
        data = {
            'generation': self.generation,
            'best_agent': self.get_best_agent(),
            'best_fitness_history': self.best_fitness_history,
            'avg_fitness_history': self.avg_fitness_history,
            'best_score_history': self.best_score_history,
            'population_size': self.population_size,
            'elite_size': self.elite_size,
            'mutation_rate': self.mutation_rate
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
            
        print(f"💾 Progress saved to {filepath}")
        return filepath


def train_snake_ai(generations=100, population_size=50, max_moves=200):
    """Train Snake AI using genetic algorithm."""
    print("🐍🧠 Welcome to Snake AI Training! 🧬✨")
    print("=" * 50)
    
    # Initialize genetic algorithm
    ga = GeneticAlgorithm(population_size=population_size)
    
    try:
        for gen in range(generations):
            # Evaluate current generation
            best_fitness, avg_fitness, best_score = ga.evaluate_population(max_moves=max_moves)
            
            # Save progress every 10 generations
            if (gen + 1) % 10 == 0:
                ga.save_progress()
                
            # Create next generation
            if gen < generations - 1:  # Don't evolve after last generation
                ga.selection_and_reproduction()
                
    except KeyboardInterrupt:
        print("\n⏹️ Training stopped by user.")
        
    # Final save
    final_file = ga.save_progress()
    
    print("\n🎉 Training Complete!")
    print(f"📈 Final best score: {max(ga.best_score_history)}")
    print(f"🏆 Final best fitness: {max(ga.best_fitness_history):.1f}")
    
    return ga, final_file


def demo_best_agent(filepath):
    """Load and demonstrate the best trained agent."""
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
        
    best_agent = data['best_agent']
    print(f"\n🎮 Demonstrating best agent from generation {data['generation']}")
    print(f"📊 Best score achieved: {max(data['best_score_history'])}")
    
    # Play visual game
    from turtle import ontimer, penup, goto, color, write
    game = SnakeGameVisual(speed=100)
    
    def ai_game_loop():
        if not game.game_over:
            state = game.get_game_state()
            if state is not None:
                valid_actions = game.get_valid_actions()
                action = best_agent.network.get_action(state, valid_actions)
                game.step(action)
                
            game.render()
            ontimer(ai_game_loop, game.speed)
        else:
            # Game over
            penup()
            goto(0, -50)
            color('blue')
            write(f'AI Final Score: {game.score}', align='center', font=('Arial', 16, 'bold'))
    
    ai_game_loop()


if __name__ == "__main__":
    print("🐍 Snake AI Training System 🧠")
    print("Choose an option:")
    print("1. Train new AI (100 generations)")
    print("2. Quick training session (20 generations)")
    print("3. Load and demo saved AI")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        ga, filepath = train_snake_ai(generations=100, population_size=50)
        demo_best_agent(filepath)
    elif choice == "2":
        ga, filepath = train_snake_ai(generations=20, population_size=30)
        demo_best_agent(filepath)
    elif choice == "3":
        # List available saves
        if os.path.exists("simulation_saves"):
            saves = [f for f in os.listdir("simulation_saves") if f.endswith('.pkl')]
            if saves:
                print("\nAvailable saves:")
                for i, save in enumerate(saves):
                    print(f"{i+1}. {save}")
                try:
                    idx = int(input("Choose save: ")) - 1
                    if 0 <= idx < len(saves):
                        demo_best_agent(os.path.join("simulation_saves", saves[idx]))
                except:
                    print("Invalid selection")
            else:
                print("No saved models found!")
        else:
            print("No simulation_saves directory found!")
    else:
        print("Invalid choice!")
