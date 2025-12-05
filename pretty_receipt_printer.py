# pretty_receipt_printer.py
# TKO AUTO – Professional Customer Receipt Generator
# Drop this file next to your estimates.json and run!

import json
import os
from datetime import datetime
from pathlib import Path

SHOP_NAME = "TKO AUTO"
SHOP_ADDRESS = "448 Thrift Ave. St. Louis, MO. 63137"
SHOP_PHONE = "refer to website"
SHOP_EMAIL = "support@tkoauto.online"
SHOP_TAGLINE = "Quality Work • Honest Prices • Lifetime Customer"

def load_estimates():
    if not Path("estimates.json").exists():
        print("estimates.json not found!")
        return []
    with open("estimates.json", "r", encoding="utf-8") as f:
        return json.load(f)

def fmt_currency(amount):
    return f"${amount:,.2f}"

def draw_line(char="=", length=68):
    return char * length

def print_receipt(est):
    lines = []
    created = datetime.fromisoformat(est["created_at"].replace("T", " ")[:19])
    date_str = created.strftime("%b %d, %Y at %I:%M %p")

    # Header
    lines.append(draw_line("═"))
    lines.append(f"{SHOP_NAME:^68}")
    lines.append(f"{SHOP_ADDRESS:^68}")
    lines.append(f"{SHOP_PHONE} • {SHOP_EMAIL}")
    lines.append(f"{SHOP_TAGLINE:^68}")
    lines.append(draw_line("═"))
    lines.append("")

    # Customer & Vehicle
    cust = est["customer"]
    veh = est["vehicle"]
    lines.append(f"Customer: {cust.get('name', 'Walk-In').title()}")
    if cust.get("phone") and cust["phone"] not in ["n/a", ""]:
        lines.append(f"Phone:    {cust['phone']}")
    if cust.get("email") and cust["email"] not in ["n/a", ""]:
        lines.append(f"Email:    {cust['email']}")
    lines.append("")
    lines.append(f"Vehicle:  {veh.get('year', '')} {veh.get('make', '')} {veh.get('model', '')}".strip())
    if veh.get("license_plate"):
        lines.append(f"Plate:    {veh['license_plate']}  |  Mileage: {veh.get('mileage', 'N/A')}")
    if veh.get("vin"):
        lines.append(f"VIN:      {veh['vin']}")
    lines.append("")

    # Complaint
    lines.append(f"Concern:  {est.get('complaint', 'Routine Service')}")
    if est.get("notes"):
        lines.append(f"Notes:    {est['notes']}")
    lines.append(draw_line("-", 68))

    # Parts
    if est.get("parts"):
        lines.append(f"{'PARTS':<40} {'QTY':>6} {'PRICE':>10} {'TOTAL':>10}")
        lines.append(draw_line("-", 68))
        for p in est["parts"]:
            desc = p["description"][:35]
            qty = f"{p['qty']:.0f}" if p['qty'] == int(p['qty']) else f"{p['qty']:.1f}"
            lines.append(f"{desc:<40} {qty:>6} {fmt_currency(p['unit_price']):>10} {fmt_currency(p['line_total']):>10}")
        lines.append("")

    # Labor
    if est.get("labor"):
        lines.append(f"{'LABOR':<40} {'HRS':>6} {'RATE':>10} {'TOTAL':>10}")
        lines.append(draw_line("-", 68))
        for l in est["labor"]:
            desc = l["description"][:35]
            hrs = f"{l['hours']:.1f}"
            lines.append(f"{desc:<40} {hrs:>6} {fmt_currency(l['rate']):>10} {fmt_currency(l['line_total']):>10}")
        lines.append("")

    # Totals
    t = est["totals"]
    lines.append(draw_line("─", 68))
    lines.append(f"{'Parts Total':<48} {fmt_currency(t['parts_total']):>18}")
    lines.append(f"{'Labor Total':<48} {fmt_currency(t['labor_total']):>18}")
    lines.append(f"{'Shop Supplies':<48} {fmt_currency(t['shop_supplies']):>18}")
    lines.append(f"{'Hazardous Waste Fee':<48} {fmt_currency(t.get('misc_total', 5.0)):>18}")
    if t["discount_amount"] > 0:
        lines.append(f"{'Discount':<48} -{fmt_currency(t['discount_amount']):>18}")
    lines.append(f"{'Subtotal':<48} {fmt_currency(t['subtotal']):>18}")
    lines.append(f"{'Tax':<48} {fmt_currency(t['tax_amount']):>18}")
    lines.append(draw_line("=", 68))
    lines.append(f"{'GRAND TOTAL':<48} {fmt_currency(t['grand_total']):>18}")
    lines.append(draw_line("=", 68))

    # Status & Expiry
    status = est.get("status", "estimate").upper()
    lines.append(f"\nEstimate #{est['id']:06d} • Created: {date_str}")
    if est.get("expiry_date"):
        exp = datetime.strptime(est["expiry_date"], "%Y-%m-%d").strftime("%B %d, %Y")
        lines.append(f"Valid until {exp} • Status: {status}")

    lines.append("\nThank you for choosing TKO AUTO!")
    lines.append("We stand behind our work. See reverse for warranty details.")

    # Save to file
    safe_name = "".join(c if c.isalnum() else "_" for c in cust.get("name", "Customer"))
    filename = f"Receipt_{est['id']:06d}_{safe_name.title()}_{created.strftime('%Y-%m-%d')}.txt"
    Path("Receipts").mkdir(exist_ok=True)
    with open(Path("Receipts") / filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generated → Receipts/{filename}")

# MAIN
if __name__ == "__main__":
    print("TKO AUTO – Professional Receipt Printer\n")
    estimates = load_estimates()
    if not estimates:
        print("No estimates found.")
        input("Press Enter to exit...")
    else:
        print(f"Found {len(estimates)} estimate(s). Generating beautiful receipts...\n")
        for est in estimates:
            print_receipt(est)
        print("\nAll done! Check the new 'Receipts' folder.")
        input("\nPress Enter to exit...")