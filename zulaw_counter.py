""" Autor - Marta Potocka - marta.m.potocka@gmail.com """

import os
import pathlib


class ZulawCounter():

    def __init__(self):
        self.current_dir = pathlib.Path(__file__).parent.absolute()
        self.list_of_cards = list()
        self.points_summary = dict()
        self.sorted_points_summary = dict()

    def create_list_of_cards(self):
        for f in os.listdir(self.current_dir):
            if f != "Podsumowanie wyników.txt" and f[-4:] == '.txt':
                self.list_of_cards.append(f)

    def print_list_of_cards(self):
        print("\nZnaleziono pliki:")
        for idx,cart in enumerate(self.list_of_cards, 1):
            print(f"{idx} - {cart}")

    def read_cards(self):
        for card in self.list_of_cards:
            self.read_single_card(card)

    def read_single_card(self, card):
        with open(card, 'r', encoding='utf-8') as f:
            for line in f:
                if line != "\n":
                    if line[-1] == '\n':
                        line = line[:-1]
                    splitted = line.split('\t')
                    for i in range(len(splitted)):
                        splitted[i] = splitted[i].strip()
                    novel = f'{splitted[0]} - "{splitted[1]}"'
                    points = int(splitted[2])
                    self.write_to_summary(novel,points)

    def write_to_summary(self, novel, points):
        if novel in self.points_summary.keys():
            self.points_summary[novel] += points
        else:
            self.points_summary[novel] = points

    def sort_results(self):
        self.sorted_points_summary = {k:v for k,v in sorted(self.points_summary.items(), key = lambda item:item[1], reverse=True)}

    def print_results(self):
        print("\nPodsumowanie:")
        for idx, novel in enumerate(self.sorted_points_summary, 1):
            print(f"{idx} - {novel} - {self.sorted_points_summary[novel]} punktów.")

    def print_results_to_file(self):
        with open("Podsumowanie wyników.txt", "w", encoding='utf-8') as f:
            f.write("Podsumowanie wyników:\n\n")
            for idx, novel in enumerate(self.sorted_points_summary, 1):
                f.write(f"{idx} - {novel} - {self.sorted_points_summary[novel]} punktów.\n")

    def run(self):
        print("*** Witaj w programie ŻuławCounter ***")

        self.create_list_of_cards()
        self.print_list_of_cards()
        self.read_cards()
        self.sort_results()
        self.print_results()
        self.print_results_to_file()

        print("\nPlik 'Podsumowanie wyników.txt' został wygenerowany.")
        input("\nNaciśnij Enter by zamknąć program.")


if __name__ == '__main__':

    zc = ZulawCounter()
    zc.run()
