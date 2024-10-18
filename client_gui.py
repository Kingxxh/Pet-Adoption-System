import grpc
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import pet_adoption_pb2
import pet_adoption_pb2_grpc
import io  # Used for handling binary data


class PetAdoptionClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Pet Adoption System")

        # Server connection
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = pet_adoption_pb2_grpc.PetAdoptionServiceStub(self.channel)

        # Registration form
        tk.Label(root, text="Register a Pet").grid(row=0, column=0, columnspan=2)

        tk.Label(root, text="Name:").grid(row=1, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=1, column=1)

        tk.Label(root, text="Gender:").grid(row=2, column=0)
        # Gender selection box (Male or Female)
        self.gender_var = tk.StringVar(root)
        self.gender_var.set("Male")  # Default selection is Male
        self.gender_menu = tk.OptionMenu(root, self.gender_var, "Male", "Female")
        self.gender_menu.grid(row=2, column=1)

        tk.Label(root, text="Age:").grid(row=3, column=0)
        self.age_entry = tk.Entry(root)
        self.age_entry.grid(row=3, column=1)

        tk.Label(root, text="Breed:").grid(row=4, column=0)
        self.breed_entry = tk.Entry(root)
        self.breed_entry.grid(row=4, column=1)

        tk.Button(root, text="Choose Photo", command=self.choose_photo).grid(row=5, column=0, columnspan=2)
        self.photo_path_label = tk.Label(root, text="No photo selected")
        self.photo_path_label.grid(row=6, column=0, columnspan=2)

        tk.Button(root, text="Register Pet", command=self.register_pet).grid(row=7, column=0, columnspan=2)

        # Add New Registration Button to clear form
        tk.Button(root, text="New Registration", command=self.clear_registration_form).grid(row=8, column=0, columnspan=2)

        # Search form
        tk.Label(root, text="Search for a Pet").grid(row=9, column=0, columnspan=2)

        # Add search conditions: name, gender, age, or breed
        self.search_options = ["name", "gender", "age", "breed"]
        self.search_key = tk.StringVar(root)
        self.search_key.set(self.search_options[0])  # Default search by name
        self.search_menu = tk.OptionMenu(root, self.search_key, *self.search_options, command=self.update_search_field)
        self.search_menu.grid(row=10, column=1)

        tk.Label(root, text="Search by:").grid(row=10, column=0)

        self.search_entry = tk.Entry(root)  # Default is a text input field
        self.search_entry.grid(row=11, column=1)

        tk.Button(root, text="Search Pet", command=self.search_pet).grid(row=12, column=0, columnspan=2)

        # Add New Search Button to clear search fields
        tk.Button(root, text="New Search", command=self.clear_search_fields).grid(row=13, column=0, columnspan=2)

        # Display area for pet information
        self.text_area = tk.Text(root, wrap="word", height=10, width=50)
        self.text_area.grid(row=14, column=0, columnspan=2)

        # Image display area for showing multiple images
        self.image_labels = []  # A list for dynamically displaying image labels
        for i in range(3):  # Assume up to 3 pets' images are shown
            label = tk.Label(root)
            label.grid(row=15 + i, column=0, columnspan=2)
            self.image_labels.append(label)

        self.photo_data = None  # Used to store selected photo data

    def choose_photo(self):
        # Choose a pet photo file
        file_path = filedialog.askopenfilename(
            title="Choose a Photo",
            filetypes=(("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*"))
        )
        if file_path:
            self.photo_path_label.config(text=f"Selected: {file_path}")
            with open(file_path, "rb") as file:
                self.photo_data = file.read()  # Read the binary data of the image
        else:
            self.photo_path_label.config(text="No photo selected")
            self.photo_data = None

    def register_pet(self):
        name = self.name_entry.get()
        gender = self.gender_var.get()  # Get the gender from the selection box
        age = self.age_entry.get()
        breed = self.breed_entry.get()

        # Validate that the age is an integer
        if not age.isdigit():
            messagebox.showwarning("Warning", "Age must be an integer!")
            return

        if self.photo_data is None:
            messagebox.showwarning("Warning", "Please choose a photo for the pet!")
            return

        pet = pet_adoption_pb2.PetInfo(name=name, gender=gender, age=int(age), breed=breed, picture=self.photo_data)
        response = self.stub.RegisterPet(pet)
        messagebox.showinfo("Server Response", response.message)

    def search_pet(self):
        search_key = self.search_key.get()  # Get the search keyword chosen by the user

        if search_key == "gender":
            search_value = self.search_value_var.get()  # If searching by gender, get the value from the selection box
        else:
            search_value = self.search_entry.get()  # Otherwise, get the value from the text input

        # If searching by age, validate that the input is an integer
        if search_key == "age" and not search_value.isdigit():
            messagebox.showwarning("Warning", "Age must be an integer for search!")
            return

        if not search_value:
            messagebox.showwarning("Warning", "Please enter a search value!")
            return

        # Create a search request, specifying the key and value
        search_request = pet_adoption_pb2.SearchRequest(key=search_key, value=search_value)
        search_response = self.stub.SearchPet(search_request)

        # Clear the text area and image labels
        self.text_area.delete(1.0, tk.END)
        for label in self.image_labels:
            label.config(image='')

        if search_response.pets:
            # Iterate through all matching pets and display their information
            for idx, pet in enumerate(search_response.pets):
                pet_info = f"Name: {pet.name}\nBreed: {pet.breed}\nAge: {pet.age}\nGender: {pet.gender}\n\n"
                self.text_area.insert(tk.END, pet_info)

                # Display up to 3 pet images
                if idx < len(self.image_labels) and pet.picture:
                    # Load the image using Pillow
                    image = Image.open(io.BytesIO(pet.picture))
                    image = image.resize((100, 100))  # Resize the image to fit the interface
                    photo = ImageTk.PhotoImage(image)

                    # Update the image display
                    self.image_labels[idx].config(image=photo)
                    self.image_labels[idx].image = photo  # Save a reference to prevent garbage collection

        else:
            messagebox.showinfo("Search Results", "No pets found")

    def update_search_field(self, selected_key):
        """Update the search input field type based on the selected search key"""
        # If searching by gender, replace the text input with a selection box
        if selected_key == "gender":
            self.search_value_var = tk.StringVar(self.root)
            self.search_value_var.set("Male")  # Default selection is Male
            self.search_entry.grid_forget()  # Remove the text input field
            self.search_menu = tk.OptionMenu(self.root, self.search_value_var, "Male", "Female")
            self.search_menu.grid(row=11, column=1)
        else:
            # For other search keys, revert to a text input field
            self.search_menu.grid_forget()  # Remove the gender selection box
            self.search_entry = tk.Entry(self.root)
            self.search_entry.grid(row=11, column=1)

    def clear_registration_form(self):
        """Clear all fields in the registration form and the selected image"""
        self.name_entry.delete(0, tk.END)
        self.gender_var.set("Male")  # Reset gender to Male
        self.age_entry.delete(0, tk.END)
        self.breed_entry.delete(0, tk.END)
        self.photo_path_label.config(text="No photo selected")
        self.photo_data = None

    def clear_search_fields(self):
        """Clear the search fields, text area, and displayed images"""
        self.search_entry.delete(0, tk.END)
        self.text_area.delete(1.0, tk.END)
        for label in self.image_labels:
            label.config(image='')


if __name__ == '__main__':
    root = tk.Tk()
    app = PetAdoptionClient(root)
    root.mainloop()
