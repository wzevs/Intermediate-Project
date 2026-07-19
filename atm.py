#!/usr/bin/env python3
"""
მოდული : ბანკომატის სიმულატორი
ინახავს მომხმარებლის ანგარიშებს accounts.txt ფაილში.
მოიცავს ავტორიზაციას, ბალანსის შემოწმებას, თანხის შეტანას და გატანას.
"""

import os
from typing import Optional

ACCOUNTS_FILE = "accounts.txt"
DEFAULT_BALANCE = 500.0

# საწყისი ანგარიშები (თუ ფაილი არ არსებობს)
# ფორმატი: ანგარიში:PIN:სახელი:გვარი:ასაკი:ბალანსი
DEFAULT_ACCOUNTS = {
    "1001": {
        "pin": "1234",
        "first_name": "გიორგი",
        "last_name": "ბერიძე",
        "age": 25,
        "balance": DEFAULT_BALANCE,
    },
    "1002": {
        "pin": "5678",
        "first_name": "ნინო",
        "last_name": "ქავთარაძე",
        "age": 30,
        "balance": DEFAULT_BALANCE,
    },
}


def load_accounts() -> dict:
    """კითხულობს ყველა ანგარიშს ფაილიდან. თუ ფაილი არ არსებობს, ქმნის დეფოლტ ანგარიშებს."""
    if not os.path.exists(ACCOUNTS_FILE):
        save_accounts(DEFAULT_ACCOUNTS)
        return {acc: data.copy() for acc, data in DEFAULT_ACCOUNTS.items()}
    
    accounts = {}
    try:
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                parts = line.split(":")
                if len(parts) != 6:
                    continue
                
                account_id, pin, first_name, last_name, age_str, balance_str = parts
                accounts[account_id.strip()] = {
                    "pin": pin.strip(),
                    "first_name": first_name.strip(),
                    "last_name": last_name.strip(),
                    "age": int(age_str.strip()),
                    "balance": float(balance_str.strip()),
                }
    except (ValueError, IOError):
        save_accounts(DEFAULT_ACCOUNTS)
        return {acc: data.copy() for acc, data in DEFAULT_ACCOUNTS.items()}
    
    if not accounts:
        save_accounts(DEFAULT_ACCOUNTS)
        return {acc: data.copy() for acc, data in DEFAULT_ACCOUNTS.items()}
    
    return accounts


def save_accounts(accounts: dict) -> None:
    """ინახავს ყველა ანგარიშს ტექსტურ ფაილში."""
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as file:
        file.write("# ანგარიში:PIN:სახელი:გვარი:ასაკი:ბალანსი\n")
        for account_id, data in accounts.items():
            file.write(
                f"{account_id}:{data['pin']}:{data['first_name']}:"
                f"{data['last_name']}:{data['age']}:{data['balance']:.2f}\n"
            )


def full_name(account: dict) -> str:
    """აბრუნებს სახელს და გვარს ერთ სტრიქონად."""
    return f"{account['first_name']} {account['last_name']}"


def authenticate(accounts: dict) -> Optional[str]:
    """ითხოვს ანგარიშის ნომერს და PIN-ს. წარმატებისას აბრუნებს ანგარიშის ID-ს."""
    account_id = input("შეიყვანეთ ანგარიშის ნომერი: ").strip()
    if account_id not in accounts:
        print("❌ ანგარიში ვერ მოიძებნა!\n")
        return None
    
    pin = input("შეიყვანეთ PIN კოდი: ").strip()
    if pin != accounts[account_id]["pin"]:
        print("❌ არასწორი PIN კოდი!\n")
        return None
    
    account = accounts[account_id]
    print(
        f"✅ გამარჯობა, {full_name(account)}! "
        f"(ასაკი: {account['age']}, ანგარიში: {account_id})\n"
    )
    return account_id


def get_valid_amount(prompt: str) -> float:
    """ითხოვს თანხის ოდენობას და ამოწმებს, რომ დადებითი რიცხვი იყოს."""
    while True:
        try:
            amount = float(input(prompt).strip())
            if amount > 0:
                return amount
            print("❌ შეცდომა: თანხა უნდა იყოს დადებითი რიცხვი!\n")
        except ValueError:
            print("❌ შეცდომა: გთხოვთ შეიყვანოთ ვალიდური რიცხვი!\n")


def check_balance(accounts: dict, account_id: str) -> None:
    """აჩვენებს მომხმარებლის მონაცემებს და მიმდინარე ბალანსს."""
    account = accounts[account_id]
    print(f"\n👤 მფლობელი: {full_name(account)}")
    print(f"🎂 ასაკი: {account['age']}")
    print(f"💰 ბალანსი: {account['balance']:.2f} ლარი")


def deposit(accounts: dict, account_id: str) -> None:
    """თანხის შეტანა ანგარიშზე და ფაილის განახლება."""
    amount = get_valid_amount("\nშეიყვანეთ შესატანი თანხის ოდენობა: ")
    accounts[account_id]["balance"] += amount
    save_accounts(accounts)
    print(
        f"✅ თანხა წარმატებით შემოვიდა. "
        f"ახალი ბალანსი: {accounts[account_id]['balance']:.2f} ლარი"
    )


def withdraw(accounts: dict, account_id: str) -> None:
    """თანხის გატანა ანგარიშიდან (საკმარისი ბალანსის შემოწმებით)."""
    amount = get_valid_amount("\nშეიყვანეთ გასატანი თანხის ოდენობა: ")
    balance = accounts[account_id]["balance"]
    
    if amount > balance:
        print(
            f"❌ ტრანზაქცია უარყოფილია: ანგარიშზე არ არის საკმარისი თანხა! "
            f"(ბალანსი: {balance:.2f} ლარი)"
        )
        return
    
    accounts[account_id]["balance"] -= amount
    save_accounts(accounts)
    print(
        f"✅ თანხა გაცემულია. "
        f"დარჩენილი ბალანსი: {accounts[account_id]['balance']:.2f} ლარი"
    )


def show_accounts(accounts: dict) -> None:
    """აჩვენებს ხელმისაწვდომ ანგარიშებს ფაილიდან წაკითხული მონაცემებით."""
    print("\nსატესტო ანგარიშები:")
    for account_id, data in accounts.items():
        print(
            f"  {account_id} — {full_name(data)} "
            f"(ასაკი: {data['age']}, PIN: {data['pin']})"
        )


def run_atm() -> None:
    print("=" * 40)
    print("             მოდული: ბანკომატი")
    print("=" * 40)
    
    accounts = load_accounts()
    show_accounts(accounts)
    
    account_id = None
    while account_id is None:
        account_id = authenticate(accounts)
        if account_id is None:
            retry = input("გსურთ თავიდან ცდა? (კ/ა): ").strip().lower()
            if retry not in ("კ", "k", "yes", "y", "კი"):
                print("ბანკომატის მოდული დაიხურა.")
                return
                
    while True:
        print("\nხელმისაწვდომი ოპერაციები:")
        print("1. ბალანსის შემოწმება")
        print("2. თანხის შეტანა")
        print("3. თანხის გატანა")
        print("0. გასვლა")
        
        choice = input("აირჩიეთ ოპერაცია (0-3): ").strip()
        
        if choice == "1":
            check_balance(accounts, account_id)
        elif choice == "2":
            deposit(accounts, account_id)
        elif choice == "3":
            withdraw(accounts, account_id)
        elif choice == "0":
            print("ბანკომატის მოდული დაიხურა.")
            break
        else:
            print("❌ არასწორი არჩევანი. სცადეთ თავიდან.")


if __name__ == "__main__":
    try:
        run_atm()
    except KeyboardInterrupt:
        print("\n\nმოდული შეწყდა მომხმარებლის მიერ.")