import re, json

# Class mapping based on MasterclassID
CLASS_MAP = {
    5: "I",
    6: "II",
    7: "III",
    8: "IV",
    9: "V",
    10: "VI",
    11: "VII",
    12: "VIII"
}

# We will read the raw text of the 15 pages and parse them.
# Let's inspect the file where we can store raw page data.
print("Script template ready.")
