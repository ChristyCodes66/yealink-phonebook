import pandas as pd
from lxml import etree

CSV_FILE = "contacts_test.csv"
OUTPUT_XML = "remote_phonebook.xml"

# COLUMN_MAP = {
#     "Name": "Name",
#     "Company": "Firma",    # only used for concatentation, not XML tag
#     "Telephone": "Telefon"
# }

# Read CSV (change sep to "," if needed) and force columns as strings
df = pd.read_csv(
    CSV_FILE,
    sep=";",
    dtype=str,
    keep_default_na=False   # prevents "nan"
)

# shows first few rows
print(f"Rows read: {len(df)}")
print(df.head()) 

root = etree.Element("root_contact")

for index, row in df.iterrows():
    # --- Mandatory Fields ---
    display_name = row["DisplayName"].strip()
    office_number = row["OfficeNumber"].strip()

    if not display_name or not office_number:
        print(f"Skipping row {index + 1}: missing DisplayName or OfficeNumber")
        continue

    # --- Optional Fields ---
    company = row["Company"].strip()
    mobile = row["MobileNumber"].strip()
    other = row["OtherNumber"].strip()

    # --- Concat company into display name ---
    if company:
        display_name = f"{display_name} ({company})"

    etree.SubElement(
        root,
        "contact", 
        display_name = display_name,
        office_number = office_number,
        mobile_number = mobile,
        other_number = other
    )

tree = etree.ElementTree(root)
tree.write(
    OUTPUT_XML,
    pretty_print=True,
    xml_declaration=True,
    encoding="UTF-8"
)

print("Phonebook XML generated successfully.")
