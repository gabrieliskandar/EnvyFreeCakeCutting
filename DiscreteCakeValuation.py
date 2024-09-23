from CakeValuation import CakeValuation

class DiscreteCakeValuation(CakeValuation):

    # A cake is divided into n pieces, where values[i] is the value of the ith piece.
    # Cake is of range 0 to n.
    def __init__(self, values):
        super().__init__()
        self.values = values

    def getValue(self, start, end):
        return sum(self.values[start:end])

    def setValue(self, position, value):
        self.values[position] = value

    # Returns the cuts (between 0-n) that divide the cake into n equal pieces.
    def divideCakeEqually(self, nPieces):
        totalValue = sum(self.values)
        targetPieceValue = totalValue / nPieces
        cuts = []

        currentPieceValue = 0
        for i in range(0, len(self.values)):
            currentPieceValue += self.values[i]

            if currentPieceValue >= targetPieceValue:
                if currentPieceValue > targetPieceValue:
                    print("Warning: Piece value is greater than target value")
                cuts.append(i + 1)
                currentPieceValue = 0
        return cuts[:-1]
    
    def evalCakePiece(self, pieceStart, pieceEnd):
        return self.getValue(pieceStart, pieceEnd)
    
    def trimPieceToValue(self, pieceStart, pieceEnd, targetValue):
        pieceValue = self.getValue(pieceStart, pieceEnd)
        if pieceValue == targetValue:
            return pieceStart
        elif pieceValue < targetValue:
            print("Warning: Piece value is less than target value")
            return pieceStart
        else:
            cutLocation = pieceEnd
            while cutLocation > pieceStart:
                rightValue = self.getValue(cutLocation, pieceEnd)
                if rightValue == targetValue:
                    return cutLocation
                elif rightValue < targetValue:
                    # Continue searching to the left
                    cutLocation -= 1
                else:
                    # Piece is too large now
                    print("Warning: Could not find a cut that makes the piece equal to targetValue")
                    return cutLocation
            return pieceStart