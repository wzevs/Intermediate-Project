#!/usr/bin/env python3
"""
მოდული : თარჯიმანი (ტექსტურ ფაილზე ბაზირებული ლექსიკონი)
ინახავს და კითხულობს სიტყვებს dictionary.txt ფაილიდან.
თუ სიტყვა არ არსებობს, მომხმარებელს შეუძლია მისი ბაზაში დამატება.
"""

import os

DICTIONARY_FILE = "dictionary.txt"

# ფაილში სვეტების გამყოფი სიმბოლო — არ შეიძლება შედიოდეს
# შეყვანილ სიტყვაში ან თარგმანში, რადგან წინააღმდეგ შემთხვევაში
# ჩანაწერის სტრუქტურა დაირღვევა
DELIMITER = "|"


def load_dictionary() -> dict[str, dict[str, str]]:
    """
    კითხულობს dictionary.txt-ს და აბრუნებს სტრუქტურირებულ dict-ს:
    { "ka-en": {"გამარჯობა": "hello"}, "en-ka": {"hello": "გამარჯობა"} ... }
    """
    # თუ ფაილი არ არსებობს, ვქმნით ცარიელს
    if not os.path.exists(DICTIONARY_FILE):
        with open(DICTIONARY_FILE, "w", encoding="utf-8") as file:
            pass
        return {}

    dictionary: dict[str, dict[str, str]] = {}
    with open(DICTIONARY_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or DELIMITER not in line:
                continue
            # ფაილის ფორმატი: ენის_წყვილი|სიტყვა|თარგმანი (მაგ: ka-en|წყალი|water)
            # maxsplit=2 იმისთვის, რომ თარგმანში შემთხვევით მოხვედრილმა
            # დამატებითმა "|" სიმბოლომ ჩანაწერი არ დაშალოს
            parts = line.split(DELIMITER, maxsplit=2)
            if len(parts) != 3:
                continue
            direction, word, translation = parts
            if not word or not translation:
                continue
            if direction not in dictionary:
                dictionary[direction] = {}
            dictionary[direction][word.lower()] = translation
    return dictionary


def save_word_to_file(direction: str, word: str, translation: str) -> None:
    """ამატებს ახალ სიტყვას ტექსტური ფაილის ბოლოში."""
    with open(DICTIONARY_FILE, "a", encoding="utf-8") as file:
        file.write(f"{direction}{DELIMITER}{word.lower()}{DELIMITER}{translation}\n")


def get_translation_direction() -> str:
    """მომხმარებელს აარჩევინებს თარგმნის მიმართულებას."""
    print("აირჩიეთ თარგმნის მიმართულება:")
    print("1. ქართული -> ინგლისური (ka-en)")
    print("2. ინგლისური -> ქართული (en-ka)")
    print("3. ქართული -> რუსული (ka-ru)")
    print("4. რუსული -> ქართული (ru-ka)")

    mapping = {"1": "ka-en", "2": "en-ka", "3": "ka-ru", "4": "ru-ka"}

    while True:
        choice = input("თქვენი არჩევანი (1-4): ").strip()
        if choice in mapping:
            return mapping[choice]
        print("❌ არასწორი არჩევანი. გთხოვთ აირჩიოთ 1-დან 4-მდე.\n")


def get_word_to_translate() -> str:
    """
    ითხოვს მომხმარებლისგან სათარგმნ სიტყვას/ფრაზას (ან 'exit' სიტყვას გამოსასვლელად)
    და ამოწმებს, რომ იგი არ შეიცავდეს გამყოფ სიმბოლოს (რაც ფაილის სტრუქტურას დაარღვევდა).
    """
    while True:
        word = input("\nშეიყვანეთ სათარგმნი სიტყვა (ან 'exit' გასასვლელად): ").strip()
        if not word:
            continue
        if word.lower() == "exit":
            return word
        if DELIMITER in word:
            print(f"❌ შეცდომა: სიტყვა/ფრაზა არ უნდა შეიცავდეს '{DELIMITER}' სიმბოლოს.\n")
            continue
        return word


def get_translation_input(word: str) -> str:
    """
    ითხოვს მომხმარებლისგან თარგმანს და ამოწმებს, რომ ცარიელი არ იყოს
    და არ შეიცავდეს გამყოფ სიმბოლოს.
    """
    while True:
        translation = input(f"შეიყვანეთ '{word}'-ის თარგმანი: ").strip()
        if not translation:
            print("❌ თარგმანი ცარიელი არ უნდა იყოს.\n")
            continue
        if DELIMITER in translation:
            print(f"❌ შეცდომა: თარგმანი არ უნდა შეიცავდეს '{DELIMITER}' სიმბოლოს.\n")
            continue
        return translation


def run_translator() -> None:
    print("=" * 40)
    print("             მოდული: თარჯიმანი")
    print("=" * 40)

    direction = get_translation_direction()
    dictionary = load_dictionary()

    print(f"\nთქვენ აირჩიეთ მიმართულება: {direction}. თარგმნის შესაწყვეტად ჩაწერეთ 'exit'.")

    while True:
        word = get_word_to_translate()
        if word.lower() == "exit":
            print("თარჯიმნის მოდული დაიხურა.")
            break

        # მიმდინარე მიმართულების ლექსიკონის შემოწმება
        current_dict = dictionary.get(direction, {})

        if word.lower() in current_dict:
            print(f"✅ თარგმანი: {current_dict[word.lower()]}")
        else:
            print(f"🔍 სიტყვა '{word}' ლექსიკონში ვერ მოიძებნა.")
            add_new = input("გსურთ ამ სიტყვის თარგმანის დამატება? (კი/არა): ").strip().lower()

            if add_new in ("კი", "დიახ", "yes", "y"):
                translation = get_translation_input(word)
                # ვინახავთ ფაილში
                save_word_to_file(direction, word, translation)
                # ვანახლებთ მეხსიერებაშიც, რომ ხელახლა წაკითხვა არ დაგვჭირდეს
                if direction not in dictionary:
                    dictionary[direction] = {}
                dictionary[direction][word.lower()] = translation
                print("🎉 ახალი სიტყვა წარმატებით დაემატა ლექსიკონს!")


if __name__ == "__main__":
    try:
        run_translator()
    except KeyboardInterrupt:
        print("\n\nმოდული შეწყდა მომხმარებლის მიერ.")