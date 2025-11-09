print("AI GYM — starting (menu only)")

def main():
    """Show menu and import workout modules only when the user requests them.

    This avoids import-time failures when heavy dependencies (OpenCV,
    MediaPipe, pyttsx3, etc.) are not installed. If the user selects an
    exercise whose dependencies are missing, a helpful error is shown.
    """

    print("\n=== AI GYM TRAINER ===\n")
    print("Choose Exercise:")
    print("1. Push-up")
    print("2. Squat")
    print("3. Plank")
    print("4. Lunge")
    print("q. Quit\n")

    choice = input("Enter number (or 'q' to quit): ")

    if choice == "q":
        print("Goodbye!")
        return

    try:
        if choice == "1":
            from workouts.pushup import main as run_pushup
            run_pushup()

        elif choice == "2":
            from workouts.squat import run_squat
            run_squat()

        elif choice == "3":
            from workouts.plank import run_plank
            run_plank()

        elif choice == "4":
            from workouts.lunge import run_lunge
            run_lunge()

        else:
            print("Invalid choice!")

    except ModuleNotFoundError as e:
        print("Failed to start exercise due to missing dependency:", e.name)
        print("Install required packages (e.g. 'pip install mediapipe opencv-python numpy pyttsx3')")
    except Exception as e:
        print("An error occurred while launching the exercise:", str(e))


if __name__ == "__main__":
    main()
