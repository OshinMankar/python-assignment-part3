#Task 1 — File Read & Write Basics
import requests
from datetime import datetime

file = open("python_notes.txt", "w", encoding="utf-8") #'w' - creates files & 'utf-8' - supports all characters

file.write("Topic 1: Variables store data. Python is dynamically typed.\n") # writing lines
file.write("Topic 2: Lists are ordered and mutable.\n")
file.write("Topic 3: Dictionaries store key-value pairs.\n")
file.write("Topic 4: Loops automate repetitive tasks.\n")
file.write("Topic 5: Exception handling prevents crashes.\n")

file.close()
print("File written successfully.\n") #closes the file after writing

file = open("python_notes.txt", "a", encoding="utf-8") # 'a' - add data without deleting existing content
file.write("Topic 6: Functions help reuse.\n")
file.write("Topic 7: APIs allow communication between systems.\n")
file.close()

print("Lines appended.\n") #confirmation message

file = open("python_notes.txt", "r", encoding="utf-8") #read file

lines = file.readlines() #reads file into list
file.close()

count = 1

for line in lines:
    print(str(count) + ". " + line.strip()) 
    count = count + 1

print("\nTotal lines: " + str(len(lines)))

keyword = input("\nEnter keyword to search: ").lower()

found = False

for line in lines:
    if keyword in line.lower():
        print(line.strip())
        found = True

if found == False:
    print("No matching lines found.")

#Task 2 — API Integration


def log_error(function_name, message):
    file = open("error_log.txt", "a")
    time = str(datetime.now())
    file.write("[" + time + "] ERROR in " + function_name + ": " + message + "\n")
    file.close()

print("\n===== PRODUCTS =====")

products = []

try:
    response = requests.get("https://dummyjson.com/products?limit=20", timeout=5)
    data = response.json()

    products = data["products"]

    print("ID | Title | Category | Price | Rating")

    for p in products:
        print(str(p["id"])+" | " + p["title"]+ " | " + p["category"]+ " | $" + str(p["price"]) + " | " + str(p["rating"]))

except requests.exceptions.ConnectionError:
    print("Connection failed.")
    log_error("fetch_products", "ConnectionError")

except requests.exceptions.Timeout:
    print("Request timed out.")
    log_error("fetch_products", "Timeout")

except Exception as e:
    print("Error:", e)
    log_error("fetch_products", str(e))

print("\nFiltered Products (rating >= 4.5):")

filtered = []

for p in products:
    if p["rating"] >= 4.5:
        filtered.append(p)

for i in range(len(filtered)):
    for j in range(i+1, len(filtered)):
        if filtered[i]["price"] < filtered[j]["price"]:
            temp = filtered[i]
            filtered[i] = filtered[j]
            filtered[j] = temp

for p in filtered:
    print(p["title"], p["price"], p["rating"])

print("\n====== LAPTOPS =======")

try:
    response = requests.get("https://dummyjson.com/products/category/laptops", timeout=5)
    data = response.json()

    for p in data["products"]:
        print(p["title"], "$" + str(p["price"]))

except Exception as e:
    print("Error:", e)
    log_error("laptops", str(e))

print("\n======== ADD PRODUCT ==========")

try:
    new_product = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"    
    }

    response = requests.post("https://dummyjson.com/products/add", json=new_product, timeout=5)

    print(response.json())

except Exception as e:
    print("Error:", e)
    log_error("add_product", str(e))

#TASK 3 - Exception Handling

def safe_divide(a, b): # safe divide function
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"
    
print("\nSafe Divide Tests:")
print(safe_divide(10,2))
print(safe_divide(10,0))
print(safe_divide("ten",2))

def read_file_safe(filename): #Safe file reader
    try:
        file = open(filename, "r")
        data = file.read()
        file.close()
        return data
    except FileNotFoundError:
        print("Error: File '" + filename + " ' not found.")
    finally:
        print("File operation attempt complete.")

print("\nReading file:")
print(read_file_safe("python_notes.txt"))
read_file_safe("ghost_file.txt") 

print("\n====== PRODUCT LOOKUP =======")

while True:
    user_input = input("Enter product ID (1-100) or 'quit':")

    if user_input == "quit":
        break

    if user_input.isdigit() == False:
        print("Invalid input")
        continue

    pid = int(user_input)

    if pid < 1 or pid > 100:
        print("Enter ID between 1-100")
        continue

    try:
        url = "https://dummyjson.com/products/" + str(pid)
        response = requests.get(url, timeout=5)

        if response.status_code == 404:
            print("Product not found.")
            log_error("lookup_product", "404 for ID" + str(pid))
        else:
            data = response.json()
            print(data["title"], "$" + str(data["price"]))

    except requests.exceptions.ConnectionError:
        print("Connection failed.")
        log_error("lookup_products", "ConnectionError")

    except requests.exceptions.Timeout:
        print("Request timed out.")
        log_error("lookup_products", "Timeout")
    
    except Exception as e:
        print("Error:", e)
        log_error("lookup_product", str(e))

# TASK 4 - Logging Test

try: #Trigger connection error
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except requests.exceptions.ConnectionError:
    print("Test Connection Error Triggered")
    log_error("test_connection", "ConnectionError")

try:
    response = requests.get("https://dummyjson.com/products/999", timeout=5)

    if response.status_code != 200:
        print("Test 404 Error Triggered")
        log_error("lookup_prouct", "404 Not Found for product ID 999")

except Exception as e:
        log_error("lookup_product", str(e))


print("\n========ERROR LOG ========") #Read log file

file = open("error_log.txt", "r")
print(file.read)
file.close()
