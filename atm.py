#!/usr/bin/env python3
"""
მოდული : ბანკომატის სიმულატორი
ინახავს მომხმარებლის ანგარიშებს accounts.txt ფაილში.
მოიცავს ავტორიზაციას, ახალი ანგარიშის რეგისტრაციას, ბალანსის შემოწმებას,
თანხის შეტანას/გატანას და ტრანზაქციების ლოგირებას (transactions.txt).
"""

import os
from datetime import datetime
from typing import Optional

ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_FILE = "transactions.txt"
DEFAULT_BALANCE = 500.0
MIN_AGE = 18
MAX_AGE = 120

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


# ---------- ტრანზაქციების ლოგირება ----------

def log_transaction(account_id: str, tx_type: str, amount: float, balance_after: float) -> None:
    """
    ამატებს ერთ ჩანაწერს ტრანზაქციების ლოგ-ფაილში.
    ფორმატი: თარიღი-დრო:ანგარიში:ტიპი:თანხა:ბალანსი_ტრანზაქციის_შემდეგ
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp}:{account_id}:{tx_type}:{amount:.2f}:{balance_after:.2f}\n"
    try:
        with open(TRANSACTIONS_FILE, "a", encoding="utf-8") as file:
            file.write(line)
    except IOError as error:
        print(f" ტრანზაქციის ლოგირება ვერ მოხერხდა: {error}")


def get_transactions(account_id: str) -> list[dict]:
    """კითხულობს და აბრუნებს მითითებული ანგარიშის ყველა ტრანზაქციას ლოგ-ფაილიდან."""
    if not os.path.exists(TRANSACTIONS_FILE):
        return []

    records = []
    try:
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":")
                if len(parts) != 5:
                    continue
                timestamp, acc_id, tx_type, amount_str, balance_str = parts
                if acc_id != account_id:
                    continue
                try:
                    records.append(
                        {
                            "timestamp": timestamp,
                            "type": tx_type,
                            "amount": float(amount_str),
                            "balance_after": float(balance_str),
                        }
                    )
                except ValueError:
                    continue
    except IOError as error:
        print(f" ტრანზაქციების ფაილის წაკითხვა ვერ მოხერხდა: {error}")

    return records


def show_transaction_history(account_id: str) -> None:
    """აჩვენებს მითითებული ანგარიშის ტრანზაქციების ისტორიას ქრონოლოგიური თანმიმდევრობით."""
    records = get_transactions(account_id)
    print(f"\n--- ტრანზაქციების ისტორია (ანგარიში {account_id}) ---")

    if not records:
        print("ტრანზაქციები არ მოიძებნა.")
        return

    for record in records:
        print(
            f"  [{record['timestamp']}] {record['type']:<9} "
            f"თანხა: {record['amount']:.2f} ლარი | "
            f"ბალანსი შემდეგ: {record['balance_after']:.2f} ლარი"
        )


# ---------- ავტორიზაცია ----------

def authenticate(accounts: dict) -> Optional[str]:
    """ითხოვს ანგარიშის ნომერს და PIN-ს. წარმატებისას აბრუნებს ანგარიშის ID-ს."""
    account_id = input("შეიყვანეთ ანგარიშის ნომერი: ").strip()
    if account_id not in accounts:
        print(" ანგარიში ვერ მოიძებნა!\n")
        return None
    
    pin = input("შეიყვანეთ PIN კოდი: ").strip()
    if pin != accounts[account_id]["pin"]:
        print(" არასწორი PIN კოდი!\n")
        return None
    
    account = accounts[account_id]
    print(
        f" გამარჯობა, {full_name(account)}! "
        f"(ასაკი: {account['age']}, ანგარიში: {account_id})\n"
    )
    return account_id


# ---------- ახალი ანგარიშის რეგისტრაცია ----------

def generate_new_account_id(accounts: dict) -> str:
    """პოულობს უახლოეს თავისუფალ 4-ნიშნა ანგარიშის ნომერს (1001-დან დაწყებული)."""
    candidate = 1001
    while str(candidate) in accounts:
        candidate += 1
    return str(candidate)


def get_non_empty_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(" შეცდომა: ველი არ შეიძლება იყოს ცარიელი.\n")


def get_valid_age(prompt: str) -> int:
    while True:
        try:
            age = int(input(prompt).strip())
            if MIN_AGE <= age <= MAX_AGE:
                return age
            print(f" შეცდომა: ასაკი უნდა იყოს {MIN_AGE}-{MAX_AGE} შორის.\n")
        except ValueError:
            print(" შეცდომა: შეიყვანეთ ვალიდური მთელი რიცხვი.\n")


def get_valid_pin(prompt: str) -> str:
    while True:
        pin = input(prompt).strip()
        if len(pin) == 4 and pin.isdigit():
            return pin
        print(" შეცდომა: PIN უნდა შედგებოდეს ზუსტად 4 ციფრისგან.\n")


def get_valid_initial_deposit(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return 0.0
        try:
            amount = float(raw)
            if amount >= 0:
                return amount
            print(" შეცდომა: თანხა არ შეიძლება იყოს უარყოფითი.\n")
        except ValueError:
            print(" შეცდომა: შეიყვანეთ ვალიდური რიცხვი.\n")


def register_account(accounts: dict) -> str:
    """
    ახალი ანგარიშის შექმნა: ითხოვს პირად მონაცემებს, PIN-ს და (სურვილისამებრ)
    საწყის შენატანს. ინახავს accounts.txt-ში და ლოგავს REGISTER ტრანზაქციას.
    """
    print("\n--- ახალი ანგარიშის გახსნა ---")
    first_name = get_non_empty_text("სახელი: ")
    last_name = get_non_empty_text("გვარი: ")
    age = get_valid_age(f"ასაკი ({MIN_AGE}-{MAX_AGE}): ")
    pin = get_valid_pin("აირჩიეთ 4-ნიშნა PIN კოდი: ")
    initial_deposit = get_valid_initial_deposit(
        "საწყისი შენატანი (Enter გამოტოვებისთვის, ნაგულისხმევი 0): "
    )

    account_id = generate_new_account_id(accounts)
    accounts[account_id] = {
        "pin": pin,
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "balance": initial_deposit,
    }
    save_accounts(accounts)
    log_transaction(account_id, "REGISTER", initial_deposit, initial_deposit)

    print(
        f"\n ანგარიში წარმატებით შეიქმნა! "
        f"თქვენი ანგარიშის ნომერია: {account_id} — გთხოვთ დაიმახსოვროთ."
    )
    print(f" მფლობელი: {full_name(accounts[account_id])} | ბალანსი: {initial_deposit:.2f} ლარი\n")

    return account_id


# ---------- ოპერაციები ----------

def get_valid_amount(prompt: str) -> float:
    """ითხოვს თანხის ოდენობას და ამოწმებს, რომ დადებითი რიცხვი იყოს."""
    while True:
        try:
            amount = float(input(prompt).strip())
            if amount > 0:
                return amount
            print(" შეცდომა: თანხა უნდა იყოს დადებითი რიცხვი!\n")
        except ValueError:
            print(" შეცდომა: გთხოვთ შეიყვანოთ ვალიდური რიცხვი!\n")


def check_balance(accounts: dict, account_id: str) -> None:
    """აჩვენებს მომხმარებლის მონაცემებს და მიმდინარე ბალანსს."""
    account = accounts[account_id]
    print(f"\n მფლობელი: {full_name(account)}")
    print(f" ასაკი: {account['age']}")
    print(f" ბალანსი: {account['balance']:.2f} ლარი")


def deposit(accounts: dict, account_id: str) -> None:
    """თანხის შეტანა ანგარიშზე, ფაილის განახლება და ტრანზაქციის ლოგირება."""
    amount = get_valid_amount("\nშეიყვანეთ შესატანი თანხის ოდენობა: ")
    accounts[account_id]["balance"] += amount
    save_accounts(accounts)
    new_balance = accounts[account_id]["balance"]
    log_transaction(account_id, "DEPOSIT", amount, new_balance)
    print(f" თანხა წარმატებით შემოვიდა. ახალი ბალანსი: {new_balance:.2f} ლარი")


def withdraw(accounts: dict, account_id: str) -> None:
    """თანხის გატანა ანგარიშიდან (საკმარისი ბალანსის შემოწმებით) და ლოგირება."""
    amount = get_valid_amount("\nშეიყვანეთ გასატანი თანხის ოდენობა: ")
    balance = accounts[account_id]["balance"]
    
    if amount > balance:
        print(
            f" ტრანზაქცია უარყოფილია: ანგარიშზე არ არის საკმარისი თანხა! "
            f"(ბალანსი: {balance:.2f} ლარი)"
        )
        log_transaction(account_id, "WITHDRAW_FAILED", amount, balance)
        return
    
    accounts[account_id]["balance"] -= amount
    save_accounts(accounts)
    new_balance = accounts[account_id]["balance"]
    log_transaction(account_id, "WITHDRAW", amount, new_balance)
    print(f" თანხა გაცემულია. დარჩენილი ბალანსი: {new_balance:.2f} ლარი")


def show_accounts(accounts: dict) -> None:
    """აჩვენებს ხელმისაწვდომ ანგარიშებს ფაილიდან წაკითხული მონაცემებით."""
    print("\nსატესტო ანგარიშები:")
    for account_id, data in accounts.items():
        print(
            f"  {account_id} — {full_name(data)} "
            f"(ასაკი: {data['age']}, PIN: {data['pin']})"
        )


def account_operations_menu(accounts: dict, account_id: str) -> None:
    """მთავარი ოპერაციების მენიუ ავტორიზებული/ახლადრეგისტრირებული მომხმარებლისთვის."""
    while True:
        print("\nხელმისაწვდომი ოპერაციები:")
        print("1. ბალანსის შემოწმება")
        print("2. თანხის შეტანა")
        print("3. თანხის გატანა")
        print("4. ტრანზაქციების ისტორია")
        print("0. გასვლა")

        choice = input("აირჩიეთ ოპერაცია (0-4): ").strip()

        if choice == "1":
            check_balance(accounts, account_id)
        elif choice == "2":
            deposit(accounts, account_id)
        elif choice == "3":
            withdraw(accounts, account_id)
        elif choice == "4":
            show_transaction_history(account_id)
        elif choice == "0":
            print("ბანკომატის მოდული დაიხურა.")
            break
        else:
            print(" არასწორი არჩევანი. სცადეთ თავიდან.")


def run_atm() -> None:
    print("=" * 40)
    print("             მოდული: ბანკომატი")
    print("=" * 40)
    
    accounts = load_accounts()
    show_accounts(accounts)

    while True:
        print("\n--- მთავარი მენიუ ---")
        print("1. შესვლა არსებულ ანგარიშზე")
        print("2. ახალი ანგარიშის გახსნა")
        print("0. გასვლა")
        main_choice = input("აირჩიეთ ოპერაცია (0-2): ").strip()

        if main_choice == "1":
            account_id = authenticate(accounts)
            if account_id is None:
                continue
            account_operations_menu(accounts, account_id)
            break
        elif main_choice == "2":
            account_id = register_account(accounts)
            account_operations_menu(accounts, account_id)
            break
        elif main_choice == "0":
            print("ბანკომატის მოდული დაიხურა.")
            break
        else:
            print(" არასწორი არჩევანი. სცადეთ თავიდან.")


if __name__ == "__main__":
    try:
        run_atm()
    except KeyboardInterrupt:
        print("\n\nმოდული შეწყდა მომხმარებლის მიერ.")