#!/usr/bin/env python3
"""
კონსოლ კალკულატორი
საშუალებას აძლევს მომხმარებელს შეასრულოს ძირითადი არითმეტიკული მოქმედებები:
შეკრება (+), გამოკლება (-), გამრავლება (*), გაყოფა (/)

მოიცავს:
- შეყვანილი რიცხვების ვალიდაციას
- ოპერაციის ვალიდაციას
- ნულზე გაყოფის დამუშავებას
- საშუალებას გავიმეოროთ გამოთვლა ან გავჩერდეთ
"""


def get_number(prompt: str) -> float:
    """
    ითხოვს მომხმარებლისგან რიცხვს, სანამ არასწორ მნიშვნელობას შეიყვანს.
    აბრუნებს ვალიდურ float რიცხვს.
    """
    while True:
        raw_value = input(prompt).strip()
        try:
            return float(raw_value)
        except ValueError:
            print(f" შეცდომა: '{raw_value}' არ არის სწორი რიცხვი. სცადეთ თავიდან.\n")


def get_operation() -> str:
    """
    ითხოვს მომხმარებლისგან ოპერაციას, სანამ არასწორ მნიშვნელობას შეიყვანს.
    აბრუნებს ვალიდურ ოპერატორს: +, -, *, /
    """
    valid_operations = {"+", "-", "*", "/"}
    while True:
        operation = input("აირჩიეთ მოქმედება (+, -, *, /): ").strip()
        if operation in valid_operations:
            return operation
        print(f" შეცდომა: '{operation}' არ არის ვალიდური მოქმედება. "
              f"გამოიყენეთ +, -, * ან /.\n")


def calculate(a: float, b: float, operation: str) -> float:
    """
    ასრულებს არითმეტიკულ მოქმედებას ორ რიცხვზე.
    გაყოფისას ნულზე იწვევს ZeroDivisionError-ს.
    """
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        if b == 0:
            raise ZeroDivisionError("ნულზე გაყოფა დაუშვებელია.")
        return a / b
    else:
        # ეს ტოტი პრაქტიკულად ვერასდროს ამოქმედდება,
        # რადგან get_operation() უკვე ვალიდაციას ატარებს
        raise ValueError(f"უცნობი მოქმედება: {operation}")


def format_result(a: float, operation: str, b: float, result: float) -> str:
    """აფორმატებს შედეგს წასაკითხად."""
    def fmt(n: float) -> str:
        # თუ რიცხვი მთელია, გამოვაჩინოთ მთელი რიცხვის სახით,
        # წინააღმდეგ შემთხვევაში დავამრგვალოთ 2 ათწილადამდე
        if n == int(n):
            return str(int(n))
        return f"{round(n, 2)}"
 
    return f"{fmt(a)} {operation} {fmt(b)} = {fmt(result)}"


def main():
    print("=" * 40)
    print("        კონსოლ კალკულატორი")
    print("=" * 40)
    print("მხარდაჭერილი მოქმედებები: +, -, *, /")
    print("გასასვლელად ნებისმიერ დროს დააჭირეთ Ctrl+C\n")

    while True:
        try:
            first_number = get_number("შეიყვანეთ პირველი რიცხვი: ")
            operation = get_operation()
            second_number = get_number("შეიყვანეთ მეორე რიცხვი: ")

            result = calculate(first_number, second_number, operation)
            print("\n შედეგი:")
            print(f"   {format_result(first_number, operation, second_number, result)}\n")

        except ZeroDivisionError as e:
            print(f"\n შეცდომა: {e}\n")
        except Exception as e:
            print(f"\n მოულოდნელი შეცდომა: {e}\n")

        again = input("გსურთ კიდევ ერთი გამოთვლა? (დიახ/არა): ").strip().lower()
        if again not in ("დიახ", "კი", "yes", "y"):
            print("\nნახვამდის! 👋")
            break
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nპროგრამა შეწყდა მომხმარებლის მიერ. ნახვამდის! 👋")