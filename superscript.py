import sys
import asyncio
import argparse
from stdlib import SuperError
from lexer import Lexer

parser = argparse.ArgumentParser(prog="superscript", description="Program anything, the fun way.")
parser.add_argument("file", type=str, help="What file should we run?", nargs="?", default=None)
parser.add_argument("--debug", help="Get more information", action="store_true")
args = parser.parse_args()
from rich.console import Console
from rich.panel import Panel

console = Console()


debug = False

if args.debug:
    debug = True
    print("Debug mode on. GLHF!")



if True:
    with open("test.super", "r") as file:
        text = file.read()
    
    text = "\n" + " " + text  
    lexer = Lexer(text)
    try:
        tokens = lexer.scanTokens()
    
    except SuperError as e:
        line = str(e).split("|")[0]
        col = str(e).split("|")[1]
        msg = str(e).split("|")[2]
        console.print(Panel.fit(f"Whoops! During lexing I found an error on [green][i][b]line {line}[blue], column {col}:\n[red][not i]{msg}     ", title="[red]:warning-emoji: [bold]ERROR" ))
        sys.exit(1)
    finally:
        if debug:
            print(tokens)
