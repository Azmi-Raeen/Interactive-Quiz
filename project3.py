import tkinter as tk
from tkinter import messagebox
import random
import time

class Question:
    def __init__(self, prompt, choices, answer):
        self.prompt = prompt
        self.choices = choices
        self.answer = answer

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Quiz")
        
        self.categories = {
            "General Knowledge": self.general_knowledge_questions(),
            "Math": self.math_questions(),
            "Physics": self.physics_questions(),
            "Chemistry": self.chemistry_questions()
        }
        
        self.current_questions = []
        self.score = 0
        self.question_index = 0
        self.time_left = 60  # Total time for the quiz in seconds
        
        self.create_widgets()
        self.show_start_screen()

    def general_knowledge_questions(self):
        return [
            Question("What is the capital of France?", ["Paris", "London", "Rome", "Berlin"], "Paris"),
            Question("Which planet is known as the Red Planet?", ["Earth", "Venus", "Mars", "Jupiter"], "Mars"),
            Question("What is the largest ocean on Earth?", ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"], "Pacific Ocean")
        ]

    def math_questions(self):
        return [
            Question("What is 2 + 2?", ["3", "4", "5", "6"], "4"),
            Question("What is 5 * 6?", ["30", "35", "40", "45"], "30"),
            Question("What is the square root of 16?", ["2", "4", "8", "10"], "4")
        ]
    def physics_questions(self):
        return [
             Question("The device which changes from serial data to parallel data is?", ["Demultiplexer", "Multiplexer", "Flip-Flop", "Counter"], "Demultiplexer"),
             Question("What is the speed of light?", ["299,792 km/s", "150,000 km/s", "300,000 km/s", "299,792 m/s"], "299,792 km/s"),
             Question("What is the unit of force?", ["Newton", "Pascal", "Joule", "Watt"], "Newton")
   
        ]
    def chemistry_questions(self):
        return [
            Question("Which among the above plays the most important role in ozone depletion?", ["Hydrogen", "Carbon", "Chlorine", "Flourine"], "Chlorine"),
            Question("What is the fourth state of matter called?", ["Solid", "Liquid", "Gas", "Plasma"], "Plasma"),
            Question("What is the PH of the human blood?", ["Highly Basic", "Slightly Basic", "Slightly Acidic", "Highly Acidic"], "Slightly Basic")
        ]
    def create_widgets(self):
        self.category_label = tk.Label(self.root, text="Select Category")
        self.category_var = tk.StringVar(value="General Knowledge")
        self.category_menu = tk.OptionMenu(self.root, self.category_var, *self.categories.keys())

        self.start_button = tk.Button(self.root, text="Start Quiz", command=self.start_quiz)
        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left} seconds")
        self.question_label = tk.Label(self.root, text="", wraplength=400)

        self.choice_vars = []
        self.choice_buttons = []
        for i in range(4):
            var = tk.StringVar(value="")
            self.choice_vars.append(var)
            btn = tk.Radiobutton(self.root, text="", variable=self.choice_vars[i], value="", command=self.check_answer)
            self.choice_buttons.append(btn)

        self.feedback_label = tk.Label(self.root, text="")
        self.end_button = tk.Button(self.root, text="End Quiz", command=self.end_quiz)

    def show_start_screen(self):
        self.category_label.pack()
        self.category_menu.pack()
        self.start_button.pack()

    def start_quiz(self):
        self.score = 0
        self.question_index = 0
        self.time_left = 60  # Reset timer
        self.current_questions = random.sample(self.categories[self.category_var.get()], len(self.categories[self.category_var.get()]))
        
        self.category_label.pack_forget()
        self.category_menu.pack_forget()
        self.start_button.pack_forget()

        self.timer_label.pack()
        self.question_label.pack()

        for btn in self.choice_buttons:
            btn.pack(anchor=tk.W)
        
        self.feedback_label.pack()
        self.end_button.pack()

        self.update_question()
        self.update_timer()

    def update_question(self):
        if self.question_index < len(self.current_questions):
            question = self.current_questions[self.question_index]
            self.question_label.config(text=question.prompt)
            for i, choice in enumerate(question.choices):
                self.choice_buttons[i].config(text=choice, value=choice)
                self.choice_vars[i].set("")  # Deselect previous selection
        else:
            self.end_quiz()

    def check_answer(self):
        question = self.current_questions[self.question_index]
        selected_choice = None
        for var in self.choice_vars:
            if var.get() == question.answer:
                selected_choice = var.get()
                break

        if selected_choice == question.answer:
            self.feedback_label.config(text="Correct!")
            self.score += 1
        else:
            self.feedback_label.config(text=f"Wrong! The correct answer is {question.answer}")
        
        self.question_index += 1
        self.root.after(1000, self.update_question)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.root.after(1000, self.update_timer)
        else:
            self.end_quiz()

    def end_quiz(self):
        messagebox.showinfo("Quiz Over", f"Your score: {self.score}/{len(self.current_questions)}")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
