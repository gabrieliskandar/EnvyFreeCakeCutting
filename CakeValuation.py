from abc import ABC, abstractmethod

class CakeValuation(ABC):

    """
    Takes in n (nPieces), and returns n-1 cuts
    that divide the cake into n equal pieces.
    """
    @abstractmethod
    def divideCakeEqually(self, nPieces):
        pass

    """
    Takes a piece between 2 cuts and 
    returns the value of that piece
    """
    @abstractmethod
    def evalCakePiece(self, pieceStart, pieceEnd):
        pass

    """
    Takes a piece between 2 cuts, and returns another cut 
    so that the right-most piece is equal to the targetValue.
    """
    @abstractmethod
    def trimPieceToValue(self, pieceStart, pieceEnd, targetValue):
        pass