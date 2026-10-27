from .models import CarMake, CarModel


def initiate():
    """
    Populate the database with car makes and models.

    Existing records are reused instead of duplicated.
    """

    car_make_data = [
        {
            "name": "NISSAN",
            "description": "Great cars. Japanese technology"
        },
        {
            "name": "Mercedes",
            "description": "Great cars. German technology"
        },
        {
            "name": "Audi",
            "description": "Great cars. German technology"
        },
        {
            "name": "Kia",
            "description": "Great cars. Korean technology"
        },
        {
            "name": "Toyota",
            "description": "Great cars. Japanese technology"
        },
    ]

    # Create or retrieve car makes.
    car_make_instances = {}

    for data in car_make_data:
        make, created = CarMake.objects.get_or_create(
            name=data["name"],
            defaults={
                "description": data["description"]
            }
        )

        car_make_instances[data["name"]] = make

        if created:
            print(f"Created car make: {make.name}")
        else:
            print(f"Car make already exists: {make.name}")

    # Car model data.
    car_model_data = [
        {
            "name": "Pathfinder",
            "type": "SUV",
            "year": 2023,
            "car_make": "NISSAN"
        },
        {
            "name": "Qashqai",
            "type": "SUV",
            "year": 2023,
            "car_make": "NISSAN"
        },
        {
            "name": "XTRAIL",
            "type": "SUV",
            "year": 2023,
            "car_make": "NISSAN"
        },
        {
            "name": "A-Class",
            "type": "SUV",
            "year": 2023,
            "car_make": "Mercedes"
        },
        {
            "name": "C-Class",
            "type": "SUV",
            "year": 2023,
            "car_make": "Mercedes"
        },
        {
            "name": "E-Class",
            "type": "SUV",
            "year": 2023,
            "car_make": "Mercedes"
        },
        {
            "name": "A4",
            "type": "SUV",
            "year": 2023,
            "car_make": "Audi"
        },
        {
            "name": "A5",
            "type": "SUV",
            "year": 2023,
            "car_make": "Audi"
        },
        {
            "name": "A6",
            "type": "SUV",
            "year": 2023,
            "car_make": "Audi"
        },
        {
            "name": "Sorrento",
            "type": "SUV",
            "year": 2023,
            "car_make": "Kia"
        },
        {
            "name": "Carnival",
            "type": "SUV",
            "year": 2023,
            "car_make": "Kia"
        },
        {
            "name": "Cerato",
            "type": "SEDAN",
            "year": 2023,
            "car_make": "Kia"
        },
        {
            "name": "Corolla",
            "type": "SEDAN",
            "year": 2023,
            "car_make": "Toyota"
        },
        {
            "name": "Camry",
            "type": "SEDAN",
            "year": 2023,
            "car_make": "Toyota"
        },
        {
            "name": "Kluger",
            "type": "SUV",
            "year": 2023,
            "car_make": "Toyota"
        },
    ]

    # Create or retrieve car models.
    for data in car_model_data:
        make = car_make_instances[data["car_make"]]

        model, created = CarModel.objects.get_or_create(
            car_make=make,
            name=data["name"],
            defaults={
                "dealer_id": 0,
                "type": data["type"],
                "year": data["year"]
            }
        )

        if created:
            print(f"Created car model: {make.name} {model.name}")
        else:
            print(f"Car model already exists: {make.name} {model.name}")

    print("Car database population completed.")