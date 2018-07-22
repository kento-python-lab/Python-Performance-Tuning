def list_unique_names(phonebook):
    unique_names = []
    for name, phonenumber in phonebook:
       first_name, last_name = name.split(" ", 1)
       for unique in unique_names:
           if unique == first_name:
               break
       else:
           unique_names.append(first_name)
    return len(unique_names)


def set_unique_names(phonebook):
    unique_names = set()
    for name, phonenumber in phonebook:
        first_name, last_name = name.split(" ", 1)
        unique_names.add(first_name)
    return len(unique_names)


phonebook = [
    ("John Doe", "555-555-5555"),
    ("Albert Einstein", "212-555-5555"),
    ("John Murphey", "202-555-5555"),
    ("Albert Rutherford", "647-555-5555"),
    ("Elaine Bodian", "301-555-5555"),
]

print("Number of unique names from set method:  ", set_unique_names(phonebook))
print("Number of unique names from list method: ", list_unique_names(phonebook))
