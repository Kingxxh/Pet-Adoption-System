import grpc
import pet_adoption_pb2
import pet_adoption_pb2_grpc

class PetAdoptionClient:
    def __init__(self):
        # Server connection
        self.channel = grpc.insecure_channel('grpc-pet-adoption-server:50051')
        self.stub = pet_adoption_pb2_grpc.PetAdoptionServiceStub(self.channel)

    def register_pet(self, name, gender, age, breed, photo_path):
        # Check if fields are empty
        if not name:
            print("Pet name is required!")
            return
        if not gender or gender not in ["Male", "Female"]:
            print("Pet gender must be 'Male' or 'Female'!")
            return
        if not age:
            print("Pet age is required!")
            return
        if not breed:
            print("Pet breed is required!")
            return
        if not photo_path:
            print("Photo path is required!")
            return

        try:
            age = int(age)  # Check if age is an integer
        except ValueError:
            print("Age must be an integer!")
            return

        try:
            with open(photo_path, "rb") as file:
                photo_data = file.read()  # Read the binary data of the image
        except FileNotFoundError:
            print(f"Photo file not found at {photo_path}. Please provide a valid file path.")
            return

        pet = pet_adoption_pb2.PetInfo(name=name, gender=gender, age=age, breed=breed, picture=photo_data)
        response = self.stub.RegisterPet(pet)
        print("Server Response:", response.message)

    def search_pet(self, search_key, search_value):
        if not search_value:
            print(f"{search_key.capitalize()} is required for search!")
            return

        if search_key == "age":
            try:
                search_value = str(int(search_value))  # Ensure the age is an integer
            except ValueError:
                print("Age must be an integer for search!")
                return

        search_request = pet_adoption_pb2.SearchRequest(key=search_key, value=search_value)
        search_response = self.stub.SearchPet(search_request)

        if search_response.pets:
            for pet in search_response.pets:
                print(f"Name: {pet.name}, Breed: {pet.breed}, Age: {pet.age}, Gender: {pet.gender}")
        else:
            print("No pets found.")

if __name__ == '__main__':
    client = PetAdoptionClient()

    while True:
        print("\n--- Pet Adoption System ---")
        print("1. Register a Pet")
        print("2. Search for a Pet")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter pet name: ")
            gender = input("Enter pet gender (Male/Female): ")
            age = input("Enter pet age: ")
            breed = input("Enter pet breed: ")
            photo_path = input("Enter path to pet's photo: ")
            client.register_pet(name, gender, age, breed, photo_path)

        elif choice == '2':
            print("Search by:")
            print("1. Name")
            print("2. Gender")
            print("3. Age")
            print("4. Breed")
            search_option = input("Choose an option: ")
            search_key_map = {'1': 'name', '2': 'gender', '3': 'age', '4': 'breed'}
            search_key = search_key_map.get(search_option)
            if search_key:
                search_value = input(f"Enter {search_key}: ")
                client.search_pet(search_key, search_value)
            else:
                print("Invalid option.")

        elif choice == '3':
            break

        else:
            print("Invalid choice, please try again.")
