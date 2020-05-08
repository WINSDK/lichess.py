#!/usr/bin/python3.7
from bs4 import BeautifulSoup
import chess.engine
import chess
import re
import logging
import asyncio
import dryscrape

async def processing(FEN): # Parses FEN into stockfish/engine of choice
    transport, engine = await chess.engine.popen_uci("/bin/stockfish") 

    ############################## Settings start
    await engine.configure({"Hash": 16})
    await engine.configure({"Threads": 5})
    await engine.configure({"Slow Mover": 100})
    await engine.configure({"SyzygyProbeDepth": 1})
    ############################## Settings end

    board = chess.Board(FEN)
    result = await engine.play(board, chess.engine.Limit(depth=20))
    result = re.search(r"\((.*)\)>", str(result))
    result = re.sub('info={}, ', '', result.group(1))
    await engine.quit()

    if board.is_stalemate() or board.is_game_over() or board.is_insufficient_material() == True:
        print("+----------------| game finished |----------------+")
        exit()

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