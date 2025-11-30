def read_purchases(path):
    purchases = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            parts = line.split(';')

            if len(parts) != 5:
                continue

            date = parts[0].strip()
            category = parts[1].strip()
            name = parts[2].strip()
            price_str = parts[3].strip()
            qty_str = parts[4].strip()

            try:
                price = float(price_str)
                qty = float(qty_str)
            except ValueError:
                continue


            if price < 0 or qty < 0:
                continue

            purchase = {
                "date": date,
                "category": category,
                "name": name,
                "price": price,
                "qty": qty,
            }
            purchases.append(purchase)
    return purchases


def count_errors(path):
    valid_count = 0
    total_count = 0
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            total_count += 1
            line = line.strip()
            if not line:
                continue

            parts = line.split(';')

            if len(parts) != 5:
                continue

            price_str = parts[3].strip()
            qty_str = parts[4].strip()

            try:
                price = float(price_str)
                qty = float(qty_str)
            except ValueError:
                continue

            if price < 0 or qty < 0:
                continue

            valid_count += 1

    return total_count - valid_count


def total_spent(purchases):
    total = 0.0
    for p in purchases:
        total += p["price"] * p["qty"]
    return total


def spent_by_category(purchases):
    result = {}
    for p in purchases:
        category = p["category"]
        amount = p["price"] * p["qty"]
        if category not in result:
            result[category] = 0.0
        result[category] += amount
    return result


def top_n_expensive(purchases, n=3):

    purchases_with_cost = []
    for p in purchases:
        cost = p["price"] * p["qty"]

        new_p = dict(p)
        new_p["cost"] = cost
        purchases_with_cost.append(new_p)


    purchases_with_cost.sort(key=lambda x: x["cost"], reverse=True)

    return purchases_with_cost[:n]


def write_report(purchases, errors, out_path):
    total = total_spent(purchases)
    by_cat = spent_by_category(purchases)
    top3 = top_n_expensive(purchases, 3)

    report_lines = []

    report_lines.append("VALID PURCHASES: " + str(len(purchases)) + "\n")
    report_lines.append("ERROR LINES: " + str(errors) + "\n")
    report_lines.append("TOTAL SPENT: " + str(total) + "\n")
    report_lines.append("\n")

    report_lines.append("SPENT BY CATEGORY:\n")
    for category, amount in by_cat.items():
        report_lines.append(f"  {category}: {amount}\n")
    report_lines.append("\n")

    report_lines.append("TOP 3 EXPENSIVE PURCHASES:\n")
    for p in top3:
        line = (
            f"  {p['date']} | {p['category']} | {p['name']} "
            f"| price={p['price']} qty={p['qty']} cost={p['cost']}\n"
        )
        report_lines.append(line)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(report_lines)