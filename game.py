from agent import run_agent

def start_game():
    print("Welcome to the dungeon of doom!")
    name = input("What is your name, bold adventurer? ")
    print(f'Greetings, {name}! You find yourself at the entrance to a dark and mysterious dungeon.')
    while True:
        choice = input("\nWhat do you do? ")
        if choice.lower() == "quit":
            break
        try:
            response = run_agent(choice)
            print(response)
        except Exception as e:
            print(f"[Error] {str(e)}")
            print("Let's try again...")

if __name__ == "__main__":
    start_game()