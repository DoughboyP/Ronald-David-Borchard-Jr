"""
1984 Chevrolet Impala — Custom Build
Interactive menu to explore and control the car.

Usage
-----
    python3 impala_main.py
"""

from impala_1984 import Impala1984


def print_banner():
    print("\n" + "█" * 50)
    print("█" + " " * 48 + "█")
    print("█    1984 CHEVROLET IMPALA — CUSTOM BUILD       █")
    print("█    🖤 Black on Black | Chrome Forgatos 🖤     █")
    print("█" + " " * 48 + "█")
    print("█" * 50)


def menu(car: Impala1984):
    print("\n  What do you want to do?")
    print("  1. View Full Specs")
    print("  2. Start the Car")
    print("  3. Stop the Car")
    print("  4. Rev the Engine")
    print("  5. Drive")
    print("  6. Honk")
    print("  7. Bump the Sound System")
    print("  8. Set Volume")
    print("  9. Spin the Wheels")
    print("  0. Exit")
    return input("\n  Enter choice: ").strip()


def main():
    print_banner()
    car = Impala1984()
    print(f"\n  Build loaded: {car}\n")

    while True:
        choice = menu(car)

        if choice == "1":
            print(car.specs())
        elif choice == "2":
            print("\n" + car.start())
        elif choice == "3":
            print("\n" + car.stop())
        elif choice == "4":
            print("\n  " + car.engine.rev())
        elif choice == "5":
            print("\n" + car.drive())
        elif choice == "6":
            print("\n  " + car.honk())
        elif choice == "7":
            print("\n" + car.sound_system.bump())
        elif choice == "8":
            try:
                level = int(input("  Enter volume (0-100): "))
                print("\n  " + car.sound_system.set_volume(level))
            except ValueError:
                print("  ❌ Please enter a number between 0 and 100.")
        elif choice == "9":
            print("\n  " + car.wheels.spin())
        elif choice == "0":
            print("\n  🖤 Parking the '84 Impala. Stay legendary. 🖤\n")
            break
        else:
            print("  ❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
