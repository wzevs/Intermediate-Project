#!/usr/bin/env python3
"""
შუალედური პროექტი: მთავარი გამშვები ფაილი
აერთიანებს დავალებებს ერთ მთავარ მენიუში.
"""

import sys
import calculator
import guess_number
import hangman
import translator
import atm

def show_menu() -> None:
    """ბეჭდავს მთავარ მენიუს კონსოლში."""
    print("\n" + "=" * 50)
    print("    შუალედური პროექტი: პითონის კურსი (Backend)")
    print("=" * 50)
    print("1. კალკულატორი")
    print("2. რიცხვის გამოცნობა")
    print("3. Hangman (ჩამოხრჩობანა)")
    print("4. თარჯიმანი")
    print("5. ბანკომატის სიმულატორი")
    print("0. პროგრამიდან გასვლა")
    print("=" * 50)

def main() -> None:
    while True:
        show_menu()
        choice = input("აირჩიეთ მოდული (0-5): ").strip()

        if choice == "1":
            print("\n--- ირთვება კალკულატორი ---")
            calculator.run_calculator()  # შეცვალე შენი ფუნქციის სახელით
            
        elif choice == "2":
            print("\n--- ირთვება რიცხვის გამოცნობა ---")
            guess_number.run_guess_number()  # შეცვალე შენი ფუნქციის სახელით
            
        elif choice == "3":
            print("\n--- ირთვება Hangman ---")
            hangman.run_hangman()  # შეცვალე შენი ფუნქციის სახელით
            
        elif choice == "4":
            print("\n--- ირთვება თარჯიმანი ---")
            translator.run_translator()  # შეცვალე შენი ფუნქციის სახელით
            
        elif choice == "5":
            print("\n--- ირთვება ბანკომატი ---")
            atm.run_atm()  # ეს ზუსტად ვიცით, რომ ასე დავარქვით
            
        elif choice == "0":
            print("\nპროგრამა დასრულებულია. ნახვამდის!")
            sys.exit()
            
        else:
            print("\n❌ არასწორი არჩევანი. გთხოვთ შეიყვანოთ რიცხვი 0-დან 5-მდე.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nპროგრამა შეწყდა მომხმარებლის მიერ (Ctrl+C).")
        sys.exit()