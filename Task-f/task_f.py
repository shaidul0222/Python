# Copyright (c) 2025 Shaidul Islam
# License: MIT

from datetime import datetime, date
from typing import List, Dict, Any

def read_data(filename: str) -> List[Dict[str, Any]]:
    data = []
    with open(filename, encoding="utf-8") as file:
        header = file.readline().strip().split(";")
        header = [h.strip().lower() for h in header]
        key_map = {}
        for h in header:
            if "time" in h:
                key_map[h] = "time"
            elif "consumption" in h:
                key_map[h] = "consumption"
            elif "production" in h:
                key_map[h] = "production"
            elif "temperature" in h:
                key_map[h] = "temperature"
        for line in file:
            values = line.strip().split(";")
            row = dict(zip(header, values))
            row = {key_map[k]: v for k, v in row.items()}
            row["time"] = datetime.fromisoformat(row["time"].replace("+02:00",""))
            row["consumption"] = float(row["consumption"].replace(",", "."))
            row["production"] = float(row["production"].replace(",", "."))
            row["temperature"] = float(row["temperature"].replace(",", "."))
            data.append(row)
    return data

def show_main_menu() -> str:
    print("Choose a report type:")
    print("1) Daily summary for a date range")
    print("2) Monthly summary for one month")
    print("3) Full year 2025 summary")
    print("4) Exit the program")
    return input("Enter your choice: ")

def create_daily_report(data: List[Dict[str, Any]]) -> List[str]:
    start_str = input("Enter start date (dd.mm.yyyy): ")
    end_str = input("Enter end date (dd.mm.yyyy): ")
    start_date = datetime.strptime(start_str, "%d.%m.%Y").date()
    end_date = datetime.strptime(end_str, "%d.%m.%Y").date()
    total_consumption = 0
    total_production = 0
    temp_sum = 0
    count = 0
    for row in data:
        day = row["time"].date()
        if start_date <= day <= end_date:
            total_consumption += row["consumption"]
            total_production += row["production"]
            temp_sum += row["temperature"]
            count += 1
    avg_temp = temp_sum / count if count else 0
    lines = [
        "-----------------------------------------------------",
        f"Report for the period {start_str}–{end_str}",
        f"- Total consumption: {format_value(total_consumption)} kWh",
        f"- Total production: {format_value(total_production)} kWh",
        f"- Average temperature: {format_value(avg_temp)} °C"
    ]
    return lines

def create_monthly_report(data: List[Dict[str, Any]]) -> List[str]:
    month_num = int(input("Enter month number (1–12): "))
    total_consumption = 0
    total_production = 0
    temp_sum = 0
    count = 0
    for row in data:
        if row["time"].month == month_num:
            total_consumption += row["consumption"]
            total_production += row["production"]
            temp_sum += row["temperature"]
            count += 1
    avg_temp = temp_sum / count if count else 0
    month_name = row["time"].strftime("%B")
    lines = [
        "-----------------------------------------------------",
        f"Report for the month: {month_name}",
        f"- Total consumption: {format_value(total_consumption)} kWh",
        f"- Total production: {format_value(total_production)} kWh",
        f"- Average temperature: {format_value(avg_temp)} °C"
    ]
    return lines

def create_yearly_report(data: List[Dict[str, Any]]) -> List[str]:
    total_consumption = sum(row["consumption"] for row in data)
    total_production = sum(row["production"] for row in data)
    avg_temp = sum(row["temperature"] for row in data) / len(data) if data else 0
    lines = [
        "-----------------------------------------------------",
        "Report for the year: 2025",
        f"- Total consumption: {format_value(total_consumption)} kWh",
        f"- Total production: {format_value(total_production)} kWh",
        f"- Average temperature: {format_value(avg_temp)} °C"
    ]
    return lines

def format_value(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")

def print_report_to_console(lines: List[str]) -> None:
    for line in lines:
        print(line)

def write_report_to_file(lines: List[str]) -> None:
    with open("report.txt", "w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")
    print("Report successfully written to report.txt")

def main() -> None:
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, "2025.csv")
    data = read_data(filename)
    while True:
        choice = show_main_menu()
        if choice == "1":
            report = create_daily_report(data)
        elif choice == "2":
            report = create_monthly_report(data)
        elif choice == "3":
            report = create_yearly_report(data)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
            continue
        print_report_to_console(report)
        print("\nWhat would you like to do next?")
        print("1) Write the report to the file report.txt")
        print("2) Create a new report")
        print("3) Exit")
        next_choice = input("Enter your choice: ")
        if next_choice == "1":
            write_report_to_file(report)
        elif next_choice == "2":
            continue
        elif next_choice == "3":
            break
        else:
            print("Invalid choice, returning to main menu.")

if __name__ == "__main__":
    main()
