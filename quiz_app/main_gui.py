import tkinter as tk
from quiz_loader import QuestionLoader
from quiz_interface import QuizInterface

def main():
    loader = QuestionLoader()
    questions = loader.load_questions()
    if questions:
        root = tk.Tk()
        quiz_ui = QuizInterface(root, questions)
        root.mainloop()

if __name__ == "__main__":
    main()