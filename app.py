import datetime
import os

def main():
    name = os.getenv("APP_NAME", "Docker Learner")
    timestamp = datetime.datetime.now().isoformat()
    print(f"Hello, {name}! Current time: {timestamp}")
    print(f"Python version: {os.sys.version}")
    print(f"Running inside a container: True")

if __name__ == "__main__":
    main()
