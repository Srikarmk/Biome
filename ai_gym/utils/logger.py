import csv
import datetime

def log_result(exercise, result):
    with open("workout_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now(), exercise, result])
