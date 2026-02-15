# Copyright (c) 2026 Shaidul Islam
# License: MIT

import csv
import os
from datetime import datetime, date
from collections import defaultdict
from typing import List, Dict


WeekSummary = Dict[date, Dict[str, List[float]]]


def read_data(filename: str) -> List[Dict[str, str]]:
    """Reads CSV file and returns rows as dictionaries."""
    with open(filename, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        return list(reader)


def wh_to_kwh(value: float) -> float:
    """Converts Wh to kWh."""
    return value / 1000.0


def get_weekday(day: date) -> str:
    """Returns weekday name in English."""
    weekdays = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]
    return weekdays[day.weekday()]


def calculate_daily_summary(rows: List[Dict[str, str]]) -> WeekSummary:
    """Calculates daily totals for consumption and production per phase."""
    summary: WeekSummary = defaultdict(
        lambda: {
            "consumption": [0.0, 0.0, 0.0],
            "production": [0.0, 0.0, 0.0]
        }
    )

    for row in rows:
        dt = datetime.fromisoformat(row["Time"])
        day = dt.date()

        summary[day]["consumption"][0] += wh_to_kwh(float(row["Consumption phase 1 Wh"]))
        summary[day]["consumption"][1] += wh_to_kwh(float(row["Consumption phase 2 Wh"]))
        summary[day]["consumption"][2] += wh_to_kwh(float(row["Consumption phase 3 Wh"]))

        summary[day]["production"][0] += wh_to_kwh(float(row["Production phase 1 Wh"]))
        summary[day]["production"][1] += wh_to_kwh(float(row["Production phase 2 Wh"]))
        summary[day]["production"][2] += wh_to_kwh(float(row["Production phase 3 Wh"]))

    return dict(summary)


def format_number(value: float) -> str:
    """Formats number with two decimals and comma as decimal separator."""
    return f"{value:.2f}".replace(".", ",")


def format_date(day: date) -> str:
    """Formats date as dd.mm.yyyy."""
    return f"{day.day:02d}.{day.month:02d}.{day.year}"


def format_week_section(week_number: int, summary: WeekSummary) -> str:
    """Formats one week's report section as a string."""
    lines = []

    lines.append(f"Week {week_number} electricity consumption and production (kWh, by phase)")
    lines.append("Day      Date           Consumption [kWh]            Production [kWh]")
    lines.append("                        v1      v2      v3           v1      v2      v3")
    lines.append("-" * 75)

    for day in sorted(summary.keys()):
        weekday = get_weekday(day)
        date_str = format_date(day)

        cons = [format_number(v) for v in summary[day]["consumption"]]
        prod = [format_number(v) for v in summary[day]["production"]]

        line = (
            f"{weekday:<9} {date_str:<13}"
            f"{cons[0]:>8} {cons[1]:>8} {cons[2]:>8}      "
            f"{prod[0]:>8} {prod[1]:>8} {prod[2]:>8}"
        )

        lines.append(line)

    lines.append("")  # blank line between weeks
    return "\n".join(lines)


def write_report(sections: List[str]) -> None:
    """Writes all weekly sections to summary.txt."""
    with open("summary.txt", "w", encoding="utf-8") as file:
        for section in sections:
            file.write(section + "\n")


def main() -> None:
    """Main function: reads CSVs, computes summaries, writes report."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    files = {
        41: os.path.join(script_dir, "week41.csv"),
        42: os.path.join(script_dir, "week42.csv"),
        43: os.path.join(script_dir, "week43.csv")
    }

    sections = []

    for week_number, filepath in files.items():
        rows = read_data(filepath)
        summary = calculate_daily_summary(rows)
        sections.append(format_week_section(week_number, summary))

    write_report(sections)
    print("Report successfully written to summary.txt")


if __name__ == "__main__":
    main()
