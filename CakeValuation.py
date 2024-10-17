from typing import List, Tuple
from abc import ABC, abstractmethod
import warnings

class CakeValuation(ABC):
    id = -1
    imaginaryValues = []

    @abstractmethod
    def getId(self) -> int:
        pass

    @abstractmethod
    def setImaginaryValues(self, values: List[int]):
        pass

    """
    Get the new imaginary value in the list.
    """
    @abstractmethod
    def getNextImaginaryValue(self) -> int:
        pass

    """
    Takes in n (nPieces), and returns n-1 cuts
    that divide the cake into n equal pieces.
    """
    @abstractmethod
    def divideCakeEqually(self, nPieces: int) -> List[int]:
        pass

    """
    Takes a piece between 2 cuts and 
    returns the value of that piece
    """
    @abstractmethod
    def evalCakePiece(self, pieceStart: int, pieceEnd: int) -> int:
        pass

    """
    Takes a piece between 2 cuts, and returns another cut 
    so that the right-most piece is equal to the targetValue.
    """
    @abstractmethod
    def trimPieceToValue(self, pieceStart: int, pieceEnd: int, targetValue: int) -> int:
        pass

    """
    Ranks the pieces by value, from highest to lowest.
    """
    @abstractmethod
    def rankPiecesByValue(self, pieces: List[Tuple[int, int, Tuple[int]]]) -> List[Tuple[int, int, Tuple[int]]]:
        pass

class DiscreteCakeValuation(CakeValuation):
    # A cake is divided into n pieces, where values[i] is the value of the ith piece.
    # Cake is of range 0 to n.

    def __init__(self, values, id: int):
        super().__init__()
        self.values = values
        self.id = id
        self.pieceImaginaryValues = {}

    def getValue(self, start, end):
        return sum(self.values[start:end])

    def setValue(self, position, value):
        self.values[position] = value
    
    def getId(self) -> int:
        return self.id
    
    def setImaginaryValues(self, values: List[int]):
        self.imaginaryValues = values
    
    def getNextImaginaryValue(self) -> int:
        if (not self.imaginaryValues):
            warnings.warn("No more imaginary values")
            return 0
        return self.imaginaryValues.pop()

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
                    warnings.warn("Piece value is greater than target value")
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
            warnings.warn("Piece value is less than target value")
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
                    warnings.warn("Could not find a cut that makes the piece equal to targetValue")
                    return cutLocation
            if self.getValue(pieceStart, pieceEnd) != targetValue:
                warnings.warn("Could not find a cut that makes the piece equal to targetValue")
            return pieceStart
        
    def rankPiecesByValue(self, pieces):
        sortedPieces = sorted(pieces, key=lambda x: self.getValue(x[0], x[1]), reverse=True)
        swap = True
        # Need to handle tie cases
        while swap:
            swap = False
            for (i, piece) in enumerate(sortedPieces):
                if i == 0:
                    continue
                if self.getValue(piece[0], piece[1]) == self.getValue(sortedPieces[i-1][0], sortedPieces[i-1][1]):
                    # In case of tie of values, default to imaginary values, if the current piece has a larger imaginary piece, swap the pieces
                    if compareImaginaryValues(piece[2], sortedPieces[i-1][2]):
                        sortedPieces[i] = sortedPieces[i-1]
                        sortedPieces[i-1] = piece
                        swap = True
        return sortedPieces

"""
Function to compare a list of imaginary values, to determine which list has the first unique smallest value. If the first list has a smaller value, return True, otherwise return False.
This means that if first list has a larger imaginary piece, return True.
"""
def compareImaginaryValues(imaginaryValues1: Tuple[int], imaginaryValues2: Tuple[int]) -> bool:
    if (imaginaryValues1 == imaginaryValues2):
        warnings.warn("Imaginary values are equal")
        return False
    if (len(imaginaryValues1) == 0):
        warnings.warn("Imaginary values are empty")
        return False
    if (len(imaginaryValues2) == 0):
        warnings.warn("Imaginary values are empty")
        return True
    list1 = sorted(imaginaryValues1)
    list2 = sorted(imaginaryValues2)
    for i in range(0, len(list1)):
        if (i >= len(list2)):
            return True
        if (list1[i] < list2[i]):
            return True
        elif (list1[i] > list2[i]):
            return False
    return True