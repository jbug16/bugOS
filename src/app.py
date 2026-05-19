class PhoneApp:
    def __init__(self):
        self.running = True

        self.menu_items = [
            "Contacts",
            "Messages",
            "Settings",
            "Call"
        ]

        self.selected = 0

    def draw(self):
        print("\n" * 50)

        print("bugOS v0.1")
        print("------------------")

        for i, item in enumerate(self.menu_items):
            if i == self.selected:
                print(f"> {item}")
            else:
                print(f"  {item}")

        print("\nW/S = Move")
        print("Q = Quit")

    def run(self):
        while self.running:
            self.draw()

            choice = input("\nInput: ").lower()

            if choice == "w":
                self.selected -= 1

                if self.selected < 0:
                    self.selected = len(self.menu_items) - 1

            elif choice == "s":
                self.selected += 1

                if self.selected >= len(self.menu_items):
                    self.selected = 0

            elif choice == "q":
                self.running = False