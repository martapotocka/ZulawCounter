""" Autor - Marta Potocka - marta.m.potocka@gmail.com """

import os
import sys
import pathlib

ACCEPTED_NOVELS = "lista.txt"
FILES_TO_IGNORE = ["Podsumowanie wyników.txt", ACCEPTED_NOVELS, 'README.txt']


class ZulawCounter:

    def __init__(self):
        self.current_dir = pathlib.Path(__file__).parent.absolute()
        self.list_of_cards = list()
        self.points_summary = dict()
        self.sorted_points_summary = dict()
        self.list_of_accepted_novels = list()
        self.list_of_accepted_authors = list()

    def handle_list_of_accepted_novels_and_authors(self):
        if os.path.isfile(ACCEPTED_NOVELS):
            self.read_list_of_accepted_novels_and_authors(ACCEPTED_NOVELS)
        else:
            print(f'\nNie znaleziono pliku "{ACCEPTED_NOVELS}" zawierającego listę zgłoszeniową powieści.')
            while True:
                decision = input(
                    'Czy chcesz [p]rzerwać działanie programu, czy [k]ontynuować? Naciśnij "p" lub "k" i Enter. ')
                if decision == 'k':
                    break
                elif decision == 'p':
                    sys.exit()
                else:
                    continue

    def read_list_of_accepted_novels_and_authors(self, list_file):
        with open(list_file, 'r', encoding='utf-8') as f:
            for line in f:
                author, novel = line.split('\t')
                author = self.clean_author(author.strip())
                novel = self.clean_title(novel[:-1].strip())
                self.list_of_accepted_authors.append(author)
                self.list_of_accepted_novels.append(novel)

    def create_list_of_cards(self):
        for f in os.listdir(self.current_dir):
            if f not in FILES_TO_IGNORE and f[-4:] == '.txt':
                self.list_of_cards.append(f)

    def print_list_of_cards(self):
        print("\nZnalezione karty do głosowania:")
        for idx, cart in enumerate(self.list_of_cards, 1):
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
            if author[i] == '.' and author[i + 1] != ' ':
                author = author[:(i + 1)] + ' ' + author[(i + 1):]
        author = author.lower().title()
        return author

    def clean_title(self, title):
        return title.lower().capitalize()

    def check_title_against_list_of_accepted_novels(self, title, card):
        if self.list_of_accepted_novels:
            if title not in self.list_of_accepted_novels:
                print(
                    f'\nPowieść "{title}" z karty do głosowania: {card} nie znajduje się na liście zgłoszeniowej (w pliku {ACCEPTED_NOVELS}).')
                print("Program zostanie zamknięty.")
                print(
                    f'Zanim ponownie go uruchomisz dodaj powieść "{title}" do listy zgłoszeniowej, lub usuń ją z karty do głosowania: {card}.')
                input('Nacisnij Enter aby zamknąć program.')
                sys.exit()

    def check_author_against_list_of_accepted_authors(self, author, card):
        if self.list_of_accepted_authors:
            if author not in self.list_of_accepted_authors:
                print(
                    f'\nAutor "{author}" z karty do głosowania: {card} nie znajduje się na liście zgłoszeniowej (w pliku {ACCEPTED_NOVELS}).')
                print("Program zostanie zamknięty.")
                print(
                    f'Zanim ponownie go uruchomisz dodaj autora "{author}" do listy zgłoszeniowej, lub usuń go z karty do głosowania: {card}.')
                input('Nacisnij Enter aby zamknąć program.')
                sys.exit()

    def read_line(self, line, card):
        splitted_line = line.split('\t')
        splitted_line = self.clean_spaces(splitted_line)
        author = self.clean_author(splitted_line[0])
        title = self.clean_title(splitted_line[1])
        self.check_title_against_list_of_accepted_novels(title, card)
        self.check_author_against_list_of_accepted_authors(author, card)
        novel = f'{author} - {title}'
        points = int(splitted_line[2])
        return novel, points

    def read_single_card(self, card):
        with open(card, 'r', encoding='utf-8-sig') as f:
            for line in f:
                if line != "\n":
                    if line[-1] == '\n':
                        line = line[:-1]
                    novel, points = self.read_line(line, card)
                    self.write_to_summary(novel, points)

    def write_to_summary(self, novel, points):
        if novel in self.points_summary.keys():
            self.points_summary[novel] += points
        else:
            self.points_summary[novel] = points

    def sort_results(self):
        self.sorted_points_summary = {k: v for k, v in
                                      sorted(self.points_summary.items(), key=lambda item: item[1], reverse=True)}

    def print_results(self):
        print("\nPodsumowanie:")
        for idx, novel in enumerate(self.sorted_points_summary, 1):
            print(f"{idx} - {novel} - {self.sorted_points_summary[novel]} punktów.")

    def print_results_to_file(self):
        with open("Podsumowanie wyników.txt", "w", encoding='utf-8-sig') as f:
            f.write("Podsumowanie wyników:\n\n")
            for idx, novel in enumerate(self.sorted_points_summary, 1):
                f.write(f"{idx} - {novel} - {self.sorted_points_summary[novel]} punktów.\n")

    def run(self):
        print("*** Witaj w programie ŻuławCounter ***")

        self.handle_list_of_accepted_novels_and_authors()
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
