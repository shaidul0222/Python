from datetime import datetime
import os

class Reservation:
    def __init__(self, reservation_id, name, email, phone,
                 date, time, duration, price,
                 confirmed, resource, created):
        self.reservation_id = reservation_id
        self.name = name
        self.email = email
        self.phone = phone
        self.date = date
        self.time = time
        self.duration = duration
        self.price = price
        self.confirmed = confirmed
        self.resource = resource
        self.created = created

    def is_confirmed(self) -> bool:
        return self.confirmed

    def is_long(self) -> bool:
        return self.duration >= 3

    def total_price(self) -> float:
        return self.duration * self.price

    def __str__(self):
        return f"{self.name}, {self.resource}, {self.date.strftime('%d.%m.%Y')}, {self.duration}h, {self.total_price():.2f}€"


def convert_reservation(data: list[str]) -> Reservation | None:
    """Convert a list of strings to a Reservation object."""
    if not data or all(not field.strip() for field in data):
        return None
    try:
        return Reservation(
            reservation_id=int(data[0].strip()),
            name=data[1].strip(),
            email=data[2].strip(),
            phone=data[3].strip(),
            date=datetime.strptime(data[4].strip(), "%Y-%m-%d").date(),
            time=datetime.strptime(data[5].strip(), "%H:%M").time(),
            duration=int(data[6].strip()),
            price=float(data[7].strip()),
            confirmed=data[8].strip().lower() == "true",
            resource=data[9].strip(),
            created=datetime.fromisoformat(data[10].strip())
        )
    except (IndexError, ValueError) as e:
        print(f"Skipping invalid line: {data} ({e})")
        return None


def fetch_reservations(filename: str) -> list[Reservation]:
    """Read reservations from a file and return a list of Reservation objects."""
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


def print_confirmed(reservations: list[Reservation]) -> None:
    print("Confirmed Reservations:")
    for r in reservations:
        if r.is_confirmed():
            print(f"- {r.name}, {r.resource}, {r.date.strftime('%d.%m.%Y')}")


def print_long(reservations: list[Reservation]) -> None:
    print("\nLong Reservations (>= 3 hours):")
    for r in reservations:
        if r.is_long():
            print(f"- {r.name}, {r.duration}h, {r.resource}")


def total_revenue(reservations: list[Reservation]) -> float:
    return sum(r.total_price() for r in reservations)


def main() -> None:
    # Look for reservations.txt in the same folder as this script
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
