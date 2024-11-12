import markdown 
import os

from build_dataset import build_dataset
from markdown_to_html import markdown_to_html


def main():
    """
    """

    print("running main")

    tasks = [0, 1]


    # create records from metadata 
    # populate records with wearable data \
    if 0 in tasks: markdown_to_html()
    if 1 in tasks: build_dataset()
        
    #markdown_to_html()



    print("completed main")


if __name__ == "__main__":
    main()
