#!/usr/bin/env python3
"""
თამაში : Hangman (სიტყვების გამოცნობა)
პროგრამა ირჩევს შემთხვევით სიტყვას (ჰინტთან ერთად) და მომხმარებელი ცდილობს
მის გამოცნობას ასო-ასო ან პირდაპირ მთელი სიტყვის შეტანით.

მოიცავს:
- სიტყვების ლექსიკონს (word -> hint), საიდანაც ხდება შემთხვევითი არჩევა
- ჰინტის ჩვენებას თამაშის დაწყებისას და მოთხოვნისამებრ (შეიყვანეთ "?")
- შეყვანილი ასოების ვალიდაციას (მხოლოდ ერთი ქართული ასო)
- მთელი სიტყვის ერთბაშად გამოცნობის შესაძლებლობას
- უკვე გამოყენებული ასოების კონტროლს
- მცდელობების დინამიკურ ჩვენებას (ASCII ფიგურით)
- სიცოცხლეების მოქნილ, მომხმარებლის მიერ განსაზღვრულ რაოდენობას
- სესიის მასშტაბით მოგება/წაგების სტატისტიკას
"""

import random

# ქართული ანბანის ასოები — გამოიყენება შესატანი ასოს ვალიდაციისთვის
GEORGIAN_LETTERS = set("აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ")

# სიტყვების ლექსიკონი: სიტყვა -> ჰინტი
WORDS = {
    "პითონი": "პროგრამირების ენა, სახელწოდებული გველის მიხედვით",
    "პროგრამირება": "კომპიუტერული კოდის წერის პროცესი",
    "დეველოპერი": "ადამიანი, რომელიც წერს პროგრამებს",
    "კომპიუტერი": "მოწყობილობა, რომელზეც მუშაობს ეს პროგრამა",
    "მონაცემები": "ინფორმაცია, რომელსაც პროგრამა ამუშავებს",
    "ალგორითმი": "ნაბიჯების თანმიმდევრობა ამოცანის გადასაჭრელად",
    "ფუნქცია": "კოდის ბლოკი, რომელსაც შეგვიძლია მრავალჯერ გამოვიძახოთ",
    "ცვლადი": "სახელი, რომელშიც მონაცემს ვინახავთ",
}

# Hangman-ის ვიზუალური სტადიები, ინდექსირებული არასწორი მცდელობების რაოდენობით
HANGMAN_STAGES = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========""",
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    ========="""
]


def get_random_word() -> tuple[str, str]:
    """
    აბრუნებს შემთხვევით (სიტყვა, ჰინტი) წყვილს WORDS ლექსიკონიდან.
    შეგიძლია სიტყვები და ჰინტები შენი სურვილისამებრ შეცვალო ან დაამატო.
    """
    word = random.choice(list(WORDS.keys()))
    hint = WORDS[word]
    return word, hint


def get_max_lives() -> int:
    """
    ითხოვს მომხმარებლისგან სიცოცხლეების (დასაშვები შეცდომების) რაოდენობას.
    დასაშვებია მხოლოდ 1-დან 6-მდე, რადგან ASCII ფიგურას ამდენივე სტადია აქვს.
    """
    min_lives = 1
    max_lives_limit = len(HANGMAN_STAGES) - 1  # ამჟამად 6

    while True:
        raw_value = input(
            f"რამდენი სიცოცხლე გსურთ თამაშისთვის? (აირჩიეთ {min_lives}-დან {max_lives_limit}-მდე): "
        ).strip()
        try:
            max_lives = int(raw_value)
        except ValueError:
            print(f" შეცდომა: '{raw_value}' არ არის მთელი რიცხვი. სცადეთ თავიდან.\n")
            continue
        if max_lives < min_lives or max_lives > max_lives_limit:
            print(f" შეცდომა: აირჩიეთ რიცხვი {min_lives}-დან {max_lives_limit}-მდე დიაპაზონში.\n")
            continue
        return max_lives


def get_valid_letter(used_letters: set) -> str:
    """
    ითხოვს მომხმარებლისგან ერთ ქართულ ასოს, ამოწმებს ვალიდაციას
    აგრეთვე იმას, არის თუ არა ეს ასო უკვე გამოყენებული.
    """
    while True:
        letter = input("შემოიტანეთ ასო: ").strip().lower()

        # ვალიდაცია 1: ცარიელი შეყვანა ან ერთზე მეტი სიმბოლო
        if len(letter) != 1:
            print(" შეცდომა: გთხოვთ შემოიტანოთ მხოლოდ ერთი ასო!\n")
            continue

        # ვალიდაცია 2: მხოლოდ ქართული ანბანის ასოები
        if letter not in GEORGIAN_LETTERS:
            print(f" შეცდომა: '{letter}' არ არის ქართული ანბანის ასო.\n")
            continue

        # ვალიდაცია 3: უკვე გამოყენებული ასო
        if letter in used_letters:
            print(f"  ასო '{letter}' უკვე ნაცადი გაქვთ. აირჩიეთ სხვა.\n")
            continue

        return letter


def get_user_guess(used_letters: set, hint: str) -> tuple[str, str]:
    """
    ითხოვს მომხმარებლისგან შეყვანას, რომელიც შეიძლება იყოს:
    - ერთი ქართული ასო
    - მთელი სიტყვა (თუ მომხმარებელი მიხვდა)
    - "?" ან "ჰინტი" — ჰინტის ხელახლა სანახავად, ცხოვრებას არ აკლებს

    აბრუნებს წყვილს: (ტიპი, მნიშვნელობა), სადაც ტიპი არის "letter" ან "word".
    """
    while True:
        raw = input("შემოიტანეთ ასო, ან თუ მიხვდით — მთელი სიტყვა (ჰინტისთვის აკრიფეთ '?'): ").strip().lower()

        if raw in ("?", "ჰინტი"):
            print(f" ჰინტი: {hint}\n")
            continue

        if len(raw) == 0:
            print(" შეცდომა: შეყვანა ცარიელია. სცადეთ თავიდან.\n")
            continue

        if len(raw) == 1:
            if raw not in GEORGIAN_LETTERS:
                print(f" შეცდომა: '{raw}' არ არის ქართული ანბანის ასო.\n")
                continue
            if raw in used_letters:
                print(f"  ასო '{raw}' უკვე ნაცადი გაქვთ. აირჩიეთ სხვა.\n")
                continue
            return "letter", raw

        # თუ ერთზე მეტი სიმბოლოა შეყვანილი — ეს არის მთელი სიტყვის მცდელობა
        return "word", raw


def display_current_state(word: str, guessed_letters: set) -> str:
    """
    ქმნის და აბრუნებს სიტყვის მიმდინარე ვიზუალურ მდგომარეობას ტირეებით და გამოცნობილი ასოებით.
    მაგალითად: პ _ თ _ ნ ი
    """
    displayed_word = []
    for letter in word:
        if letter in guessed_letters:
            displayed_word.append(letter)
        else:
            displayed_word.append("_")
    return " ".join(displayed_word)


def run_hangman_game(max_lives: int) -> bool:
    """
    აშვებს Hangman თამაშის მთავარ ლოგიკას მითითებული სიცოცხლეების რაოდენობით.
    აბრუნებს True, თუ მომხმარებელმა გაიმარჯვა, წინააღმდეგ შემთხვევაში False.
    """
    print("=" * 40)
    print("            თამაში: Hangman")
    print("=" * 40)

    secret_word, hint = get_random_word()
    guessed_letters: set = set()
    wrong_attempts = 0

    print(f"სიტყვა ჩაფიქრებულია! გაქვთ უფლება შეცდეთ {max_lives}-ჯერ.")
    print(f" ჰინტი: {hint}\n")

    while wrong_attempts < max_lives:
        current_view = display_current_state(secret_word, guessed_letters)
        print(HANGMAN_STAGES[wrong_attempts])
        print(f"\nსიტყვა: {current_view}")
        print(f"გამოყენებული ასოები: {', '.join(sorted(guessed_letters)) if guessed_letters else 'ჯერ არ არის'}")
        print(f"  დარჩენილი სიცოცხლე: {max_lives - wrong_attempts}\n")

        if "_" not in current_view:
            print(f" გილოცავთ! თქვენ გამოიცანით სიტყვა: {secret_word}\n")
            return True

        guess_type, guess = get_user_guess(guessed_letters, hint)

        if guess_type == "word":
            if guess == secret_word:
                # მომხმარებელმა წინასწარ მიხვდა მთელ სიტყვას
                guessed_letters.update(secret_word)
                print(f" ზუსტად მიხვდით! სიტყვა იყო: {secret_word}\n")
                return True
            else:
                wrong_attempts += 1
                print(f" არასწორია! სიტყვა '{guess}' არ არის სწორი პასუხი.\n")
            continue

        # guess_type == "letter"
        letter = guess
        guessed_letters.add(letter)

        if letter in secret_word:
            print(f" სწორია! ასო '{letter}' არის სიტყვაში.\n")
        else:
            wrong_attempts += 1
            print(f" არასწორია! ასო '{letter}' არ არის სიტყვაში.\n")

    print(HANGMAN_STAGES[wrong_attempts])
    print("\n სამწუხაროდ წააგეთ! ლიმიტი ამოიწურა.")
    print(f" ჩაფიქრებული სიტყვა იყო: {secret_word}\n")
    return False


def main() -> None:
    wins = 0
    losses = 0

    while True:
        max_lives = get_max_lives()
        won = run_hangman_game(max_lives)

        if won:
            wins += 1
        else:
            losses += 1

        print(f" სტატისტიკა ამ სესიაში — მოგება: {wins}, წაგება: {losses}\n")

        again = input("გსურთ კიდევ თამაში? (დიახ/არა): ").strip().lower()
        if again not in ("დიახ", "კი", "yes", "y"):
            print("\nნახვამდის! ")
            break
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nთამაში შეწყდა მომხმარებლის მიერ. ნახვამდის! ")