import sqlite3
from datetime import datetime, timezone

DB_NAME = "readings.db"


def setup_database():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL NOT NULL,
                location TEXT NOT NULL,
                recorded_at TEXT NOT NULL
            )
        """)


def record_temperature(temperature, location):
    timestamp = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """
            INSERT INTO readings
            (temperature, location, recorded_at)
            VALUES (?, ?, ?)
            """,
            (temperature, location, timestamp)
        )

    print(f"Saved {temperature}°C for {location}")

    if temperature > 30:
        print("WARNING: Temperature is above 30°C!")


def show_readings():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("""
            SELECT id, temperature, location, recorded_at
            FROM readings
            ORDER BY id DESC
        """).fetchall()

    if not rows:
        print("No readings recorded yet.")
        return

    print("\n--- Temperature History ---")

    for row in rows:
        print(
            f"ID: {row[0]} | "
            f"Temperature: {row[1]}°C | "
            f"Location: {row[2]} | "
            f"Time: {row[3]}"
        )


def main():
    setup_database()

    print("\n=== CLOUD DATA LOGGER ===")
    print("1. Record temperature")
    print("2. View temperature history")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        try:
            temperature = float(input("Temperature in °C: "))
            location = input("Location: ").strip()

            if not location:
                print("Location cannot be empty.")
                return

            record_temperature(temperature, location)

        except ValueError:
            print("Please enter a valid number.")

    elif choice == "2":
        show_readings()

    elif choice == "3":
        print("Goodbye!")

    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
