import customtkinter as ctk
from tkinter import messagebox
import re 
from customtkinter.windows.widgets.font import CTkFont 

contacts = []

def validate_input(name, phone, email):
    """Simple validation for contact fields."""
    if not name or not phone:
        return "Name and Phone Number are required."
    
    if not re.fullmatch(r'[\d\s\-\(\)]+', phone):
        return "Invalid phone number format."
        
    if email and not re.fullmatch(r'[^@]+@[^@]+\.[^@]+', email):
        return "Invalid email address format."
        
    return None

def add_contact():
    """Implements functionality to add a new contact."""
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()
    
    validation_error = validate_input(name, phone, email)
    if validation_error:
        messagebox.showerror("Input Error", validation_error)
        return

    new_contact = {
        'id': len(contacts) + 1, 
        'name': name,
        'phone': phone,
        'email': email
    }
    
    contacts.append(new_contact)
    
    entry_name.delete(0, "end")
    entry_phone.delete(0, "end")
    entry_email.delete(0, "end")
    
    display_contacts(contacts)
    messagebox.showinfo("Success", f"Contact '{name}' added!")


def display_contacts(contact_list):
    """Updates the textbox with the provided list of contacts."""
    
    contacts_textbox.delete("1.0", "end")
    
    if not contact_list:
        contacts_textbox.insert("end", "No contacts found. Add a new contact above.")
        return

    contacts_textbox.insert("end", "--- CONTACT LIST ---\n", "header")
    
    for contact in contact_list:
        display_text = (
            f"ID: {contact['id']}\n"
            f"Name: {contact['name']}\n"
            f"Phone: {contact['phone']}\n"
            f"Email: {contact['email'] if contact['email'] else 'N/A'}\n"
            f"--------------------------\n"
        )
        contacts_textbox.insert("end", display_text)
        contacts_textbox.see("end")

def search_contact():
    """Searches for contacts by name and displays the matching list."""
    search_term = entry_search.get().strip().lower()
    
    if not search_term:
        display_contacts(contacts) 
        return
        
    matching_contacts = [
        c for c in contacts if search_term in c['name'].lower()
    ]
    
    display_contacts(matching_contacts)
    
    if not matching_contacts:
        contacts_textbox.delete("1.0", "end")
        contacts_textbox.insert("end", f"No contacts found matching '{search_term}'.")
def delete_contact():
    """Deletes a contact based on the ID entered in the dedicated delete box."""
    global contacts
    id_to_delete_str = entry_delete_id.get().strip() 
    
    try:
        id_to_delete = int(id_to_delete_str)
    except ValueError:
        messagebox.showerror("Deletion Error", "Please enter a valid numeric ID to delete.")
        return

    initial_count = len(contacts)
    contacts = [c for c in contacts if c['id'] != id_to_delete]
    
    if len(contacts) == initial_count:
        messagebox.showerror("Deletion Error", f"Contact with ID {id_to_delete} not found.")
    else:
        for i, contact in enumerate(contacts):
            contact['id'] = i + 1
            
        messagebox.showinfo("Success", f"Contact ID {id_to_delete} deleted.")
    entry_delete_id.delete(0, "end")
    display_contacts(contacts)

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue") 

app = ctk.CTk()
app.title("Simple Contact Book")
app.geometry("400x750")
app.resizable(False, False)
app.configure(fg_color="#ADD8E6") 

header_font = CTkFont(family="Arial", size=14, weight="bold")

title_label = ctk.CTkLabel(app, 
                           text="📱 Simple Contact Book", 
                           font=("Arial", 20, "bold"),
                           text_color="#005A99") 
title_label.pack(pady=(20, 5))
add_frame = ctk.CTkFrame(app, fg_color="white", corner_radius=10)
add_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(add_frame, text="Add New Contact", font=("Arial", 14, "bold"), text_color="#333333").pack(pady=(10, 5))

entry_name = ctk.CTkEntry(add_frame, placeholder_text="Name (Required)", width=300)
entry_name.pack(pady=5, padx=10)
entry_phone = ctk.CTkEntry(add_frame, placeholder_text="Phone Number (Required)", width=300)
entry_phone.pack(pady=5, padx=10)
entry_email = ctk.CTkEntry(add_frame, placeholder_text="Email (Optional)", width=300)
entry_email.pack(pady=5, padx=10)

ctk.CTkButton(add_frame, 
              text="➕ Add Contact", 
              command=add_contact,
              fg_color="#4CAF50",
              hover_color="#388E3C").pack(pady=(10, 15))
search_frame = ctk.CTkFrame(app, fg_color="white", corner_radius=10)
search_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(search_frame, text="Search Contacts", font=("Arial", 14, "bold"), text_color="#333333").pack(pady=(10, 5))
entry_search = ctk.CTkEntry(search_frame, placeholder_text="Search by Name", width=250)
entry_search.pack(side="left", padx=(10, 5), pady=10)

ctk.CTkButton(search_frame, 
              text="🔍 Search", 
              command=search_contact,
              fg_color="#007ACC",
              hover_color="#005A99",
              width=80).pack(side="left", padx=(5, 10), pady=10)
delete_frame = ctk.CTkFrame(app, fg_color="white", corner_radius=10)
delete_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(delete_frame, text="Delete Contact", font=("Arial", 14, "bold"), text_color="#CC0000").pack(pady=(10, 5))
entry_delete_id = ctk.CTkEntry(delete_frame, placeholder_text="Enter Contact ID to Delete (e.g., 1)", width=250)
entry_delete_id.pack(side="left", padx=(10, 5), pady=10)

ctk.CTkButton(delete_frame, 
              text="❌ Delete", 
              command=delete_contact,
              fg_color="#CC0000",
              hover_color="#990000",
              width=80).pack(side="left", padx=(5, 10), pady=10)
ctk.CTkLabel(app, text="Contact List", font=("Arial", 14, "bold"), text_color="#333333").pack(pady=(10, 5))

contacts_textbox = ctk.CTkTextbox(app, width=360, height=250, corner_radius=10, text_color="#333333")
contacts_textbox.pack(pady=10, padx=20)
if __name__ == '__main__':
    display_contacts(contacts) 
    app.mainloop()