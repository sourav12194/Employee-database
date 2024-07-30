
import sqlite3

# Database connection setup
conn = sqlite3.connect('company.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                email TEXT UNIQUE
            )''')

# Function to create a new employee
def create_employee(name, age, email):
    """
    This function used to add a new employee to the database.
    
    Parameters:
     name(str): Name of the employee.
     age(int): Age of the employee.   
     email(str): Email of the employee.      

    Returns:
    The function will return the ID of the new employee if successfull, otherwise it will return none.
    
    If an employee with the same email already exists, it will show an error message.

    """
    
    try:
        c.execute("INSERT INTO employees (name, age, email) VALUES (?,?,?)", (name, age, email))
        conn.commit()
        employee_id = c.lastrowid
        print(f"Employee '{name}' added successfully with id:{employee_id}.")
        return employee_id
    except sqlite3.IntegrityError as e:
        print(f"Error: Employee with email '{email}' already exists.")

        return None

# Function to read and print all employees
def read_employees():
    """
    This function used to fetch and print all employees from the database.
    
    Displays the list of all employees with their details.
    If no employees are found, it will show a error message.
    """
    c.execute("SELECT * FROM employees")
    employees = c.fetchall()
    if employees:
        print("\nEmployee List:")
        for employee in employees:
            print(employee)
    else:
        print("No employees found.")

# Function to update an employee's details
def update_employee(id, name, age, email):
    """
    This function used to update details of an existing employee in the database.
    
    Parameters:
        id(int): ID of the employee to be updated.
        name(str): New name for the employee.
        age(int): New age for the employee.
        email(str): New email for the employee.

    If the employee ID is not found, it will show an error message.
    If an employee with the same email already exists, it will show an error message.
    
    """
    try:
        c.execute("UPDATE employees SET name=?, age=?, email=? WHERE id=?", (name, age, email, id))
        if c.rowcount > 0:
            conn.commit()
            print(f"Employee with ID {id} updated successfully.")
        else:
            print(f"Error: Employee with ID {id} not found.")
    except sqlite3.IntegrityError:
        print(f"Error: Employee with email '{email}' already exists.")

# Function to delete an employee
def delete_employee(id):
    """
    This function used to remove an employee from the database.
    
    Parameters:
        id(int): ID of the employee to be deleted.
    
    If the employee ID is not found, it will Show an error message.
    """
    c.execute("DELETE FROM employees WHERE id=?", (id,))
    if c.rowcount > 0:
        conn.commit()
        print(f"Employee with ID {id} deleted successfully.")
    else:
        print(f"Error: Employee with ID {id} not found.")

# Main script to demonstrate CRUD operations
if __name__ == "__main__":
    is_run = True
    while is_run:
        user_choice = input("\nC = create \nR = read\nU = update\nD = delete\nE = exit\nWhat do you want?: ")

        if user_choice.lower() == "c":
            name = input("Enter name: ")
            age = input("Enter age: ")
            email = input("Enter email: ")
            id = create_employee(name, age, email)
        elif user_choice.lower() == "r":
            read_employees()
            print("\n")
        elif user_choice.lower() == "u":
            id = input("Enter your id: ")
            name = input("Enter name: ")
            age = input("Enter age: ")
            email = input("Enter email: ")
            print("\n")
            update_employee(id, name, age, email)
            print("\n")
        elif user_choice.lower() == "d":
            id = input("Enter id to delete: ")
            delete_employee(id)
            print("\n")
        elif user_choice.lower() == "e":
            is_run = False
        else:
            print("\nPlease enter valid input.")

# Close database connection
conn.close()

