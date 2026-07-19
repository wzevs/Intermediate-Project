#!/usr/bin/env python3
"""
თამაში : გამოიცანით რიცხვი
პროგრამა აგენერირებს შემთხვევით რიცხვს მითითებულ დიაპაზონში.
მომხმარებელი ცდილობს გამოიცნოს, პროგრამა კი აძლევს მინიშნებებს.
მოიცავს:
- შეყვანილი მნიშვნელობების ვალიდაციას
- მცდელობების რაოდენობის კონტროლს
- დიაპაზონის მოქნილ პარამეტრებს
"""
import random


def get_valid_int(prompt: str) -> int:
    """
    ითხოვს მომხმარებლისგან მთელ რიცხვს, სანამ არ შეიყვანს ვალიდურ მნიშვნელობას.
    """
    while True:
        raw_value = input(prompt).strip()
        try:
            return int(raw_value)
        except ValueError:
            print(f"❌ შეცდომა: '{raw_value}' არ არის მთელი რიცხვი. სცადეთ თავიდან.\n")


def get_range() -> tuple[int, int]:
    """
    ითხოვს მომხმარებლისგან დიაპაზონის ორივე საზღვარს (low, high) ცალ-ცალკე
    ცვლადებში და ვალიდაციას უწევს, რომ low < high იყოს.
    """
    while True:
        low = get_valid_int("შეიყვანეთ დიაპაზონის ქვედა საზღვარი: ")
        high = get_valid_int("შეიყვანეთ დიაპაზონის ზედა საზღვარი: ")
        if low < high:
            return low, high
        print(f"❌ შეცდომა: ქვედა საზღვარი ({low}) უნდა იყოს ზედა საზღვარზე ({high}) "
              f"ნაკლები. სცადეთ თავიდან.\n")


def get_max_attempts() -> int:
    """
    ითხოვს მომხმარებლისგან მაქსიმალურ მცდელობათა რაოდენობას (დადებითი მთელი რიცხვი).
    """
    while True:
        max_attempts = get_valid_int("შეიყვანეთ მაქსიმალური მცდელობების რაოდენობა: ")
        if max_attempts > 0:
            return max_attempts
        print("❌ შეცდომა: მცდელობების რაოდენობა უნდა იყოს დადებითი რიცხვი.\n")


def run_guess_game(low: int, high: int, max_attempts: int) -> None:
    """
    აშვებს რიცხვის გამოცნობის თამაშის მთავარ ლოგიკას მითითებულ დიაპაზონსა
    და მცდელობათა ლიმიტში.
    """
    print(f"\nმე ჩავიფიქრე რიცხვი {low}-დან {high}-მდე. გაქვთ {max_attempts} მცდელობა. აბა, თუ გამოიცნობ?\n")

    secret_number = random.randint(low, high)
    attempts = 0

    while attempts < max_attempts:
        guess = get_valid_int(f"შეიყვანეთ თქვენი ვარაუდი ({max_attempts - attempts} მცდელობა დარჩა): ")

        if guess < low or guess > high:
            print(f"⚠️  გთხოვთ, აირჩიოთ რიცხვი {low}-დან {high}-მდე დიაპაზონში (მცდელობა არ ჩაითვალა).\n")
            continue

        attempts += 1

        if guess < secret_number:
            print("🔼 უფრო მაღალი! სცადეთ თავიდან.\n")
        elif guess > secret_number:
            print("🔽 უფრო დაბალი! სცადეთ თავიდან.\n")
        else:
            print(f"\n🎉 ყოჩაღ! შენ გამოიცანი სწორი რიცხვი: {secret_number}")
            print(f"📊 მცდელობების რაოდენობა: {attempts}\n")
            return

    print(f"\n😢 მცდელობები ამოიწურა! სწორი რიცხვი იყო: {secret_number}\n")


def main() -> None:
    print("=" * 40)
    print("       თამაში: გამოიცანი რიცხვი")
    print("=" * 40)

    while True:
        low, high = get_range()
        max_attempts = get_max_attempts()
        run_guess_game(low, high, max_attempts)

        again = input("გსურთ თამაშის თავიდან დაწყება? (დიახ/არა): ").strip().lower()
        if again not in ("დიახ", "კი", "yes", "y"):
            print("\nნახვამდის! 👋")
            break
        print()


if __name__ == "__main__":
    # ეს ხაზი უზრუნველყოფს, რომ ფაილის პირდაპირ გაშვებისას თამაში ჩაირთოს
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nთამაში შეწყდა მომხმარებლის მიერ. ნახვამდის! 👋")