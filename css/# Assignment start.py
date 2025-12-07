# Assignment start
# Task 2: Program structure to read a CSV file, and take care of any errors

from datetime import date   # Used to print today's date in the report


# -------------------------------
# MAIN FUNCTION – program entry point
# -------------------------------
def main():
    path = "500000 Sales Records.csv"     # Name of the data file
    file = open_file(path)                # Attempt to open the file

    # If file failed to open, stop the whole program
    if file is None:
        return

    # If file opened correctly, start the menu system
    menu(file)



# -------------------------------
# Task 2 — Open File Using try/except
# -------------------------------
def open_file(path):
    """Attempts to open the CSV file safely."""

    try:
        file = open(path, "r", encoding="utf-8")   # Try to open file for reading
        return file                                # Return the file object if successful

    # If any error happens (ex: file not found), print required message
    except Exception:
        print("Sorry an error has occurred.")
        return None                                 # Signal to main() that file failed



# -------------------------------
# Task 3.1 — Total Profit by Country
# -------------------------------
def total_profit_by_country(country_name, file):

    if file is None:
        return None      # Defensive programming - prevents crashes

    file.seek(0)         # Start reading from the beginning
    file.readline()      # Skip the header row

    profit_total = 0.0   # Accumulator for profit

    for line in file:
        fields = line.strip().split(",")

        # Skip broken or incomplete lines (safety check)
        if len(fields) < 14:
            continue

        # fields[1]  = Country column
        # fields[13] = Total Profit column
        if fields[1].strip().lower() == country_name.strip().lower():
            profit_total += float(fields[13])   # Add profit for matching country

    return profit_total



# -------------------------------
# Task 3.2 — Total Profit by Region
# -------------------------------
def total_profit_by_region(region_name, file):

    if file is None:
        return None

    file.seek(0)
    file.readline()

    total_profit = 0.0

    for line in file:
        fields = line.strip().split(",")

        if len(fields) < 14:
            continue

        # fields:
        # [0] → Region
        # [13] → Total Profit
        region = fields[0].strip()
        profit = float(fields[13])

        # Case-insensitive comparison
        if region.lower() == region_name.strip().lower():
            total_profit += profit

    return total_profit



# -------------------------------
# Task 3.3 — Generate All Regional + Grand Totals
# -------------------------------
def generate_all_totals(file):

    if file is None:
        return None

    file.seek(0)
    file.readline()

    regions = []   # Will store unique region names

    # ---- First pass: collect all unique regions ----
    for line in file:
        fields = line.strip().split(",")

        if len(fields) < 14:
            continue

        region = fields[0].strip()

        # Only add region once
        if region not in regions:
            regions.append(region)

    # Sort alphabetically for cleaner output
    regions = sorted(regions)

    # ---- Second pass: compute totals ----
    file.seek(0)
    file.readline()

    units_by_region = {}     # Total units for each region
    revenue_by_region = {}   # Total revenue for each region

    grand_units = 0.0        # Units sold across all regions
    grand_revenue = 0.0      # Total revenue across all regions

    for line in file:
        fields = line.strip().split(",")

        if len(fields) < 14:
            continue

        # fields:
        # [8]  → Units Sold
        # [11] → Total Revenue
        region = fields[0].strip()
        units = float(fields[8])
        revenue = float(fields[11])

        # Initialize dictionaries if region is new
        if region not in units_by_region:
            units_by_region[region] = 0.0
            revenue_by_region[region] = 0.0

        # Update totals
        units_by_region[region] += units
        revenue_by_region[region] += revenue

        # Update grand totals
        grand_units += units
        grand_revenue += revenue

    # ---- Build a dictionary summarizing all regional totals ----
    region_totals = {}

    for region in regions:
        total_units = units_by_region[region]
        total_revenue = revenue_by_region[region]

        # Avoid division by zero
        if total_units > 0:
            avg_rev = total_revenue / total_units
        else:
            avg_rev = 0.0

        region_totals[region] = {
            "units": total_units,
            "avg_revenue": avg_rev,
            "revenue": total_revenue
        }

    # Compute overall average revenue per unit
    if grand_units > 0:
        grand_avg_rev = grand_revenue / grand_units
    else:
        grand_avg_rev = 0.0

    # Return all results needed by the report function
    return regions, region_totals, grand_units, grand_avg_rev, grand_revenue



# -------------------------------
# Task 4 — Printing the Report
# -------------------------------
def print_report(file):

    data = generate_all_totals(file)

    # If something failed while processing
    if data is None:
        print("Sorry an error has occurred.")
        return

    regions, region_totals, grand_units, grand_avg, grand_rev = data

    print("\nSales Report")
    print("------------\n")

    # Print today’s date in required format
    today = date.today().isoformat()
    print("Produced on:", today)
    print()

    # Show all regions included in the report
    print("Regions analyzed:", ", ".join(regions))
    print()
    print("Total,", len(regions), "regions.\n")

    # Print region-by-region details
    for region in regions:
        stats = region_totals[region]

        print(region)
        print(" Total units sold:              ", format(stats["units"], ",.0f"))
        print(" Average revenue per unit:      $", format(stats["avg_revenue"], ",.2f"), sep="")
        print(" Total revenue of sales:        $", format(stats["revenue"], ",.2f"), sep="")
        print()

    # Print grand totals
    print("Grand Totals")
    print("------------\n")
    print(" Total units sold:              ", format(grand_units, ",.0f"))
    print(" Average revenue per unit:      $", format(grand_avg, ",.2f"), sep="")
    print(" Total revenue of sales:        $", format(grand_rev, ",.2f"), sep="")
    print()



# -------------------------------
# Task 5 — Menu System
# -------------------------------
def menu(file):

    while True:
        print("\nWelcome to Data analysis tools.")
        print("Select from one of the following options:")
        print("1) Total profit based on a country")
        print("2) Total profit based on a region")
        print("3) Generate report")
        print("4) Exit\n")

        choice = input("Enter your choice (1-4): ")

        # ---- Option 1: Profit by country ----
        if choice == "1":
            country = input("Please provide the name of the country: ")
            result = total_profit_by_country(country, file)

            if result == 0:
                print("No records found for this country.\n")
            elif result is not None:
                print("The total profit is:", format(result, ",.2f") + "$\n")

        # ---- Option 2: Profit by region ----
        elif choice == "2":
            region = input("Please provide the name of the region: ")
            result = total_profit_by_region(region, file)

            if result == 0:
                print("No records found for this region.\n")
            elif result is not None:
                print("The total profit is:", format(result, ",.2f") + "$\n")

        # ---- Option 3: Generate complete report ----
        elif choice == "3":
            print_report(file)

        # ---- Option 4: Exit the program ----
        elif choice == "4":
            print("Process finished with exit code 0")
            break

        else:
            print("Invalid selection. Please choose a number between 1 and 4.")



# -------------------------------
# Program Execution Starts Here
# -------------------------------
main()
