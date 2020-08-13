import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore

args = sys.argv
directory = args[1]

if not os.path.exists(directory):
    os.mkdir(directory)

page_stack = deque()

while True:
    inp = input()
    if inp == 'exit':
        break
    elif inp == 'back':
        if len(page_stack) > 0:
            page_stack.pop() # Remove current page
            page = page_stack.pop()
            page_stack.append(page) # Add again as current page
            with open("{}/{}".format(directory, page), 'r') as f:
                for line in f:
                    print(line.strip())
    elif '.' not in inp:
        if os.path.exists("{}/{}".format(directory, inp)):
            with open("{}/{}".format(directory, inp), 'r') as f:
                page_stack.append(inp)
                for line in f:
                    print(line.strip())
        else:
            print("Error: Incorrect URL")
    else:
        if not inp.startswith("https://"):
            url = "https://{}".format(inp)
        else:
            url = inp
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        tags = soup.find_all(['p', 'a', 'ul', 'ol', 'li'])
        page_content = ''
        for tag in tags:
            if tag.name == 'a':
                page_content += Fore.BLUE + tag.text + Fore.RESET + '\n'
            else:
                page_content += tag.text + '\n'
        fname = url.rsplit('.', 1)[0][8:]
        with open("{}/{}".format(directory, fname), 'w') as f:
            f.write(page_content)
        page_stack.append(fname)
        print(page_content)
