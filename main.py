import os
import shutil

base_dir = os.path.dirname(__file__)
unsorted = os.path.join(base_dir, "unsorted")
questions = os.path.join(base_dir, "questions")
solutions = os.path.join(base_dir, "solutions")

os.makedirs(questions, exist_ok=True)
os.makedirs(solutions, exist_ok=True)

for f in os.listdir(unsorted):
    src = os.path.join(unsorted, f)
    if f.endswith("s.gif"):
        shutil.move(src, os.path.join(solutions, f))
    elif f.endswith(".gif"):
        shutil.move(src, os.path.join(questions, f))
