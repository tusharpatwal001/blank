import streamlit as st
from colorama import Fore, Back

# heading
st.header("Tokenizer")

# input

input_text = st.text_area("", max_chars=500, placeholder="Enter some text")

# output
st.write(input_text)

from main2 import create_token

output = create_token(input_text)

col1, col2 = st.columns(2)

col1.write("Tokens")
col1.write(len(output))

col2.write("Characters")
col2.write(len(input_text))


def color_strings(
    string_list,
    colors=[Back.LIGHTMAGENTA_EX, Back.GREEN, Back.YELLOW, Back.RED, Back.BLUE],
):
    """
    Prints each string in the list with a color from the colors list,
    cycling through the colors in order.
    """
    num_colors = len(colors)
    # print(num_colors)

    output_str = ""
    for index, text in enumerate(string_list):
        # print(index, text)
        # Determine which color to use based on the index (cycling every 5 items)
        color_code = colors[index % num_colors]
        # print(f"{index=}  % { num_colors=} = {index%num_colors}")

        # Print the colored string
        # Style.RESET_ALL is handled by autoreset=True, but good practice to be explicit if needed
        output_str += f"{color_code + text + Fore.BLACK} "
    return output_str


cont = st.container(border=True,  height=200)
cont.write(color_strings(output))  # type: ignore
