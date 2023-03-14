
#Klasa reprezentująca gracza w grze
class Player: 
    def __init__(self, char: str) -> None:
 
        #pojedynczy ciąg znaków reprezentujący gracza w tekstowej reprezentacji stanu gry

        if len(char) != 1:
            raise ValueError('Postać reprezentująca gracza powinna mieć długość 1') 

        self.char = char
