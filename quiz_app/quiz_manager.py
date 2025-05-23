import sys
import time
from datetime import datetime

class QuizManager:
    def __init__(self, filename='questions.txt'):
        self.filename = filename
        self.auto_reindex_questions()

    def auto_reindex_questions(self):
        try:
            with open(self.filename, 'r') as file:
                content = file.read().strip()

            if not content:
                return

            blocks = content.split('--- Question')
            updated_blocks = []
            question_number = 1

            for block in blocks:
                if block.strip() == "":
                    continue
                lines = block.strip().split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('Q'):
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            lines[i] = f"Q{question_number}: {parts[1].strip()}"
                reindexed_block = f"--- Question {question_number} ---\n" + '\n'.join(lines)
                updated_blocks.append(reindexed_block)
                question_number += 1

            with open(self.filename, 'w') as file:
                file.write('\n\n'.join(updated_blocks) + '\n')
        except FileNotFoundError:
            return

    def loading_bar(self, duration):
        for i in range(0, 101, 2):
            time.sleep(duration / 50)
            if i < 30:
                color = "\033[31m"
            elif i < 60:
                color = "\033[33m"
            elif i < 90:
                color = "\033[34m"
            else:
                color = "\033[32m"
            bar = '=' * (i // 2)
            spaces = ' ' * (50 - i // 2)
            sys.stdout.write(f"\r{color}[{bar}{spaces}] {i}%")
            sys.stdout.flush()
        print()

    def main_menu(self):
        print("\n\033[32mWelcome to the Main Menu!\033[0m")
        print("1. \033[34m[📝] Create Questions\033[0m")
        print("2. \033[35m[💻] Developer Info\033[0m")
        print("3. \033[33m[📚] See Questions\033[0m")
        print("4. \033[36m[⚙️ ] Manage Questions\033[0m")
        print("5. \033[91m[🚪] Exit Like a Legend\033[0m")

        choice = input("\033[97mEnter your choice 1-5: \033[0m")
        if choice == '1':
            self.create_quiz()
        elif choice == '2':
            self.developer_info()
        elif choice == '3':
            self.see_questions()
        elif choice == '4':
            self.manage_questions()
        elif choice == '5':
            print("\033[97mGoodbye! 😊\033[0m")
            exit()
        else:
            print("\033[97mInvalid choice. Please try again.\033[0m")
            self.main_menu()

    def developer_info(self):
        print("\nDeveloper: \033[96mGerald Tan Rogado\033[0m")
        print("Email: \033[95mgeraldtanrogado@gmail.com\033[0m")
        print("Github Profile: \033[33mhttps://github.com/Yozora-apricity\033[0m")

        while True:
            choice = input("\nWould you like to go back to the main menu? (y/n): ").lower()
            if choice == 'y':
                self.main_menu()
                break
            elif choice == 'n':
                print("\033[97mGoodbye! 😊\033[0m")
                exit()
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def get_next_question_number(self):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                return len([line for line in lines if line.startswith('Q')]) + 1
        except FileNotFoundError:
            return 1

    def create_quiz(self):
        print("\n--- Create Quiz Questions ---")
        with open(self.filename, 'a') as file:
            while True:
                question = input("Enter question: ")
                a = input("Enter option a: ")
                b = input("Enter option b: ")
                c = input("Enter option c: ")
                d = input("Enter option d: ")

                correct = input("Enter the correct answer (a-d): ").lower()
                while correct not in {'a', 'b', 'c', 'd'}:
                    print("Invalid answer! Please enter a, b, c, or d.")
                    correct = input("Enter the correct answer (a-d): ").lower()

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                question_number = self.get_next_question_number()

                print("\nSaving your question...")
                self.loading_bar(3)

                file.write(f'\n--- Question {question_number} ---\n')
                file.write(f'Q{question_number}: {question}\n')
                file.write(f"A) {a}\nB) {b}\nC) {c}\nD) {d}\n")
                file.write(f"ANSWER: {correct}\n")
                file.write(f"--- Added on {timestamp} ---\n\n")

                if input("\nAdd another question? (y/n): ").lower() != 'y':
                    print("\nQuestions saved to questions.txt")
                    break
        self.main_menu()

    def see_questions(self):
        print("\n--- View Questions ---")
        try:
            with open(self.filename, 'r') as file:
                content = file.read()
                if content.strip():
                    print(content)
                else:
                    print("No questions available.")
        except FileNotFoundError:
            print("No questions have been added yet.")

        while True:
            choice = input("\nWould you like to go back to the main menu? (y/n): ").lower()
            if choice == 'y':
                self.main_menu()
                break
            elif choice == 'n':
                print("\033[97mGoodbye! 😊\033[0m")
                exit()
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def manage_questions(self):
        print("\n--- Manage Questions ---")
        try:
            with open(self.filename, 'r') as file:
                content = file.readlines()
            if not content:
                print("No questions available.")
                return

            question_num = 1
            for line in content:
                if line.startswith('Q'):
                    print(f"{question_num}. {line.strip()}")
                    question_num += 1

            print("\nOptions:")
            print("1. \033[31m[🗑️ ] Delete all questions\033[0m")
            print("2. \033[38;5;214m[❌] Delete a specific question\033[0m")
            print("3.[🔙] Go back to the main menu")

            choice = input("\033[97mEnter your choice (1-3): \033[0m")
            if choice == '1':
                self.delete_all_questions()
            elif choice == '2':
                self.delete_specific_question(content)
            elif choice == '3':
                self.main_menu()
            else:
                print("Invalid choice. Please try again.")
                self.manage_questions()
        except FileNotFoundError:
            print("No questions have been added yet.")

    def delete_all_questions(self):
        confirm = input("Are you sure you want to delete all questions? (y/n): ").lower()
        if confirm == 'y':
            print("Deleting all questions...")
            self.loading_bar(5)
            with open(self.filename, 'w') as file:
                file.truncate(0)
            print("All questions have been deleted.")
        else:
            print("No questions were deleted.")
        self.main_menu()

    def delete_specific_question(self, content):
        try:
            question_num = int(input("Enter the question number to delete: "))
            question_start = f'Q{question_num}:'
            question_lines = []
            question_block = False

            for idx, line in enumerate(content):
                if line.startswith(question_start):
                    question_block = True
                if question_block:
                    question_lines.append(line)
                if question_block and line.startswith("---"):
                    question_block = False
                    break

            if not question_lines:
                print(f'Question {question_num} does not exist.')
                return

            filtered_content = [line for line in content if line not in question_lines]

            print(f"Deleting question {question_num}...")
            self.loading_bar(3)
            with open(self.filename, 'w') as file:
                file.writelines(filtered_content)

            print(f"Question {question_num} has been deleted.")
            self.manage_questions()
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            self.manage_questions()


if __name__ == '__main__':
    quiz_app = QuizManager()
    quiz_app.main_menu()
