import grpc  # Import the gRPC library to enable client-server communication.
import pet_adoption_pb2  # Import the generated gRPC classes for PetAdoption service messages.
import pet_adoption_pb2_grpc  # Import the generated gRPC classes for the PetAdoption service.


class PetAdoptionClient:
    def __init__(self):
        # Constructor: Initializes the client by setting up a connection to the gRPC server.
        # Connect to the server using an insecure channel (no encryption).
        self.channel = grpc.insecure_channel('grpc-pet-adoption-server:50051')
        # Create a stub (client) to interact with the server's PetAdoptionService.
        self.stub = pet_adoption_pb2_grpc.PetAdoptionServiceStub(self.channel)

    def register_pet(self, name, gender, age, breed, photo_path):
        """
        Registers a new pet with the server.

        Parameters:
        - name (str): The name of the pet.
        - gender (str): The gender of the pet, must be 'Male' or 'Female'.
        - age (int): The age of the pet.
        - breed (str): The breed of the pet.
        - photo_path (str): The file path of the pet's photo.

        Returns:
        - Prints a message with the server response if successful.
        - If any input validation fails, an error message is printed, and registration does not proceed.
        """

        # Check if the name is provided.
        if not name:
            print("Pet name is required!")
            return

        # Check if gender is provided and valid.
        if not gender or gender not in ["Male", "Female"]:
            print("Pet gender must be 'Male' or 'Female'!")
            return

        # Check if age is provided.
        if not age:
            print("Pet age is required!")
            return

        # Check if breed is provided.
        if not breed:
            print("Pet breed is required!")
            return

        # Check if photo path is provided.
        if not photo_path:
            print("Photo path is required!")
            return

        try:
            # Ensure age is an integer.
            age = int(age)
        except ValueError:
            print("Age must be an integer!")
            return

        try:
            # Open and read the pet photo as binary data.
            with open(photo_path, "rb") as file:
                photo_data = file.read()
        except FileNotFoundError:
            # If the photo file doesn't exist, print an error and return.
            print(f"Photo file not found at {photo_path}. Please provide a valid file path.")
            return

        # Create a PetInfo message with the pet's details.
        pet = pet_adoption_pb2.PetInfo(name=name, gender=gender, age=age, breed=breed, picture=photo_data)

        # Send the RegisterPet request to the server and get the response.
        response = self.stub.RegisterPet(pet)

        # Print the server's response message.
        print("Server Response:", response.message)

    def search_pet(self, search_key, search_value):
        """
        Searches for pets on the server using a specified search criterion.

        Parameters:
        - search_key (str): The field to search by (e.g., 'name', 'gender', 'age', or 'breed').
        - search_value (str): The value to search for in the specified field.

        Returns:
        - Prints details of the matching pets found by the server, or a message if no pets are found.
        """

        # Check if the search value is provided.
        if not search_value:
            print(f"{search_key.capitalize()} is required for search!")
            return

        # If searching by age, ensure that the age is a valid integer.
        if search_key == "age":
            try:
                search_value = str(int(search_value))
            except ValueError:
                print("Age must be an integer for search!")
                return

        # Create a SearchRequest message with the search criteria.
        search_request = pet_adoption_pb2.SearchRequest(key=search_key, value=search_value)

        # Send the SearchPet request to the server and get the response.
        search_response = self.stub.SearchPet(search_request)

        # If pets are found, print their details.
        if search_response.pets:
            for pet in search_response.pets:
                print(f"Name: {pet.name}, Breed: {pet.breed}, Age: {pet.age}, Gender: {pet.gender}")
        else:
            # If no pets are found, print a message.
            print("No pets found.")


# The main logic for the user interface of the Pet Adoption System.
if __name__ == '__main__':
    # Create a client instance to interact with the PetAdoption service.
    client = PetAdoptionClient()

    while True:
        # Display menu options to the user.
        print("\n--- Pet Adoption System ---")
        print("1. Register a Pet")
        print("2. Search for a Pet")
        print("3. Exit")

        # Get the user's choice.
        choice = input("Choose an option: ")

        if choice == '1':
            # If the user chooses to register a pet, collect the pet's information.
            name = input("Enter pet name: ")
            gender = input("Enter pet gender (Male/Female): ")
            age = input("Enter pet age: ")
            breed = input("Enter pet breed: ")
            photo_path = input("Enter path to pet's photo: ")

            # Register the pet using the collected information.
            client.register_pet(name, gender, age, breed, photo_path)

        elif choice == '2':
            # If the user chooses to search for a pet, display search options.
            print("Search by:")
            print("1. Name")
            print("2. Gender")
            print("3. Age")
            print("4. Breed")

            # Get the user's search criteria.
            search_option = input("Choose an option: ")
            search_key_map = {'1': 'name', '2': 'gender', '3': 'age', '4': 'breed'}
            search_key = search_key_map.get(search_option)

            if search_key:
                # Get the search value from the user.
                search_value = input(f"Enter {search_key}: ")

                # Search for pets using the provided criteria.
                client.search_pet(search_key, search_value)
            else:
                # If the user selects an invalid option, print an error message.
                print("Invalid option.")

        elif choice == '3':
            # Exit the program if the user chooses to.
            break

        else:
            # If the user enters an invalid menu option, print an error message.
            print("Invalid choice, please try again.")
