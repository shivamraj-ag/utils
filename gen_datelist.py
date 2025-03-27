import argparse
import datetime
import os

def parse_holidays(file_path):
    holidays = set()
    file_path = os.path.expanduser(file_path)
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    day = parts[0].strip()
                    month = parts[2].strip()
                    year = parts[3].strip()
                    if day.isdigit() and month.isdigit() and year.isdigit():
                        holidays.add(f"{year}{month.zfill(2)}{day.zfill(2)}")
    except FileNotFoundError:
        print(f"Warning: Holiday file not found at {file_path}. Proceeding without holidays.")
    return holidays

def generate_tradable_dates(start_date, end_date, skip_days, holidays, output_file):
    current_date = datetime.datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
    
    with open(output_file, 'w') as f:
        while current_date <= end_date:
            date_str = current_date.strftime("%Y%m%d")
            weekday = current_date.weekday()  # Monday=0, Sunday=6
            
            if weekday not in skip_days and date_str not in holidays:
                f.write(date_str + "\n")
            
            current_date += datetime.timedelta(days=1)

def main():
    parser = argparse.ArgumentParser(description="Generate tradable date list.")
    parser.add_argument("--start_date", required=True, help="Start date in YYYYMMDD format")
    parser.add_argument("--end_date", required=True, help="End date in YYYYMMDD format")
    parser.add_argument("--skip_days", type=int, nargs='*', default=[5, 6], help="Days to skip (0=Monday, 6=Sunday)")
    parser.add_argument("--holidays", default="~/data/holidays/india.holidays", help="Path to holiday file")
    parser.add_argument("--output", required=True, help="Output file path")
    
    args = parser.parse_args()
    
    holidays = parse_holidays(args.holidays)
    generate_tradable_dates(args.start_date, args.end_date, set(args.skip_days), holidays, args.output)
    
    print(f"Tradable dates written to {args.output}")

if __name__ == "__main__":
    main()
