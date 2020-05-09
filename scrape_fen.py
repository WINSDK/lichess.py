#!/usr/bin/python3.8
from bs4 import BeautifulSoup
import chess.engine
import chess
import re
import os
import logging
import asyncio
import dryscrape

async def processing(FEN): # Parses FEN into stockfish/engine of choice
    transport, engine = await chess.engine.popen_uci(f"{os.environ['HOME']}/.local/bin/lc0") 
    
    ############################## Settings start
    await engine.configure({"RamLimitMb": 4096})
    await engine.configure({"Threads": 10})
    ############################## Settings end
    
    board = chess.Board(FEN)
    try:
        result = await engine.play(board, chess.engine.Limit(time=5))
    except:
        print("+----------------| game finished |----------------+")
        exit()
    result = re.search(r"\((.*)\)>", str(result))
    result = re.sub('info={}, ', '', result.group(1))
    await engine.quit()

    print(board)
    print(result)

def grabber(): # sends GET request to lichess & filters out FEN
    session.visit(url)
    soup = BeautifulSoup(session.body(), "lxml")
    script = soup.body.findAll('script') 
    FEN = re.search('fen\":\"(.*)\",\"player\":', str(script))
    return FEN.group(1)

if __name__ == "__main__":
    logging.basicConfig(filename='output.log',level=logging.DEBUG)
    asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
    dryscrape.start_xvfb()
    session = dryscrape.Session()
    url = input("Enter lichess URL: ")
    clr = input("Enter playing side (b or w): ")
    FEN = ""

    while True: 
        check = grabber()
        sides = re.search(r'\s(w|b)\s', check)
        if check != FEN and sides.group(1) == clr: # Checks whether an update in the chessboard occurred
            asyncio.run(processing(check))
            logging.debug(f'Inverted  FEN: {check}')
        FEN = check