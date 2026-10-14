import pandas as pd
import os

# Change to the dataset directory
os.chdir(r'd:\supply_chain_dataset')

# Dictionary to store issues found
issues = {}

print("=" * 80)
print("DATA QUALITY ANALYSIS FOR SUPPLY CHAIN DATASET")
print("=" * 80)

# 1. Analyze DELIVERIES.csv
print("\n[1] ANALYZING deliveries.csv")
deliveries = pd.read_csv('deliveries.csv')
delivery_issues = []

# Check for empty customer_rating
empty_ratings = deliveries[deliveries['customer_rating'].isna()]
if len(empty_ratings) > 0:
    delivery_issues.append(f"  ❌ {len(empty_ratings)} rows with empty customer_rating")
    print(f"  ❌ {len(empty_ratings)} rows with empty customer_rating (for non-delivered items)")

# Check for empty proof_of_delivery
empty_proof = deliveries[deliveries['proof_of_delivery'].isna()]
if len(empty_proof) > 0:
    delivery_issues.append(f"  ❌ {len(empty_proof)} rows with empty proof_of_delivery")
    print(f"  ❌ {len(empty_proof)} rows with empty proof_of_delivery")

issues['deliveries'] = delivery_issues

# 2. Analyze INVENTORY.csv
print("\n[2] ANALYZING inventory.csv")
inventory = pd.read_csv('inventory.csv')
inventory_issues = []

# Check for stock_on_hand < reserved_stock (logical inconsistency)
invalid_stock = inventory[inventory['stock_on_hand'] < inventory['reserved_stock']]
if len(invalid_stock) > 0:
    inventory_issues.append(f"  ❌ {len(invalid_stock)} rows with stock_on_hand < reserved_stock")
    print(f"  ❌ {len(invalid_stock)} rows with stock_on_hand < reserved_stock (logical error)")

issues['inventory'] = inventory_issues

# 3. Analyze PRODUCTS.csv
print("\n[3] ANALYZING products.csv")
products = pd.read_csv('products.csv')
product_issues = []

# Check for unit_price < cost_price (should have positive margin)
invalid_pricing = products[products['unit_price'] < products['cost_price']]
if len(invalid_pricing) > 0:
    product_issues.append(f"  ❌ {len(invalid_pricing)} rows with unit_price < cost_price")
    print(f"  ❌ {len(invalid_pricing)} rows with unit_price < cost_price (negative profit margin)")

issues['products'] = product_issues

# 4. Analyze ORDERS.csv
print("\n[4] ANALYZING orders.csv")
orders = pd.read_csv('orders.csv')
order_issues = []

# Check for discount > 100%
invalid_discount = orders[orders['discount_pct'] > 100]
if len(invalid_discount) > 0:
    order_issues.append(f"  ❌ {len(invalid_discount)} rows with discount > 100%")
    print(f"  ❌ {len(invalid_discount)} rows with discount > 100%")

# Check for negative quantities
invalid_qty = orders[orders['quantity'] <= 0]
if len(invalid_qty) > 0:
    order_issues.append(f"  ❌ {len(invalid_qty)} rows with zero or negative quantity")
    print(f"  ❌ {len(invalid_qty)} rows with zero or negative quantity")

# Check for negative unit_price
invalid_price = orders[orders['unit_price'] <= 0]
if len(invalid_price) > 0:
    order_issues.append(f"  ❌ {len(invalid_price)} rows with zero or negative unit_price")
    print(f"  ❌ {len(invalid_price)} rows with zero or negative unit_price")

issues['orders'] = order_issues

# 5. Analyze SHIPMENTS.csv
print("\n[5] ANALYZING shipments.csv")
shipments = pd.read_csv('shipments.csv')
shipment_issues = []

# Check for negative distance
invalid_distance = shipments[shipments['distance_km'] < 0]
if len(invalid_distance) > 0:
    shipment_issues.append(f"  ❌ {len(invalid_distance)} rows with negative distance")
    print(f"  ❌ {len(invalid_distance)} rows with negative distance_km")

# Check for negative cost
invalid_cost = shipments[shipments['shipping_cost'] < 0]
if len(invalid_cost) > 0:
    shipment_issues.append(f"  ❌ {len(invalid_cost)} rows with negative shipping_cost")
    print(f"  ❌ {len(invalid_cost)} rows with negative shipping_cost")

# Check for inconsistent delay_days (should match dates)
shipments['actual_delivery_date'] = pd.to_datetime(shipments['actual_delivery_date'], errors='coerce')
shipments['expected_delivery_date'] = pd.to_datetime(shipments['expected_delivery_date'], errors='coerce')
shipments['calculated_delay'] = (shipments['actual_delivery_date'] - shipments['expected_delivery_date']).dt.days
delay_mismatch = shipments[shipments['delay_days'] != shipments['calculated_delay']]
if len(delay_mismatch) > 0:
    shipment_issues.append(f"  ❌ {len(delay_mismatch)} rows with mismatched delay_days")
    print(f"  ⚠️  {len(delay_mismatch)} rows with mismatched delay_days (recalculation needed)")

issues['shipments'] = shipment_issues

# 6. Check for duplicates in ID fields
print("\n[6] CHECKING FOR DUPLICATES")
duplicate_issues = []

files_to_check = {
    'carriers.csv': 'carrier_id',
    'customers.csv': 'customer_id',
    'products.csv': 'product_id',
    'suppliers.csv': 'supplier_id',
    'warehouses.csv': 'warehouse_id'
}

for filename, id_col in files_to_check.items():
    df = pd.read_csv(filename)
    dups = df[df.duplicated(subset=[id_col], keep=False)]
    if len(dups) > 0:
        duplicate_issues.append(f"  ❌ {filename}: {len(dups)} duplicate {id_col} values")
        print(f"  ❌ {filename}: {len(dups)} duplicate {id_col} values")

print("\n" + "=" * 80)
print("SUMMARY OF ISSUES FOUND")
print("=" * 80)

total_issues = sum(len(v) for v in issues.values()) + len(duplicate_issues)
if total_issues == 0:
    print("✓ No major data quality issues detected!")
else:
    print(f"Total issues found: {total_issues}")
    for category, msgs in issues.items():
        for msg in msgs:
            print(msg)
    for msg in duplicate_issues:
        print(msg)

print("\n" + "=" * 80)
