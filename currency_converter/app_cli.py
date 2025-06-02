# app_cli.py (Versi Benar)

from converter import convert_currency, get_all_conversions, is_currency_supported

def print_menu(title, options):
    print("=" * 50)
    print(f"🌐 {title}")
    print("=" * 50)
    for key, value in options.items():
        print(f"{key}. {value['desc']}")
    print("=" * 50)

def flexible_mode():
    flexible_options = {
        "1": {"desc": "Convert from one currency to another"},
        "2": {"desc": "Show conversions from one currency to ALL"},
        "0": {"desc": "Back to Main Menu"}
    }

    while True:
        print_menu("Currency Converter - Free Mode", flexible_options)
        choice = input("Select an option (0-2): ")

        if choice == "0":
            break

        try:
            amount = float(input("Enter amount: "))
            from_curr = input("From currency (e.g., USD): ").upper()

            if not is_currency_supported(from_curr):
                print("❌ Unsupported source currency.")
                continue

            if choice == "1":
                to_curr = input("To currency (e.g., IDR): ").upper()
                if not is_currency_supported(to_curr):
                    print("❌ Unsupported target currency.")
                    continue

                result = convert_currency(amount, from_curr, to_curr)
                print(f"\n💱 {amount} {from_curr} = {result:.2f} {to_curr}\n")

            elif choice == "2":
                results = get_all_conversions(amount, from_curr)
                print(f"\n📊 {amount} {from_curr} to other currencies:")
                print("-" * 40)
                for k, v in results.items():
                    print(f"{k: <5}: {v}")
                print()

            else:
                print("❌ Invalid menu option.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except Exception as e:
            print(f"⚠  Error: {e}")


def fixed_mode():
    fixed_menu = {
        "1": {"desc": "USD to EUR", "from": "USD", "to": "EUR"},
        "2": {"desc": "USD to IDR", "from": "USD", "to": "IDR"},
        "3": {"desc": "USD to JPY", "from": "USD", "to": "JPY"},
        "4": {"desc": "IDR to USD", "from": "IDR", "to": "USD"},
        "5": {"desc": "EUR to USD", "from": "EUR", "to": "USD"},
        "6": {"desc": "Show all from IDR", "from": "IDR", "to": None},
        "0": {"desc": "Back to Main Menu"}
    }

    while True:
        print_menu("Currency Converter - Popular Menu", fixed_menu)
        choice = input("Enter your choice: ")

        if choice not in fixed_menu or choice == "0":
            return

        try:
            amount = float(input("Enter amount: "))
            selected = fixed_menu[choice]
            from_curr = selected["from"]
            to_curr = selected["to"]

            if to_curr:
                result = convert_currency(amount, from_curr, to_curr)
                print(f"{amount} {from_curr} = {result:.2f} {to_curr}")
            else:
                results = get_all_conversions(amount, from_curr)
                frequent_currencies = {"USD", "EUR", "JPY", "IDR"}
                print(f"\n📊 {amount} {from_curr} to popular currencies:")
                print("-" * 40)
                for k, v in results.items():
                    if k in frequent_currencies:
                        print(f"{amount} {from_curr} = {v} {k}")
            print()

        except Exception as e:
            print(f"⚠ Error: {e}")

def run():
    main_menu = {
        "1": {"desc": "Flexible Mode (input currencies manually)", "action": flexible_mode},
        "2": {"desc": "Quick Menu Mode (popular currencies)", "action": fixed_mode},
        "0": {"desc": "Exit", "action": lambda: print("👋 Goodbye!")}
    }
    
    while True:
        print_menu("Currency Converter with Menu Mode", main_menu)
        choice = input("Select an option (0-2): ")

        if choice in main_menu:
            if choice == "0":
                main_menu[choice]["action"]()
                break
            else:
                main_menu[choice]["action"]()
        else:
            print("❌ Invalid menu option.")


if __name__ == "__main__":
    run()