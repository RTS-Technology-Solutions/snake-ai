"""🐍 Snake AI Launcher: Your Gateway to AI Adventures! 🚀

Welcome to the ultimate Snake AI experience! This launcher gives you easy access 
to both classic and modern AI approaches for playing Snake.

Choose your adventure:
- 🧠 Expert System: Watch classical AI algorithms in action
- 🧬 Neural Network: Train and watch machine learning evolve
- 🤖 Head-to-Head: Compare both approaches side by side
"""

import os
import sys

def print_welcome():
    """Print the welcome screen."""
    print("=" * 70)
    print("🐍✨ WELCOME TO SNAKE AI ADVENTURES! ✨🐍")
    print("=" * 70)
    print()
    print("🎓 Educational AI Comparison Project")
    print("   Learn about Classical AI vs Modern Machine Learning!")
    print()
    print("🧠 Expert System: Instant intelligence using algorithms")
    print("🧬 Neural Network: Evolving intelligence through learning")
    print()

def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\n🚀 MAIN MENU - Choose Your AI Adventure:")
        print("=" * 50)
        print()
        print("🧠 EXPERT SYSTEM (Classical AI):")
        print("  1. Watch Expert System play (visual demo)")
        print("  2. Expert System performance test")
        print("  3. Expert vs Random comparison")
        print()
        print("🧬 NEURAL NETWORK (Machine Learning):")
        print("  4. Train new Neural Network (quick - 20 generations)")
        print("  5. Train new Neural Network (full - 100 generations)")
        print("  6. Watch trained Neural Network play")
        print("  7. Neural Network performance test")
        print()
        print("🤖 HEAD-TO-HEAD COMPARISONS:")
        print("  8. Side-by-side visual comparison")
        print("  9. Performance statistics comparison")
        print("  10. Educational learning progress demo")
        print()
        print("🎮 INTERACTIVE OPTIONS:")
        print("  11. Play Snake yourself (human vs AI)")
        print("  12. Create custom AI tournament")
        print()
        print("  0. Exit")
        print()
        
        try:
            choice = input("🎯 Enter your choice (0-12): ").strip()
            
            if choice == "0":
                print("\n🎉 Thanks for exploring Snake AI! Keep learning! 🚀")
                break
            elif choice == "1":
                run_expert_visual_demo()
            elif choice == "2":
                run_expert_performance_test()
            elif choice == "3":
                run_expert_vs_random()
            elif choice == "4":
                train_neural_network(quick=True)
            elif choice == "5":
                train_neural_network(quick=False)
            elif choice == "6":
                run_neural_visual_demo()
            elif choice == "7":
                run_neural_performance_test()
            elif choice == "8":
                run_side_by_side_comparison()
            elif choice == "9":
                run_performance_comparison()
            elif choice == "10":
                run_learning_progress_demo()
            elif choice == "11":
                run_human_vs_ai()
            elif choice == "12":
                run_custom_tournament()
            else:
                print("❌ Invalid choice! Please enter a number between 0-12.")
                
        except KeyboardInterrupt:
            print("\n\n🛑 Exiting Snake AI Adventures. See you later! 👋")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            input("Press Enter to continue...")

def run_expert_visual_demo():
    """Run expert system visual demonstration."""
    print("\n🧠 Starting Expert System Visual Demo...")
    try:
        from snake_engine import SnakeEngineDemo
        demo = SnakeEngineDemo()
        demo.demo_visual_game(speed=60)  # Faster for observation
    except Exception as e:
        print(f"❌ Error running expert demo: {e}")
        input("Press Enter to continue...")

def run_expert_performance_test():
    """Run expert system performance test."""
    print("\n🧠 Running Expert System Performance Test...")
    try:
        from snake_engine import SnakeEngineDemo
        demo = SnakeEngineDemo()
        demo.run_performance_test(num_games=10)
    except Exception as e:
        print(f"❌ Error running expert test: {e}")
    input("Press Enter to continue...")

def run_expert_vs_random():
    """Run expert system vs random player comparison."""
    print("\n🧠 vs 🎲 Expert System vs Random Player...")
    try:
        from snake_engine import SnakeEngineDemo
        demo = SnakeEngineDemo()
        demo.compare_with_human_demo()
    except Exception as e:
        print(f"❌ Error running comparison: {e}")
    input("Press Enter to continue...")

def train_neural_network(quick=True):
    """Train a neural network."""
    generations = 20 if quick else 100
    population = 30 if quick else 50
    
    print(f"\n🧬 Training Neural Network ({generations} generations)...")
    print("⏰ This may take a few minutes...")
    
    try:
        from snake_ai import train_snake_ai, demo_best_agent
        ga, filepath = train_snake_ai(generations=generations, population_size=population)
        
        print(f"\n🎉 Training complete! Best model saved to: {filepath}")
        
        choice = input("\n🎬 Start visual demo of trained AI? (y/n): ").strip().lower()
        if choice == 'y':
            demo_best_agent(filepath)
            
    except Exception as e:
        print(f"❌ Error during training: {e}")
    input("Press Enter to continue...")

def run_neural_visual_demo():
    """Run neural network visual demonstration."""
    print("\n🧬 Neural Network Visual Demo...")
    
    try:
        import os
        import pickle
        
        if not os.path.exists("simulation_saves"):
            print("❌ No trained models found! Please train a neural network first.")
            input("Press Enter to continue...")
            return
            
        saves = [f for f in os.listdir("simulation_saves") if f.endswith('.pkl')]
        if not saves:
            print("❌ No trained models found! Please train a neural network first.")
            input("Press Enter to continue...")
            return
            
        print("\n📁 Available trained models:")
        for i, save in enumerate(saves):
            # Load and show basic info
            try:
                with open(os.path.join("simulation_saves", save), 'rb') as f:
                    data = pickle.load(f)
                print(f"  {i+1}. {save} (Gen {data['generation']}, Best Score: {max(data['best_score_history'])})")
            except:
                print(f"  {i+1}. {save}")
                
        try:
            idx = int(input("\n🎯 Choose model to demo: ")) - 1
            if 0 <= idx < len(saves):
                from snake_ai import demo_best_agent
                demo_best_agent(os.path.join("simulation_saves", saves[idx]))
            else:
                print("❌ Invalid selection!")
        except:
            print("❌ Invalid selection!")
            
    except Exception as e:
        print(f"❌ Error running neural demo: {e}")
    input("Press Enter to continue...")

def run_neural_performance_test():
    """Run neural network performance test."""
    print("\n🧬 Neural Network Performance Test...")
    
    try:
        import os
        import pickle
        
        if not os.path.exists("simulation_saves"):
            print("❌ No trained models found! Please train a neural network first.")
            input("Press Enter to continue...")
            return
            
        saves = [f for f in os.listdir("simulation_saves") if f.endswith('.pkl')]
        if not saves:
            print("❌ No trained models found! Please train a neural network first.")
            input("Press Enter to continue...")
            return
            
        # Use latest model
        latest_save = max(saves, key=lambda x: os.path.getctime(os.path.join("simulation_saves", x)))
        
        with open(os.path.join("simulation_saves", latest_save), 'rb') as f:
            data = pickle.load(f)
        
        best_agent = data['best_agent']
        print(f"Testing model: {latest_save}")
        print(f"Generation: {data['generation']}")
        
        scores = []
        for i in range(10):
            fitness = best_agent.play_game(max_moves=300)
            scores.append(best_agent.score)
            print(f"Game {i+1}: Score = {best_agent.score}")
        
        print(f"\n📊 Results:")
        print(f"   Average Score: {sum(scores)/len(scores):.1f}")
        print(f"   Best Score: {max(scores)}")
        print(f"   Success Rate: {sum(1 for s in scores if s > 0)/len(scores)*100:.1f}%")
        
    except Exception as e:
        print(f"❌ Error running neural test: {e}")
    input("Press Enter to continue...")

def run_side_by_side_comparison():
    """Run side-by-side visual comparison."""
    print("\n🤖 Side-by-Side AI Comparison")
    print("This will show both AIs playing one after another...")
    
    input("🧠 Press Enter to start Expert System demo...")
    run_expert_visual_demo()
    
    input("🧬 Press Enter to start Neural Network demo...")
    run_neural_visual_demo()

def run_performance_comparison():
    """Run performance statistics comparison."""
    print("\n📊 Performance Statistics Comparison")
    try:
        from snake_engine import compare_ai_approaches
        compare_ai_approaches()
    except Exception as e:
        print(f"❌ Error running comparison: {e}")
    input("Press Enter to continue...")

def run_learning_progress_demo():
    """Run learning progress demonstration."""
    print("\n🎓 Educational Learning Progress Demo")
    
    try:
        import os
        if os.path.exists("simulation_saves"):
            saves = [f for f in os.listdir("simulation_saves") if f.endswith('.pkl')]
            if saves:
                latest_save = max(saves, key=lambda x: os.path.getctime(os.path.join("simulation_saves", x)))
                from snake_ai import demo_training_progress
                demo_training_progress(os.path.join("simulation_saves", latest_save))
            else:
                print("❌ No training data found! Train a neural network first.")
        else:
            print("❌ No training data found! Train a neural network first.")
    except Exception as e:
        print(f"❌ Error running learning demo: {e}")
    input("Press Enter to continue...")

def run_human_vs_ai():
    """Run human vs AI game."""
    print("\n🎮 Human vs AI Challenge")
    print("Play Snake yourself, then watch the AI try to beat your score!")
    
    try:
        from snake_game import SnakeGameVisual
        from turtle import done
        
        print("\n👤 Your turn! Use arrow keys to control the snake.")
        print("Close the window when you're done playing.")
        
        game = SnakeGameVisual(speed=100)  # Reasonable speed for human play
        game.play_human()
        
        human_score = game.score
        print(f"\n🏆 Your score: {human_score}")
        
        choice = input("🤖 Want to see if the AI can beat your score? (y/n): ").strip().lower()
        if choice == 'y':
            print("\n🧠 Expert System's turn...")
            from snake_engine import SnakeEngineDemo
            demo = SnakeEngineDemo()
            ai_score, _, _ = demo.play_single_game(max_moves=500)
            
            print(f"\n🏁 Results:")
            print(f"   👤 Your Score: {human_score}")
            print(f"   🤖 AI Score: {ai_score}")
            
            if ai_score > human_score:
                print(f"   🤖 AI wins by {ai_score - human_score} points!")
            elif human_score > ai_score:
                print(f"   👤 You win by {human_score - ai_score} points! Great job!")
            else:
                print(f"   🤝 It's a tie! Both scored {human_score} points!")
                
    except Exception as e:
        print(f"❌ Error running human vs AI: {e}")
    input("Press Enter to continue...")

def run_custom_tournament():
    """Run custom AI tournament."""
    print("\n🏆 Custom AI Tournament")
    print("Create your own AI competition!")
    
    try:
        print("\n🎯 Tournament Options:")
        print("1. Expert System vs Multiple Random Opponents")
        print("2. Best Neural Networks Tournament")
        print("3. Evolution Showcase (multiple generations)")
        
        choice = input("Choose tournament type (1-3): ").strip()
        
        if choice == "1":
            print("\n🧠 Expert System vs Random Players Tournament")
            from snake_engine import SnakeEngineDemo
            demo = SnakeEngineDemo()
            
            expert_scores = []
            random_scores = []
            
            for round_num in range(5):
                print(f"\n🎮 Round {round_num + 1}/5")
                expert_score, random_score = demo.compare_with_human_demo()
                expert_scores.append(expert_score)
                random_scores.append(random_score)
            
            print(f"\n🏆 Tournament Results:")
            print(f"   Expert System - Average: {sum(expert_scores)/len(expert_scores):.1f}")
            print(f"   Random Players - Average: {sum(random_scores)/len(random_scores):.1f}")
            print(f"   Expert wins: {sum(1 for i in range(5) if expert_scores[i] > random_scores[i])}/5 rounds")
            
        elif choice == "2":
            print("\n🧬 Neural Network Tournament")
            import os
            if os.path.exists("simulation_saves"):
                saves = [f for f in os.listdir("simulation_saves") if f.endswith('.pkl')]
                if len(saves) >= 2:
                    print(f"Found {len(saves)} trained models. Testing top performers...")
                    # Tournament implementation would go here
                    print("🚧 Tournament feature coming soon!")
                else:
                    print("❌ Need at least 2 trained models for tournament!")
            else:
                print("❌ No trained models found!")
                
        elif choice == "3":
            print("\n🎓 Evolution Showcase")
            print("🚧 Evolution showcase feature coming soon!")
            
        else:
            print("❌ Invalid choice!")
            
    except Exception as e:
        print(f"❌ Error running tournament: {e}")
    input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        print_welcome()
        main_menu()
    except KeyboardInterrupt:
        print("\n\n🛑 Goodbye! Thanks for exploring Snake AI! 👋")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your installation and try again.")