from tkinter import messagebox

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
