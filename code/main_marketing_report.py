"""
main_marketing_report.py — the Marketing department's report.

Marketing does not care about individual transactions. They care about *products*:
which one earns the most money, and which one moves the most units. Those are
frequently not the same product, and the gap between them is the interesting part.

This is the payoff for building a package instead of a script. Marketing needs a
roll-up that Finance never asked for, so `summarize_by_item` and `find_top_entry`
were **added** to `sales_pipeline.transform` — and `main_finance_report.py` did
not change by a single character. That is what modular means: the package grows
by addition, not by editing everyone who already depends on it.

Before running:  pip install -r requirements.txt

    python code/main_marketing_report.py        # the fixed sample data
    python code/main_marketing_report.py 42     # the generated data for seed 42
"""

import sys

from sales_pipeline import (
    get_raw_sales_data,
    clean_sales_data,
    summarize_by_item,
    find_top_entry,
    print_item_table,
)

# --- Reading the dataset seed ----------------------------------------------------

seed = None
if len(sys.argv) > 1 and sys.argv[1].strip() != "":
    seed = int(sys.argv[1])


# --- The report ------------------------------------------------------------------

print("=== MARKETING: Revenue by Item ===")
print()

# 1. Extract — the same source Finance uses, called the same way.
raw_data = get_raw_sales_data(seed)

# 2. Transform — clean the rows, roll them up to one entry per item, then find the
#    best entry twice: once by "revenue", once by "units_sold".
clean_data = clean_sales_data(raw_data)
item_summary = summarize_by_item(clean_data)
top_earner = find_top_entry(item_summary, "revenue")
top_mover = find_top_entry(item_summary, "units_sold")

# 3. Load — the item table, a blank line, then two headline lines.
print_item_table(item_summary)
print()
print(f"Top seller by revenue: {top_earner['item']} (${top_earner['revenue']:,.2f})")
print(f"Top seller by units:   {top_mover['item']} ({top_mover['units_sold']} units)")
