import keyboard
import os
import time

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def select_menu(options):
    index = 0

    while True:
        clear()
        print("Use ↑ ↓ to navigate. Press Enter to select.\n")

        for i, option in enumerate(options):
            if i == index:
                print(f"> {option}")
            else:
                print(f"  {option}")

        key = keyboard.read_key()

        if key == "up":
            index = (index - 1) % len(options)
        elif key == "down":
            index = (index + 1) % len(options)
        elif key == "enter":
            return options[index]

        time.sleep(0.1)

# Example
options = ["Apple", "Banana", "Cherry", "Exit"]
selected = select_menu(options)
print(f"\nYou selected: {selected}")
