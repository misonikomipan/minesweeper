import random
import sys


# 各マスのオブジェクト
class Grid:
    def __init__(self) -> None:
        self.isBomb = False
        self.isOpen = False
        self.isFrag = False
        self.nAroundBomb = 0
    
    def __str__(self):
        # print(obj)での出力
        state = ("#" if self.isBomb else self.nAroundBomb) if self.isOpen else "."
        return f"{state}"


# ゲーム用オブジェクト
class MineSweeper:
    def __init__(self, nRow, nCol, nBomb, isDebug = True) -> None:
        self.nRow = nRow
        self.nCol = nCol
        self.nSize = self.nRow * self.nCol
        self.board = [[Grid() for iCol in range(nCol)] for iRow in range(nRow)]
        self.nBomb = nBomb
        self.isPlay = True
        self.bombPosList = self.setBomb()
        self.calcAroundBombs()
        # デバッグ用
        if isDebug:
            self.debug()
        else:
            pass

    def __str__(self):
        return f"{self.nBomb}"
            
    def debug(self):
        print(self.bombPosList)
        for r in range(self.nRow):
            for c in range(self.nCol):
                print(self.board[r][c], end = " ")
            print()
    
    def setBomb(self):
        # 爆弾座標の決定
        bombPosList1d = random.sample(range(self.nSize), k=self.nBomb)
        bomPosList2d = tuple(map(divmod, bombPosList1d, [self.nCol for iBomb in range(self.nBomb)])) # (r, c)
        # 盤面に反映
        # TODO: for文を排除 
        for (r, c) in bomPosList2d: 
            self.board[r][c].isBomb = True
        
        return bomPosList2d

    def calcAroundBombs(self):
        for (r, c) in self.bombPosList:
            for dr in range(-1, 2): # [-1, 1]
                for dc in range(-1, 2): # [-1, 1]
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < self.nRow) and (0 <= nc < self.nCol): # 枠内だよ
                        self.board[nr][nc].nAroundBomb += 1
                    else:
                        continue
    
    def openGrid(self, iRow, iCol):
        self.board[iRow][iCol].isOpen = True
        if self.board[iRow][iCol].nAroundBomb == 0:
            for dr in range(-1, 2): # [-1, 1]
                for dc in range(-1, 2): # [-1, 1]
                    nr, nc = iRow + dr, iCol + dc
                    if (0 <= nr < self.nRow) and (0 <= nc < self.nCol): # 枠内だよ
                        if self.board[nr][nc].isOpen:
                            continue
                        else:
                            self.openGrid(nr, nc)
                    else:
                        continue
    
    def judgeIsLose(self):
        currentNBombOpen = sum([sum([(boardElement.isOpen and boardElement.isBomb) for boardElement in boardRow]) for boardRow in self.board])
        if currentNBombOpen > self.nBomb:
            raise ValueError("爆弾の数が合わないよ")
        else:
            return bool(currentNBombOpen)

    def judgeIsWin(self):
        # 敗北判定の後にやらないかん
        requiredNOpen = self.nSize - self.nBomb
        currentNOpen = sum([sum([boardElement.isOpen for boardElement in boardRow]) for boardRow in self.board])
        
        if requiredNOpen - currentNOpen < 0:
            raise ValueError("爆弾の数が合わないよ")
        elif requiredNOpen - currentNOpen == 0:
            return True
        else:
            return False


def deleteConsole(nRow):
    # N行上にカーソルを移動
    sys.stdout.write(f"\033[{nRow}A")
    # そこからすべてを削除
    sys.stdout.write("\033[0J")


def main():
    
    game = MineSweeper(20, 10, 10)
    while game.isPlay:
        isValidGrid = False
        while not(isValidGrid):
            iRow, iCol = map(int, input("行・列番号を空白区切りで入力").split())
            isValidGrid = (0 <= iRow < game.nRow) and (0 <= iCol < game.nCol)
        # マス開ける
        game.openGrid(iRow, iCol)
        deleteConsole(100)
        game.debug()
        # 敗北判定
        if game.judgeIsLose():
            print("敗北！")
            game.isPlay = False
        # 勝利判定
        if game.isPlay and game.judgeIsWin():
            print("勝利！")
            game.isPlay = False

if __name__ == "__main__":
    main()