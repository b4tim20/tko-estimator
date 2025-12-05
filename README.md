# TKO Estimator

Turns customer input into a clear, printable auto repair estimate and receipt.

> “Turns customer input into a pretty receipt.” :contentReference[oaicite:0]{index=0}

---

## Overview

TKO Estimator is a small Flask app plus a companion CLI tool for auto repair shops.

- Customers (or staff) fill out a simple online estimate form.
- The app calculates labor, shop fees, discounts, tax, and a grand total based on your shop settings. :contentReference[oaicite:1]{index=1}  
- When you’re ready, you can generate a professional-looking, text-based receipt from saved estimates using `pretty_receipt_printer.py`. :contentReference[oaicite:2]{index=2}  

The project is tailored for **TKO AUTO** but can be adapted for any small shop.

---

## Features

- 🧾 **Online estimate request form**
  - Customer & vehicle information
  - Labor hours
  - Misc fluids / shop fees
  - Optional discount (%) :contentReference[oaicite:3]{index=3}  
- 📊 **Automatic price breakdown**
  - Parts total, labor total, misc / shop supplies
  - Discount calculation
  - Taxable amount and sales tax
  - Grand total (estimate) :contentReference[oaicite:4]{index=4}  
- 🖨️ **Pretty receipt generator (CLI)**
  - Reads from `estimates.json`
  - Outputs a formatted, 68-column text receipt with shop header, line items, and totals :contentReference[oaicite:5]{index=5}  
- 🛠 **Shop-configurable**
  - Shop name and branding
  - Labor rate per hour
  - Tax rate
  - Contact info in the printed receipt header :contentReference[oaicite:6]{index=6}  

---

## Tech Stack

- **Python** (3.x)
- **Flask 3.0.0** for the web app :contentReference[oaicite:7]{index=7}  
- Simple **Jinja2 templates** for the form and estimate result views :contentReference[oaicite:8]{index=8}  

---

## Getting Started

### 1. Clone the repo

```bashFlask==3.0.0

