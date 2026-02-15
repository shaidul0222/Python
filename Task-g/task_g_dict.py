from datetime import datetime
import os

def convert_reservation(data: list[str]) -> dict | None:
    """Convert a list of strings into a reservation dictionary."""
    if not data or all(not field.strip() for field in data):
        return None  # skip empty lines
    try:
        return {
            "id": int(data[0].strip()),
            "name": data[1].strip(),
            "email": data[2].strip(),
            "phone": data[3].strip(),
            "date": datetime.strptime(data[4].strip(), "%Y-%m-%d").date(),
            "time": datetime.strptime(data[5].strip(), "%H:%M").time(),
            "duration": int(data[6].strip()),
            "price": float(data[7].strip()),
            "confirmed": data[8].strip().lower() == "true",
            "resource": data[9].strip(),
            "created": datetime.fromisoformat(data[10].strip())
        }
    except (IndexError, ValueError) as e:
        print(f"Skipping invalid line: {data} ({e})")
        return None

def fetch_reservations(filename: str) -> list[dict]:
    """Read reservations from a file and return a list of dictionaries."""
    reservations = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            header = next(f, None)  # skip header if present
            for line in f:
                parts = line.strip().split("|")
                r = convert_reservation(parts)
                if r:
                    reservations.append(r)
    except FileNotFoundError:
        print(f"File not found: {filename}")
    return reservations

def print_confirmed(reservations: list[dict]) -> None:
    """Print all confirmed reservations."""
    print("Confirmed Reservations:")
    for r in reservations:
        if r["confirmed"]:
            print(f"- {r['name']}, {r['resource']}, {r['date'].strftime('%d.%m.%Y')}")

def print_long(reservations: list[dict]) -> None:
    """Print all reservations with duration >= 3 hours."""
    print("\nLong Reservations (>= 3 hours):")
    for r in reservations:
        if r["duration"] >= 3:
            print(f"- {r['name']}, {r['duration']}h, {r['resource']}")

def total_revenue(reservations: list[dict]) -> float:
    """Calculate total revenue from all reservations."""
    return sum(r["duration"] * r["price"] for r in reservations)

def main() -> None:
    # Always look for reservations.txt in the same folder as this script
    filename = os.path.join(os.path.dirname(__file__), "reservations.txt")
    
    reservations = fetch_reservations(filename)
    if not reservations:
        print("No valid reservations found.")
        return
    
    print_confirmed(reservations)
    print_long(reservations)
    revenue = total_revenue(reservations)
    print(f"\nTotal Revenue: {revenue:.2f} €")

if __name__ == "__main__":
    main()
