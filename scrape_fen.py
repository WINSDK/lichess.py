#!/usr/bin/python3.8
from PyQt5.QtWidgets import QLabel, QMainWindow, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QFileSystemWatcher
from PyQt5.QtGui import QPixmap
from threading import Thread
from bs4 import BeautifulSoup
from os import environ
import chess.engine
import chess.svg
import chess
import sys
import re
import logging
import asyncio
import dryscrape


class Incubator(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Chess Board Representation')
        self.setFixedSize(700, 700)
        self.initUI()

    def initUI(self):
        self.i = 1
        self.centering()
        self.content()
        self.show()

    def centering(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def content(self):
        self.i += 1
        if self.i % 2 == 0:
            pixmap = QPixmap("pos.svg")
            label = QLabel(self)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            self.setCentralWidget(label)


async def processing(FEN):  # Parses FEN into stockfish/engine of choice
    transport, engine = await chess.engine.popen_uci(f"{environ['HOME']}/.local/bin/lc0") 

    ############################## Settings start
    await engine.configure({"RamLimitMb": 4096})
    await engine.configure({"Threads": 2})
    ############################## Settings end

    board = chess.Board(FEN)
    result = await engine.play(board, chess.engine.Limit(time=2.5))
    result = re.search(r"\((.*)\)>", str(result))
    result = re.sub('info={}, ', '', result.group(1))
    await engine.quit()

    if board.is_stalemate() or board.is_game_over() or board.is_insufficient_material() is True:
        print("+----------------| game finished |----------------+")
        exit()

    move_from = result[5:7].upper()
    move_to = result[7:9].upper()
    SQUARES = [
        "A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1",
        "A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2",
        "A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3",
        "A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4",
        "A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5",
        "A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6",
        "A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7",
        "A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8",
    ]

    itr = 0
    for square in SQUARES:
        if move_from == square:
            move_from = itr
        if move_to == square:
            move_to = itr
        itr += 1

    flipping = None
    sides = re.search(r'\s(w|b)\s', FEN)
    if sides.group(1) == 'b':
        flipping = True
    else:
        flipping = False
    with open("pos.svg", 'w') as f:
        f.write(chess.svg.board(board=board, size=700, flipped=flipping, arrows=[(move_from, move_to)]))


def grabber():  # sends GET request to lichess & filters out FEN
    session.visit(url)
    soup = BeautifulSoup(session.body(), "lxml")
    script = soup.body.findAll('script')
    FEN = re.search('fen\":\"(.*)\",\"player\":', str(script))
    return FEN.group(1)


def runtime(FEN):
    global waiting
    waiting = True
    while True:
        check = grabber()
        sides = re.search(r'\s(w|b)\s', check)
        if check != FEN and sides.group(1) == clr:  # Checks whether an update in the chessboard occurred
            asyncio.run(processing(check))
            waiting = False
            logging.debug(f'Inverted  FEN: {check}')
        FEN = check


if __name__ == "__main__":
    app = QApplication(sys.argv)
    logging.basicConfig(filename='output.log', level=logging.DEBUG)
    asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
    dryscrape.start_xvfb()
    session = dryscrape.Session()
    url = input("Enter lichess URL: ")
    clr = input("Enter playing side (b or w): ")
    Thread(target=runtime, args=(" "), daemon=True).start()
    while waiting:
        pass
    win = Incubator()
    watcher = QFileSystemWatcher(['pos.svg'])
    watcher.fileChanged.connect(win.content)
    sys.exit(app.exec())