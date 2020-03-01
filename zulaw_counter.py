""" Autor - Marta Potocka - marta.m.potocka@gmail.com """

import os
import pathlib

FILES_TO_IGNORE = ["Podsumowanie wyników.txt", "lista.txt", 'README.txt']


class ZulawCounter():

    def __init__(self):
        self.current_dir = pathlib.Path(__file__).parent.absolute()
        self.list_of_cards = list()
        self.points_summary = dict()
        self.sorted_points_summary = dict()
        self.list_of_novels = list()

    def handle_list_of_novels(self):
        for f in os.listdir(self.current_dir):
            if f == "lista.txt":
                self.read_list(f)
                break
        print('Nie znaleziono pliku "lista.txt" zawierającego listę zgłoszeniową powieści.')
        decision = input('Czy chcesz [p]rzerwać działanie programu, czy [k]ontynuować? Naciśnij "p" lub "k" i Enter. ')
        if decision == 'p':
            quit()

    def read_list(self, list_file):
        with open(list_file, 'r', encoding='utf-8') as f:
            for line in 


    def create_list_of_cards(self):
        for f in os.listdir(self.current_dir):
            if f not in FILES_TO_IGNORE and f[-4:] == '.txt':
                self.list_of_cards.append(f)

    def print_list_of_cards(self):
        print("\nZnaleziono pliki:")
        for idx,cart in enumerate(self.list_of_cards, 1):
            print(f"{idx} - {cart}")

    def read_cards(self):
        for card in self.list_of_cards:
            self.read_single_card(card)

    def clean_spaces(self, splitted_line):
        for i in range(len(splitted_line)):
            splitted_line[i] = ' '.join(splitted_line[i].strip().split())
        return splitted_line

    def clean_author(self, author):
        for i in range(len(author)):
            if author[i] == '.' and author[i+1] != ' ':
                author = author[:(i+1)] + ' ' + author[(i+1):]
        author = author.lower().title()
        return author

    def clean_title(self, title):
        return title.lower().capitalize()

    def check_title_against_list(self, title):
        pass

    def read_line(self, line):
        splitted_line = line.split('\t')
        splitted_line = self.clean_spaces(splitted_line)
        author = self.clean_author(splitted_line[0])
        title = self.clean_title(splitted_line[1])
        self.check_title_against_list(title)
        novel = f'{author} - {title}'
        points = int(splitted_line[2])
        return (novel, points)

    def read_single_card(self, card):
        with open(card, 'r', encoding='utf-8') as f:
            for line in f:
                if line != "\n":
                    if line[-1] == '\n':
                        line = line[:-1]
                    novel, points = self.read_line(line)
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

        self.handle_list_of_novels()
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
