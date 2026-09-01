# Format: \033[Style;ColorCode;BackgroundModem
# \033[0m resets the text back to default


# type - 1
##############################################################################
# print("\033[31mThis text is Red\033[0m")
# print("\033[32mThis text is Green\033[0m")
# print("\033[34mThis text is Blue\033[0m")

# # Combined styling: Bold (1) + Yellow Text (33) + Black Background (40m)
# print("\033[1;33;40mBold Yellow Text on Black Background\033[0m")
##############################################################################

# type - 2
##############################################################################
# from colorama import Fore, Back, Style

# # Simple color changes
# print(Fore.RED + "This is red text" + Style.RESET_ALL)
# print(Fore.GREEN + "This is green text" + Style.RESET_ALL)

# # Mixing foreground, background, and brightness
# print(Back.CYAN + Fore.BLACK + "Black text on Cyan background" + Style.RESET_ALL) ## use this one tommorow 
# print(Style.BRIGHT + Fore.YELLOW + "Bright Yellow text" + Style.RESET_ALL)
##############################################################################


# type - 3

##############################################################################

from termcolor import colored, cprint

# Method A: Assign the colored text string to a variable
red_text = colored("Hello, World!", "red")
print(red_text)

# Method B: Print directly with cprint
cprint("Green text with a red background", "green", "on_red") # or use this one to create token in colourfule way like in openai website

# Method C: Adding attributes like bold or underline
cprint("Bold and underlined cyan text", "cyan", attrs=["bold", "underline"])

##############################################################################
