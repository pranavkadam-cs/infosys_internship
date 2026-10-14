import pandas as pd

df = pd.read_csv("orders.csv")

# Remove duplicate rows
df = df.drop_duplicates()

# Remove extra spaces from text columns
text_cols = df.select_dtypes(include="object").columns
df[text_cols] = df[text_cols].apply(lambda x: x.str.strip())

# Save cleaned dataset
df.to_csv("orders_cleaned.csv", index=False)

print("Cleaning completed!")
print(df.info())