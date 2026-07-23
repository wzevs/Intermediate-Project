#!/usr/bin/env python3
"""
სტუდენტების მართვის სისტემა
OOP: ინკაფსულაცია, მემკვიდრეობა, პოლიმორფიზმი + შეყვანის ვალიდაცია.
დამატებულია: Faker-ით შემთხვევითი სტუდენტების გენერირება.
"""
import random
from abc import ABC, abstractmethod

try:
    from faker import Faker
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False


class Person(ABC):
    """ბაზური კლასი — მემკვიდრეობისთვის."""

    def __init__(self, name: str) -> None:
        # ვწერთ self.name-ს (და არა self._name-ს), რომ კონსტრუქციისასაც
        # ვალიდაცია გაეშვას name.setter-ის მეშვეობით — ინკაფსულაცია
        # მთლიანად ობიექტის სასიცოცხლო ციკლში უნდა მუშაობდეს, არა
        # მხოლოდ მოგვიანებით მინიჭებისას.
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("სახელი არ შეიძლება იყოს ცარიელი.")
        self._name = value

    @abstractmethod
    def display_info(self) -> str:
        """პოლიმორფიზმი — შვილი კლასი განსაზღვრავს ჩვენების ფორმატს."""
        pass


class Student(Person):
    """სტუდენტი: სახელი, სიის ნომერი, შეფასება."""

    VALID_GRADES = set("ABCDF")

    def __init__(self, name: str, roll_number: int, grade: str) -> None:
        super().__init__(name)
        self.roll_number = roll_number
        self.grade = grade

    @property
    def roll_number(self) -> int:
        return self._roll_number

    @roll_number.setter
    def roll_number(self, value: int) -> None:
        # isinstance(value, bool) გამორიცხულია ცალკე, რადგან Python-ში
        # bool არის int-ის subclass და True/False ტექნიკურად გაივლიდა
        # isinstance(value, int) შემოწმებას.
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError("სიის ნომერი უნდა იყოს დადებითი მთელი რიცხვი.")
        self._roll_number = value

    @property
    def grade(self) -> str:
        return self._grade

    @grade.setter
    def grade(self, value: str) -> None:
        value = value.strip().upper()
        if len(value) != 1 or value not in self.VALID_GRADES:
            raise ValueError("შეფასება უნდა იყოს ერთი ასო: A, B, C, D ან F.")
        self._grade = value

    def display_info(self) -> str:
        return (
            f"სახელი: {self.name} | "
            f"სიის ნომერი: {self.roll_number} | "
            f"შეფასება: {self.grade}"
        )

    def __str__(self) -> str:
        return self.display_info()


class StudentManager:
    """სტუდენტების სიის მართვა."""

    def __init__(self) -> None:
        self._students: list[Student] = []

    def add_student(self, student: Student) -> None:
        if self.find_by_roll(student.roll_number) is not None:
            raise ValueError(
                f"სტუდენტი სიის ნომრით {student.roll_number} უკვე არსებობს."
            )
        self._students.append(student)

    def get_all(self) -> list[Student]:
        return list(self._students)

    def find_by_roll(self, roll_number: int) -> Student | None:
        for student in self._students:
            if student.roll_number == roll_number:
                return student
        return None

    def update_grade(self, roll_number: int, new_grade: str) -> None:
        student = self.find_by_roll(roll_number)
        if student is None:
            raise ValueError(f"სტუდენტი ნომრით {roll_number} ვერ მოიძებნა.")
        student.grade = new_grade

    def next_free_roll(self) -> int:
        """
        პოულობს უახლოეს თავისუფალ სიის ნომერს (1-დან დაწყებული),
        რომელიც ჯერ არავის უჭირავს — გამოსადეგია ავტომატური გენერაციისთვის.
        """
        existing_rolls = {student.roll_number for student in self._students}
        candidate = 1
        while candidate in existing_rolls:
            candidate += 1
        return candidate


def get_non_empty_name(prompt: str) -> str:
    while True:
        name = input(prompt).strip()
        if name:
            return name
        print(" შეცდომა: სახელი არ შეიძლება იყოს ცარიელი.\n")


def get_positive_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if value > 0:
                return value
            print(" შეცდომა: შეიყვანეთ დადებითი მთელი რიცხვი.\n")
        except ValueError:
            print(" შეცდომა: შეიყვანეთ ვალიდური მთელი რიცხვი.\n")


def get_valid_grade(prompt: str) -> str:
    while True:
        grade = input(prompt).strip().upper()
        if len(grade) == 1 and grade in Student.VALID_GRADES:
            return grade
        print(" შეცდომა: შეფასება უნდა იყოს A, B, C, D ან F.\n")


def add_student_menu(manager: StudentManager) -> None:
    print("\n--- ახალი სტუდენტის დამატება ---")
    name = get_non_empty_name("სახელი: ")
    roll = get_positive_int("სიის ნომერი: ")
    grade = get_valid_grade("შეფასება (A/B/C/D/F): ")
    try:
        student = Student(name, roll, grade)
        manager.add_student(student)
        print(f" სტუდენტი დაემატა: {student}")
    except ValueError as error:
        print(f" {error}")


def view_all_students(manager: StudentManager) -> None:
    print("\n--- ყველა სტუდენტი ---")
    students = manager.get_all()
    if not students:
        print("სია ცარიელია.")
        return
    for index, student in enumerate(students, start=1):
        # პოლიმორფიზმი: display_info() Person-ის აბსტრაქტული მეთოდია
        print(f"{index}. {student.display_info()}")


def search_student(manager: StudentManager) -> None:
    print("\n--- სტუდენტის ძებნა ---")
    roll = get_positive_int("სიის ნომერი: ")
    student = manager.find_by_roll(roll)
    if student is None:
        print(f" სტუდენტი ნომრით {roll} ვერ მოიძებნა.")
    else:
        print(f" ნაპოვნია: {student.display_info()}")


def update_grade_menu(manager: StudentManager) -> None:
    print("\n--- შეფასების განახლება ---")
    roll = get_positive_int("სტუდენტის სიის ნომერი: ")
    new_grade = get_valid_grade("ახალი შეფასება (A/B/C/D/F): ")
    try:
        manager.update_grade(roll, new_grade)
        student = manager.find_by_roll(roll)
        print(f" შეფასება განახლდა: {student.display_info()}")
    except ValueError as error:
        print(f" {error}")


def generate_random_students(manager: StudentManager) -> None:
    """
    Faker-ის დახმარებით ქმნის მითითებულ რაოდენობის შემთხვევით სტუდენტს
    (ქართული სახელები, ka_GE ლოკალით) და ამატებს StudentManager-ს.
    """
    print("\n--- შემთხვევითი სტუდენტების გენერირება (Faker) ---")

    if not FAKER_AVAILABLE:
        print(
            " ბიბლიოთეკა 'faker' დაინსტალირებული არ არის.\n"
            "   დააინსტალირეთ ტერმინალში: pip install faker\n"
        )
        return

    count = get_positive_int("რამდენი სტუდენტის გენერირება გსურთ?: ")

    fake = Faker("ka_GE")
    created = 0

    for _ in range(count):
        name = fake.name()
        roll = manager.next_free_roll()
        grade = random.choice(sorted(Student.VALID_GRADES))
        try:
            student = Student(name, roll, grade)
            manager.add_student(student)
            created += 1
            print(f" დაგენერირდა: {student}")
        except ValueError as error:
            # პრაქტიკაში იშვიათია (next_free_roll ყოველთვის თავისუფალს პოულობს),
            # მაგრამ ვალიდაციის შეცდომა მაინც უსაფრთხოდ ვამუშავოთ
            print(f" {error}")

    print(f"\n სულ დაემატა {created} შემთხვევითი სტუდენტი.")


def run() -> None:
    manager = StudentManager()
    while True:
        print("\n" + "=" * 40)
        print("   სტუდენტების მართვის სისტემა")
        print("=" * 40)
        print("1. ახალი სტუდენტის დამატება")
        print("2. ყველა სტუდენტის ნახვა")
        print("3. სტუდენტის ძებნა ნომრის მიხედვით")
        print("4. შეფასების განახლება")
        print("5. შემთხვევითი სტუდენტების გენერირება (Faker)")
        print("0. გასვლა")
        choice = input("აირჩიეთ ოპერაცია (0-5): ").strip()
        if choice == "1":
            add_student_menu(manager)
        elif choice == "2":
            view_all_students(manager)
        elif choice == "3":
            search_student(manager)
        elif choice == "4":
            update_grade_menu(manager)
        elif choice == "5":
            generate_random_students(manager)
        elif choice == "0":
            print("პროგრამა დასრულდა.")
            break
        else:
            print(" არასწორი არჩევანი. სცადეთ თავიდან.")


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n\nპროგრამა შეწყდა მომხმარებლის მიერ.")