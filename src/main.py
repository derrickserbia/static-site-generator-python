from textnode import *
from helper_methods import split_nodes_image


def main():
    node = TextNode(
        "This is text with an image ![this iamge](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        text_type_text,
    )
    new_nodes = split_nodes_image([node])
    print(new_nodes)


main()
