import tkinter as tk
from tkinter import messagebox
import random

class QuestionLoader:

    def __init__(self, filename='questions.txt'):
        self.filename = filename
        
    def load_questions(self):
        try:
            with open(self.filename, 'r') as file:
                file_content = file.read().strip()
                if not file_content:
                    print("System: File is empty")
                    return []

                question_blocks = file_content.split("--- Question")
                question_list = []

                for question_block in question_blocks:
                    if question_block.strip() == "":
                        continue

                lines = question_block.strip().split("\n")
                question_data = {}

                for line in lines:
                    if line.startswith('Q'):
                        question_data['question'] = line.split(':', 1)[1].strip()
                    elif line.startswith('A)'):
                        question_data['option_a'] = line[3:].strip()
                    elif line.startswith('B)'):
                        question_data['option_b'] = line[3:].strip()
                    elif line.startswith('C)'):
                        question_data['option_c'] = line[3:].strip()
                    elif line.startswith('D)'):
                        question_data['option_d'] = line[3:].strip()
                    elif line.startswith('ANSWER:'):
                        question_data['correct_answer'] = line.split(':')[1].strip().lower()

                if question_data:
                    question_list.append(question_data)

        return question_list

    except FileNotFoundError:
        messagebox.showerror("Error", "Quiz File not found.")
        return []

class :
    def __init__(self, window, questions_list):
        self.window = window
        self.window.title("Quiz Game")
        self.window.geometry("780x600")
        self.window.configure(bg="#2d2d2d")

        self.questions = questions_list
        random.shuffle(self.questions)

        self.score = 0
        self.current_question_index = 0
        self.time_left = 180  # 3 minutes

        # UI Components
        self.create_ui()

        self.load_next_question()
        self.update_timer()

    def create_ui(self):
        self.top_frame = tk.Frame(self.window, bg="#2d2d2d")
        self.top_frame.pack(fill="x", pady=(10, 0))

        self.score_label = tk.Label(self.top_frame, text=f"Score: {self.score}",
                                    font=("Arial", 12), bg="#2d2d2d", fg="white")
        self.score_label.pack(side="left", padx=20)

        self.timer_label = tk.Label(self.top_frame, text="Time Left: 03:00",
                                    font=("Arial", 12), bg="#2d2d2d", fg="white")
        self.timer_label.pack(side="right", padx=20)

        self.question_label = tk.Label(self.window, text="", font=("Arial", 16),
                                       wraplength=700, justify="left",
                                       bg="#2d2d2d", fg="#f1f1f1")
        self.question_label.pack(pady=20)

        self.options_frame = tk.Frame(self.window, bg="#2d2d2d")
        self.options_frame.pack()

        self.option_buttons = []
        for option_letter in ['a', 'b', 'c', 'd']:
            option_button = tk.Button(
                self.options_frame,
                text="",
                width=50,
                font=("Arial", 12),
                bg="#3c3f41",
                fg="#f1f1f1",
                activebackground="#5c5f66",
                relief=tk.FLAT
            )

            option_button.config(command=lambda selected_option=option_letter: self.check_answer(selected_option))

            # Add hover animation
            option_button.bind("<Enter>", lambda e, button=option_button: button.config(bg="#5c5f66", fg="#ffffff"))
            option_button.bind("<Leave>", lambda e, button=option_button: button.config(bg="#3c3f41", fg="#f1f1f1"))

            option_button.pack(pady=5)
            self.option_buttons.append(option_button)

        self.feedback_label = tk.Label(self.window, text="", font=("Arial", 14),
                                       bg="#2d2d2d", fg="#f1f1f1")
        self.feedback_label.pack(pady=10)

        self.next_button = tk.Button(
            self.window,
            text="Next Question",
            font=("Arial", 12),
            command=self.load_next_question,
            bg="#4b4f53",
            fg="#f1f1f1",
            activebackground="#6e7178",
            relief=tk.FLAT
        )
        self.next_button.pack(pady=10)
        self.next_button.config(state=tk.DISABLED)

    def load_next_question(self):
        if self.current_question_index < len(self.questions):
            current_question = self.questions[self.current_question_index]
            self.question_label.config(text=f"Q{self.current_question_index + 1}: {current_question['question']}")
            self.option_buttons[0].config(text=f"a) {current_question['option_a']}")
            self.option_buttons[1].config(text=f"b) {current_question['option_b']}")
            self.option_buttons[2].config(text=f"c) {current_question['option_c']}")
            self.option_buttons[3].config(text=f"d) {current_question['option_d']}")
            self.feedback_label.config(text="")
            for option_button in self.option_buttons:
                option_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.DISABLED)

            self.current_question_index += 1
        else:
            self.display_final_score()

    def check_answer(self, selected_option):
        current_question = self.questions[self.current_question_index - 1]
        correct_option_letter = current_question['correct_answer']
        correct_option_text = current_question.get(f'option_{correct_option_letter}', 'Unknown')

        if selected_option == correct_option_letter:
            self.feedback_label.config(text="Correct!", fg="lime green")
            self.score += 1
        else:
            self.feedback_label.config(
                text=f"Wrong! Correct answer was: {correct_option_letter}) {correct_option_text}",
                fg="red"
            )

        self.score_label.config(text=f"Score: {self.score}")
        for option_button in self.option_buttons:
            option_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def display_final_score(self):
        messagebox.showinfo(
            "Quiz Completed",
            f"Your final score is {self.score}/{len(self.questions)}.\nThanks for playing!"
        )
        self.window.destroy()

    def update_timer(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")

        if self.time_left > 0:
            self.time_left -= 1
            self.window.after(1000, self.update_timer)
        else:
            self.display_final_score()

def main():
    question_list = load_questions()
    if question_list:
        root = tk.Tk()
        quiz_app = QuizApp(root, question_list)
        root.mainloop()

if __name__ == "__main__":
    main()