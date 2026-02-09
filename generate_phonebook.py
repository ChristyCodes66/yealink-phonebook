import pandas as pd
from lxml import etree

COLUMN_MAP = {
    "Name": "Name",
    "Company": "Firma",    # only used for concatentation, not XML tag
    "Telephone": "Telefon"
}

# Read CSV (change sep to "," if needed) and force columns as strings
df = pd.read_csv(
    "contacts_test.csv",
    sep=";",
    encoding="utf-8",
    dtype={"Name": str, "Firma": str, "Telefon": str}  # force text
)

# shows first few rows
print("Number of rows read:", len(df))
print(df.head()) 

root = etree.Element("YealinkIPPhoneBook")
title = etree.SubElement(root, "Title")
title.text = "Company Phonebook"

directory = etree.SubElement(root, "Directory")

for _, row in df.iterrows():
    entry = etree.SubElement(directory, "Entry")

    # Combine Name + Company in a single <Name> tag
    full_name = f"{row[COLUMN_MAP["Name"]]} ({row[COLUMN_MAP["Company"]]})"
    etree.SubElement(entry, "Name").text = full_name

    # Telephone Number
    etree.SubElement(entry, "Telephone").text = row[COLUMN_MAP["Telephone"]]
    
tree = etree.ElementTree(root)
tree.write(
    "remote_phonebook.xml",
    pretty_print=True,
    xml_declaration=True,
    encoding="UTF-8"
)

print("Phonebook XML generated successfully.")
