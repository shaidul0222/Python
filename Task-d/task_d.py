import csv
from datetime import datetime, date
from typing import List, Dict
import os  

# Finnish weekday names, Monday = 0
WEEKDAYS_FI = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def read_csv_data(file_path: str) -> List[Dict]:
    """
    Reads electricity data from a CSV file with semicolon separators.

    Each row contains:
    - timestamp
    - consumption for three phases (Wh)
    - production for three phases (Wh)

    Returns a list of dictionaries with values as floats and timestamp as datetime.
    """
    records = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            ts = datetime.fromisoformat(row["Time"])
            records.append({
                "timestamp": ts,
                "consumption_1": float(row["Consumption phase 1 Wh"]),
                "consumption_2": float(row["Consumption phase 2 Wh"]),
                "consumption_3": float(row["Consumption phase 3 Wh"]),
                "production_1": float(row["Production phase 1 Wh"]),
                "production_2": float(row["Production phase 2 Wh"]),
                "production_3": float(row["Production phase 3 Wh"]),
            })
    return records

def calculate_daily_totals(records: List[Dict]) -> Dict[date, Dict[str, float]]:
    """
    Groups hourly records by day and calculates total consumption and production per phase in kWh.

    Returns a dictionary keyed by date.
    """
    totals_by_day: Dict[date, Dict[str, float]] = {}

    for record in records:
        day = record["timestamp"].date()
        if day not in totals_by_day:
            totals_by_day[day] = {
                "cons_1": 0.0, "cons_2": 0.0, "cons_3": 0.0,
                "prod_1": 0.0, "prod_2": 0.0, "prod_3": 0.0,
            }

        totals_by_day[day]["cons_1"] += record["consumption_1"] / 1000
        totals_by_day[day]["cons_2"] += record["consumption_2"] / 1000
        totals_by_day[day]["cons_3"] += record["consumption_3"] / 1000
        totals_by_day[day]["prod_1"] += record["production_1"] / 1000
        totals_by_day[day]["prod_2"] += record["production_2"] / 1000
        totals_by_day[day]["prod_3"] += record["production_3"] / 1000

    return totals_by_day

def display_report(totals_by_day: Dict[date, Dict[str, float]]) -> None:
    """
    Prints a clear table of daily electricity consumption and production (kWh) for all phases.
    """
    print("Week 42 Electricity Consumption and Production (kWh, by phase)\n")
    print(f"{'Day':<12} {'Date':<12} {'Consumption [kWh]':<25} {'Production [kWh]':<25}")
    print(f"{'':<12} {'(dd.mm.yyyy)':<12} {'V1':>7} {'V2':>7} {'V3':>7} {'V1':>7} {'V2':>7} {'V3':>7}")
    print("-" * 80)

    for day in sorted(totals_by_day.keys()):
        weekday_name = WEEKDAYS_FI[day.weekday()]
        day_totals = totals_by_day[day]

        cons_1 = f"{day_totals['cons_1']:.2f}".replace(".", ",")
        cons_2 = f"{day_totals['cons_2']:.2f}".replace(".", ",")
        cons_3 = f"{day_totals['cons_3']:.2f}".replace(".", ",")
        prod_1 = f"{day_totals['prod_1']:.2f}".replace(".", ",")
        prod_2 = f"{day_totals['prod_2']:.2f}".replace(".", ",")
        prod_3 = f"{day_totals['prod_3']:.2f}".replace(".", ",")

        print(f"{weekday_name:<12} {day.strftime('%d.%m.%Y'):<12} "
              f"{cons_1:>7} {cons_2:>7} {cons_3:>7} "
              f"{prod_1:>7} {prod_2:>7} {prod_3:>7}")

def main() -> None:
    """
    Main function: reads data, calculates daily totals, and prints the report.
    """
    # Automatically find CSV in the same folder as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "week42.csv")

    records = read_csv_data(file_path)
    daily_totals = calculate_daily_totals(records)
    display_report(daily_totals)

if __name__ == "__main__":
    main()
