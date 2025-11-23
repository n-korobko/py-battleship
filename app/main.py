from typing import List, Tuple, Optional


class Deck:
    def __init__(
            self,
            row: int,
            column: int,
            is_alive: bool = True
    ) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(
            self,
            start: Tuple[int, int],
            end: Tuple[int, int],
            is_drowned: bool = False
    ) -> None:
        self.is_drowned = is_drowned
        self.decks = []

        start_row, start_col = start
        end_row, end_col = end
        if start_row == end_row:
            for col in range(min(start_col, end_col),
                             max(start_col, end_col) + 1):
                self.decks.append(Deck(start_row, col))

        else:
            for row in range(min(start_row, end_row),
                             max(start_row, end_row) + 1):
                self.decks.append(Deck(row, start_col))

    def get_deck(self, row: int, column: int) -> Optional[Deck]:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> None:
        deck = self.get_deck(row, column)
        if deck is None:
            return

        deck.is_alive = False

        if all(not d.is_alive for d in self.decks):
            self.is_drowned = True


class Battleship:
    def __init__(
            self,
            ships: List[
                Tuple[Tuple[int, int], Tuple[int, int]]
            ]
    ) -> None:
        self.field = {}
        for ship_start, ship_end in ships:
            ship = Ship(ship_start, ship_end)

            for deck in ship.decks:
                self.field[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        row, col = location

        if (row, col) not in self.field:
            return "Miss!"

        ship = self.field[(row, col)]
        ship.fire(row, col)

        if ship.is_drowned:
            return "Sunk!"
        return "Hit!"
