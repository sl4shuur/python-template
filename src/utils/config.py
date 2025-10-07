from pathlib import Path

# Base of the project
BASE_DIR = Path(__file__).parent.parent.parent

# # .env file loading
# dotenv_path = BASE_DIR / ".env"
# if not dotenv_path.exists():
#     raise FileNotFoundError(f"Environment file not found: {dotenv_path}")

# dotenv.load_dotenv(dotenv_path)


if __name__ == "__main__":
    print(f"Base directory: {BASE_DIR}")