import ipaddress
import time
import sys
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# Colors for each letter
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

# Message
message = "Merry Christmas!"

# Display the message with colors
def colorful_message(msg):
    for char in msg:
        if char.isalpha():
            color = colors[ord(char) % len(colors)]
            sys.stdout.write(color + char)
        else:
            sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)
    print()  # Move to the next line

# Border for the message
def display_border():
    print(Back.GREEN + Fore.WHITE + "*" * 30)

# Main function
def main():
    for i in range(10):
        display_border()
        colorful_message(message)
        display_border()

if __name__ == "__main__":
    main()
