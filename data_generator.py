from datetime import timedelta
import requests
import random
import json
from faker import Faker

BASE_URL = "http://localhost:5000"
EMAIL = ""
PASSWORD = ""
fake = Faker()


def get_access_token(email, password):
    response = requests.get(f"{BASE_URL}/authentication/get_access_token", params={'email': email, 'password': password})
    
    if response.status_code == 200:
        # Si el token viene en texto plano, puedes retornarlo directamente
        return response.text.strip().strip('"')

    else:
        print(f"Authentication failed with status code {response.status_code}")
        return None

def post_response(endpoint, token=None, data=None):
    headers = {'Content-Type': 'application/json'}

    if token:
        headers['Authorization'] = f'Bearer {token}'

    response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, data=json.dumps(data))

    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        print(f"Request to {endpoint} failed with status code {response.status_code}")
        return None



def generate_payload_agri_farm():
    points = [f"{round(random.uniform(0, 101), 2)},{round(random.uniform(0, 1), 2)}" for _ in range(4)]
    points.append(points[0])

    return {
        "name": fake.bs(),
        "location": f"{round(random.uniform(0, 101), 2)},{round(random.uniform(0, 1), 2)}",
        "type_location": "Point",
        "address_locality": fake.city(),
        "address_country": fake.country_code(),
        "address_street": fake.street_address(),
        "contact_point_telephone": fake.phone_number(),
        "contact_point_email": fake.email(),
        "has_building": ','.join([f"urn:ngsi-ld:Building:{fake.uuid4()}" for _ in range(3)]),
        "has_agri_parcel": ','.join([f"urn:ngsi-ld:AgriParcel:{fake.uuid4()}" for _ in range(3)]),
        "date_created": fake.date_time_this_decade().isoformat(),
        "date_modified": fake.date_time_this_year().isoformat(),
        "description": fake.sentence(),
        "related_source": ','.join([f"urn:ngsi-ld:AgriApp:{fake.uuid4()}" for _ in range(2)]),
        "see_also": f"https://example.org/concept/farm,https://datamodel.org/example/farm,https://datamodel.org/example/field",
        "land_location": ';'.join(points),
        "land_location_type": "Polygon",
        "owned_by": f"urn:ngsi-ld:Person:{fake.uuid4()}"
    }


def generate_payload_agri_crop():
    return {
        "date_created": fake.date_time_this_decade().isoformat(),
        "date_modified": fake.date_time_this_year().isoformat(),
        "name": "Wheat",
        "alternate_name": "Triticum aestivum",
        "agro_voc_concept": "http://aims.fao.org/aos/agrovoc/c_7951",
        "see_also": "https://example.org/concept/wheat,https://datamodel.org/example/wheat",
        "description": "Spring wheat",
        "related_source": f"urn:ngsi-ld:AgriApp:{fake.uuid4()};app:weat",
        "has_agri_soil": ','.join([f"urn:ngsi-ld:AgriSoil:{fake.uuid4()}" for _ in range(2)]),
        "has_agri_fertiliser": ','.join([f"urn:ngsi-ld:AgriFertiliser:{fake.uuid4()}" for _ in range(2)]),
        "has_agri_pest": ','.join([f"urn:ngsi-ld:AgriPest:{fake.uuid4()}" for _ in range(2)]),
        "planting_from": json.dumps([{"dateRange": "-09-28/-10-12", "description": "Best Season"}]),
        "harvesting_interval": json.dumps([{"dateRange": "-09-28/-10-12", "description": "Best Season"}]),
        "watering_frequency": "daily"
    }


def generate_payload_agri_greenhouse():
    return {
        "relative_humidity": random.uniform(30.0, 50.0),
        "co2": random.uniform(350.0, 500.0),
        "date_created": fake.date_time_this_decade().isoformat(),
        "date_modified": fake.date_time_this_year().isoformat(),
        "owned_by": f"urn:ngsi-ld:Person:{fake.uuid4()}",
        "related_source": ','.join([f"urn:ngsi-ld:AgriApp:{fake.uuid4()}" for _ in range(2)]),
        "see_also": "https://example.org/concept/greenhouse,https://datamodel.org/example/greenhouse",
        "belongs_to": f"urn:ngsi-ld:AgriFarm:{fake.uuid4()}",
        "has_agri_parcel_parent": f"urn:ngsi-ld:AgriParcel:{fake.uuid4()}",
        "has_agri_parcel_children": ','.join([f"urn:ngsi-ld:AgriParcel:{fake.uuid4()}" for _ in range(2)]),
        "has_weather_observed": f"urn:ngsi-ld:WeatherObserved:{fake.uuid4()}",
        "has_water_quality_observed": ','.join([f"urn:ngsi-ld:WaterQualityObserved:{fake.uuid4()}" for _ in range(2)]),
        "leaf_temperature": random.uniform(20.0, 30.0),
        "daily_light": random.uniform(500.0, 1500.0),
        "drain_flow": random.uniform(5.0, 15.0),
        "has_device": ','.join([f"urn:ngsi-ld:Device:{fake.uuid4()}" for _ in range(2)])
    }


def generate_payload_agri_parcel():
    points = [f"{round(random.uniform(0, 101), 2)},{round(random.uniform(0, 1), 2)}" for _ in range(4)]
    points.append(points[0])
    return {
        "date_created": fake.date_time_this_decade().isoformat(),
        "date_modified": fake.date_time_this_year().isoformat(),
        "location": ';'.join(points),
        "location_type": "Polygon",
        "area": random.uniform(100.0, 500.0),
        "description": random.choice(["Spring wheat", "Winter wheat", "Corn", "Soybean"]),
        "category": random.choice(["arable", "permanent"]),
        "belongs_to": f"urn:ngsi-ld:AgriFarm:{fake.uuid4()}",
        "owned_by": f"urn:ngsi-ld:Person:{fake.uuid4()}",
        "has_agri_parcel_parent": f"urn:ngsi-ld:AgriParcel:{fake.uuid4()}",
        "has_agri_parcel_children": ','.join([f"urn:ngsi-ld:AgriParcel:{fake.uuid4()}" for _ in range(2)]),
        "has_agri_crop": f"urn:ngsi-ld:AgriCrop:{fake.uuid4()}",
        "has_air_quality_observed": f"urn:ngsi-ld:AirQualityObserved:{fake.uuid4()}",
        "crop_status": random.choice(["seeded", "harvested", "growing"]),
        "last_planted_at": fake.date_time_this_year().isoformat(),
        "has_agri_soil": f"urn:ngsi-ld:AgriSoil:{fake.uuid4()}",
        "has_device": ','.join([f"urn:ngsi-ld:Device:{fake.uuid4()}" for _ in range(2)]),
        "soil_texture_type": random.choice(["Clay", "Loam", "Sand"]),
        "irrigation_system_type": random.choice(["Drip irrigation", "Furrow irrigation", "Sprinkler irrigation"]),
        "related_source": ','.join([f"urn:ngsi-ld:AgriApp:{fake.uuid4()}" for _ in range(2)]),
        "see_also": "https://example.org/concept/agriparcel,https://datamodel.org/example/agriparcel"
    }


def generate_payload_agri_parcel_operation():
    return {
        "date_created": fake.date_time_this_decade().isoformat(),
        "date_modified": fake.date_time_this_year().isoformat(),
        "related_source": ','.join([f"urn:ngsi-ld:AgriApp:{fake.uuid4()}" for _ in range(2)]),
        "see_also": "https://example.org/concept/agriparcelop,https://datamodel.org/example/agriparcelop",
        "has_agri_parcel": f"urn:ngsi-ld:AgriParcel:{fake.uuid4()}",
        "operation_type": random.choice(["fertiliser", "irrigation", "pesticide"]),
        "description": "Monthly operation application",
        "result": random.choice(["ok", "failed", "pending"]),
        "planned_start_at": fake.date_time_this_year().isoformat(),
        "planned_end_at": fake.date_time_this_year().isoformat(),
        "status": random.choice(["planned", "in progress", "finished"]),
        "has_operator": f"urn:ngsi-ld:Person:{fake.uuid4()}",
        "started_at": fake.date_time_this_year().isoformat(),
        "ended_at": fake.date_time_this_year().isoformat(),
        "reported_at": fake.date_time_this_year().isoformat(),
        "has_agri_product_type": f"urn:ngsi-ld:AgriProductType:{fake.uuid4()}",
        "quantity": random.uniform(20.0, 100.0),
        "water_source": random.choice(["rainwater capture", "well", "river"]),
        "work_order": "https://example.com/agriparcelrecords/workorder1",
        "work_record": "https://example.com/agriparcelrecords/workrecord1",
        "irrigation_record": "https://example.com/agriparcelrecords/irrigationrecord1",
        "diesel_fuel_consumption": random.uniform(20.0, 50.0),
        "gasoline_fuel_consumption": random.uniform(20.0, 50.0),
        "diesel_fuel_consumption_max_value": 50.0,
        "diesel_fuel_consumption_min_value": 20.0,
        "diesel_fuel_consumption_unit_text": "liters",
        "gasoline_fuel_consumption_max_value": 50.0,
        "gasoline_fuel_consumption_min_value": 20.0,
        "gasoline_fuel_consumption_unit_text": "liters"
    }

def generate_payload_agri_parcel_record():
    points = [f"{round(random.uniform(0, 101), 2)},{round(random.uniform(0, 1), 2)}" for _ in range(4)]
    points.append(points[0])
    return {
        "date_created": fake.date_time_this_decade().isoformat(),
        "date_modified": fake.date_time_this_year().isoformat(),
        "has_agri_parcel": f"urn:ngsi-ld:AgriParcel:{fake.uuid4()}",
        "type_location": "Polygon",
        "location": ';'.join(points),
        "soil_temperature_unit": "CEL",
        "soil_temperature": random.uniform(0.0, 30.0),
        "air_temperature_unit": "CEL",
        "air_temperature_timestamp": fake.date_time_this_year().isoformat(),
        "air_temperature": random.uniform(0.0, 40.0),
        "relative_humidity": random.uniform(0.0, 100.0),
        "relative_humidity_unit": "P1",
        "relative_humidity_timestamp": fake.date_time_this_year().isoformat(),
        "description": "Soil and weather conditions",
        "related_source": ','.join([f"urn:ngsi-ld:AgriApp:{fake.uuid4()}" for _ in range(2)]),
        "see_also": "https://example.org/concept/agriparcelrecord,https://example.org/concept/agriparcelrecord2",
        "soil_moisture_vwc": random.uniform(0.0, 1.0),
        "soil_moisture_ec": random.uniform(0.0, 1.0),
        "soil_salinity": random.uniform(0.0, 1.0),
        "leaf_wetness": random.uniform(0.0, 1.0),
        "leaf_relative_humidity": random.uniform(0.0, 100.0),
        "leaf_relative_humidity_unit": "P1",
        "leaf_relative_humidity_timestamp": fake.date_time_this_year().isoformat(),
        "leaf_temperature": random.uniform(0.0, 30.0),
        "solar_radiation": random.uniform(500.0, 1500.0),
        "atmospheric_pressure": random.uniform(950.0, 1050.0),
        "has_device": ','.join([f"urn:ngsi-ld:Device:{fake.uuid4()}" for _ in range(2)]),
        "observed_at": fake.date_time_this_year().isoformat(),
        "soil_salinity_unit": "D10",
        "soil_salinity_timestamp": fake.date_time_this_year().isoformat(),
        "leaf_wetness_unit": "P1",
        "leaf_wetness_timestamp": fake.date_time_this_year().isoformat(),
        "leaf_temperature_unit": "CEL",
        "leaf_temperature_timestamp": fake.date_time_this_year().isoformat(),
        "solar_radiation_unit": "CEL",
        "solar_radiation_timestamp": fake.date_time_this_year().isoformat(),
        "atmospheric_pressure_unit": "A97",
        "atmospheric_pressure_timestamp": fake.date_time_this_year().isoformat(),
        "soil_moisture_vwc_unit": "C62",
        "soil_moisture_vwc_timestamp": fake.date_time_this_year().isoformat(),
        "soil_moisture_ec_unit": "D10",
        "soil_moisture_ec_timestamp": fake.date_time_this_year().isoformat(),
        "depth": random.uniform(0.0, 50.0),
        "depth_unit_code": "CMT",
        "timestamp": fake.date_time_this_year().isoformat(),
    }

def generate_payload_agri_soil():
    return {
        "date_created": fake.date_time_this_decade().isoformat(),
        "date_modified": fake.date_time_this_year().isoformat(),
        "name": fake.word(),
        "alternate_name": fake.word(),
        "description": fake.sentence(),
        "agro_voc_concept": f"http://aims.fao.org/aos/agrovoc/c_{random.randint(1000, 9999)}",
        "see_also": "https://example.org/concept/clay",
        "related_source": ','.join([f"urn:ngsi-ld:AgriApp:{fake.uuid4()}" for _ in range(2)]),
        "has_agri_product_type": ','.join([f"urn:ngsi-ld:AgriProductType:{fake.uuid4()}" for _ in range(2)])
    }


def generate_payload_agri_soil_state():
    return {
        "date_created": fake.date_time_this_decade().isoformat(),
        "date_modified": fake.date_time_this_year().isoformat(),
        "date_of_measurement": fake.date_time_this_month().isoformat(),
        "acidity": round(random.uniform(0, 14), 2),
        "acidity_unit_code": 'pH',
        "acidity_timestamp": fake.date_time_this_month().isoformat(),
        "electrical_conductivity": round(random.uniform(0, 1), 2),
        "electrical_conductivity_unit": 'ohm/meter',
        "electrical_conductivity_timestamp": fake.date_time_this_month().isoformat(),
        "density": round(random.uniform(0, 20), 2),
        "density_unit": 'kg/m3',
        "density_timestamp": fake.date_time_this_month().isoformat(),
        "humus": round(random.uniform(0, 10), 2),
        "humus_unit_code": 'percent',
        "humus_timestamp": fake.date_time_this_month().isoformat(),
        "has_agri_soil": f"urn:ngsi-ld:AgriSoil:{fake.uuid4()}",
        "has_agri_parcel": f"urn:ngsi-ld:AgriParcel:{fake.uuid4()}",
        "has_agri_greenhouse": f"urn:ngsi-ld:AgriGreenhouse:{fake.uuid4()}",
    }

def generate_payload_agri_yield():
    start_date = fake.date_time_this_year()
    end_date = start_date + timedelta(days=random.randint(30,120))  # A random end date 30 to 120 days after the start
    yield_value = round(random.uniform(20, 100), 2)
    yield_min_value = round(yield_value - random.uniform(0, 10), 2)
    yield_max_value = round(yield_value + random.uniform(0, 10), 2)

    return {
        "has_agri_crop": f"urn:ngsi-ld:AgriCrop:{fake.uuid4()}",
        "has_agri_parcel": f"urn:ngsi-ld:AgriParcel:{fake.uuid4()}",
        "start_date_of_gathering_at": start_date.isoformat(),
        "end_date_of_gathering_at": end_date.isoformat(),
        "yield_value": yield_value,
        "yield_max_value": yield_max_value,
        "yield_min_value": yield_min_value,
        "yield_unit_text": 'Tons per hectare',
    }


def generate_payload_agri_carbon_footprint():
    estimation_start = fake.date_time_this_year()
    estimation_end = estimation_start + timedelta(days=random.randint(30,120))  # A random end date 30 to 120 days after the start
    carbon_footprint_value = round(random.uniform(1, 20), 2)
    carbon_footprint_accuracy_percent = round(random.uniform(1, 20), 2)
    carbon_footprint_min_value = round(carbon_footprint_value - random.uniform(0, 5), 2)

    return {
        "has_agri_crop": f"urn:ngsi-ld:AgriCrop:{fake.uuid4()}",
        "has_agri_parcel": f"urn:ngsi-ld:AgriParcel:{fake.uuid4()}",
        "has_agri_yield": f"urn:ngsi-ld:AgriYield:{fake.uuid4()}",
        "carbon_footprint_value": carbon_footprint_value,
        "carbon_footprint_accuracy_percent": carbon_footprint_accuracy_percent,
        "carbon_footprint_min_value": carbon_footprint_min_value,
        "carbon_footprint_unit_text": 'Tons',
        "estimation_start_at": estimation_start.isoformat(),
        "estimation_end_at": estimation_end.isoformat(),
    }


token = get_access_token(EMAIL, PASSWORD)


'''agri_farm = generate_payload_agri_farm()
agri_farm_response = post_response("/api/agri-farm", token=token, data=agri_farm)
print(agri_farm_response)


agri_crop = generate_payload_agri_crop()
agri_crop_response = post_response("/api/agri_crop", token=token, data=agri_crop)
print(agri_crop_response)

agri_greenhouse = generate_payload_agri_greenhouse()
agri_greenhouse_response = post_response("/api/agri_green_house", token=token, data=agri_greenhouse)
print(agri_greenhouse_response)


agri_parcel = generate_payload_agri_parcel()
agri_parcel_response = post_response("/api/agri_parcel", token=token, data=agri_parcel)
print(agri_parcel_response)

agri_parcel_operation = generate_payload_agri_parcel_operation()
agri_parcel_operation_response = post_response("/api/agri_parcel_operation", token=token, data=agri_parcel_operation)
print(agri_parcel_operation_response)

agri_parcel_record = generate_payload_agri_parcel_record()
agri_parcel_record_response = post_response("/api/agri_parcel_record", token=token, data=agri_parcel_record)
print(agri_parcel_record_response)

agri_soil = generate_payload_agri_soil()
agri_soil_response = post_response("/api/agri_soil", token=token, data=agri_soil)
print(agri_soil_response)

agri_soil_state = generate_payload_agri_soil_state()
agri_soil_state_response = post_response("/api/agri_soil_state", token=token, data=agri_soil_state)
print(agri_soil_state_response)

agri_yield = generate_payload_agri_yield()
agri_yield_response = post_response("/api/agri_yield", token=token, data=agri_yield)
print(agri_yield_response)'''

agri_carbon_footprint = generate_payload_agri_carbon_footprint()
agri_carbon_footprint_response = post_response("/api/agri_carbon_footprint", token=token, data=agri_carbon_footprint)
print(agri_carbon_footprint_response)
