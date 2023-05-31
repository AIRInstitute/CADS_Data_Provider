from json import loads
import logging
from flask import Blueprint, request, jsonify
from app.config import AUTHORIZATIONS
from app.smart_data_models.agri_carbon_footprint import AgriCarbonFootPrint
from app.smart_data_models.agri_crop import AgriCrop
from app.smart_data_models.agri_farm import AgriFarm
from app.smart_data_models.agri_greenhouse import AgriGreenHouse
from app.smart_data_models.agri_parcel import AgriParcel
from app.smart_data_models.agri_parcel_operation import AgriParcelOperation
from app.smart_data_models.agri_parcel_record import AgriParcelRecord
from app.smart_data_models.agri_soil import AgriSoil
from app.smart_data_models.agri_soil_state import AgriSoilState
from app.smart_data_models.agri_yield import AgriYield
from app.utils import api_key_required, send_to_context_broker
from flask_restx import Namespace, Resource, fields
from app import RelationshipField

smartdata_blueprint = Blueprint("smart_data", __name__)

ns_smart_data_models = Namespace('smart_data_models', description='Smart Data Models operations', authorizations=AUTHORIZATIONS, security='Bearer Auth')

def get_namespaces():
    return [ns_smart_data_models] 

def get_models():
    return {'AgriFarm': agri_farm_model,
            'AgriCrop':agri_crop_model,
            'AgriGreenHouse': agri_greenhouse_model,
            'AgriParcel': agri_parcel_model,
            'AgriParcelOperation': agri_parcel_operation_model,
            'AgriParcelRecord': agri_parcel_record_model,
            'AgriSoil': agri_soil_model,
            'AgriSoilState': agri_soil_state_model,
            'AgriYield': agri_yield_model,
            'AgriCarbonFootprint': agri_carbon_footprint_model}

agri_farm_model = ns_smart_data_models.model('AgriFarm', {
    'name': fields.String(required=True, description='Name of the farm', example="Wheat farm"),
    'location': fields.String(required=True, description='Location of the farm', example="101,0"),
    'type_location': fields.String(required=True, description='Type location of the farm', example="Point"),
    'address_locality': fields.String(required=True, description='Locality of the farm', example="Valdepeñas"),
    'address_country': fields.String(required=True, description='Country of the farm', example="ES"),
    'address_street': fields.String(required=True, description='Street address of the farm', example="Camino de Membrilla 17"),
    'contact_point_telephone': fields.String(required=True, description='Contact phone number', example="00349674532"),
    'contact_point_email': fields.String(required=True, description='Contact email', example="wheatfarm@email.com"),
    'has_building': fields.String(required=False, description='Related buildings', example="urn:ngsi-ld:Building:32bbf1f4-8c67-4b5d-b19b-392879f72015,urn:ngsi-ld:Building:32bbf1f4-8c67-4b5d-b19b-392879f72035,urn:ngsi-ld:Building:35aa1f5f-7c78-4b7c-afc3-392d74f6b014"),
    'has_agri_parcel': fields.String(required=True, description='Related agricultural parcels', example="urn:ngsi-ld:AgriParcel:26ba4be0-4474-11e8-8ec1-ab9e0ea93835,urn:ngsi-ld:AgriParcel:2d5b8874-4474-11e8-8d6b-dbe14425b5e4,urn:ngsi-ld:AgriParcel:3f8b7982-4458-11e8-9ea6-db304564e5e6"),
    'date_created': fields.DateTime(description='Date created', example="2017-01-01T01:20:00Z"),
    'date_modified': fields.DateTime(description='Date modified', example="2017-05-04T12:30:00Z"),
    'description': fields.String(description='Description of the farm', example="A farm producing wheat"),
    'related_source': fields.String(description='Related source', example="urn:ngsi-ld:AgriApp:72551db2-91d1-43c3-8534-10f1044f7d98,urn:ngsi-ld:AgriApp:23564dsf-13ds-43d4-9734-10a124gds7d98"),
    'see_also': fields.String(description='Additional resources', example="https://example.org/concept/farm,https://datamodel.org/example/farm,https://datamodel.org/example/field"),
    'land_location': fields.String(description='Land location', example="100,0;101,0;101,1;100,1;100,0"),
    'land_location_type': fields.String(required=True, description='Type location of the land', example="Polygon"),
    'owned_by': fields.String(description='Owner', example="urn:ngsi-ld:Person:430a3f2a-3434-49d1-a212-2f30a9824d99"),
})


@ns_smart_data_models.doc(security='Bearer Auth')
@ns_smart_data_models.route('/agri-farm')
class AgriFarmResource(Resource):
    @api_key_required
    @ns_smart_data_models.expect(agri_farm_model, validate=True)
    @ns_smart_data_models.response(201, 'AgriFarm successfully created.')
    def post(self):
        farm_data = request.get_json()
        name = farm_data.get('name')
        location_str = farm_data.get('location')
        type_location = farm_data.get('type_location')
        address_locality = farm_data.get('address_locality')
        address_country = farm_data.get('address_country')
        address_street = farm_data.get('address_street')
        contact_point_telephone = farm_data.get('contact_point_telephone')
        contact_point_email = farm_data.get('contact_point_email')
        has_building_str = farm_data.get('has_building')
        has_agri_parcel_str = farm_data.get('has_agri_parcel')
        see_also_str = farm_data.get('see_also')
        land_location_str = farm_data.get('land_location')
        land_location_type = farm_data.get('land_location_type')

        error_messages = []
        if not name:
            logging.info("name")
            error_messages.append("Name is missing")
        if not location_str:
            logging.info("location")
            error_messages.append("Location is missing")
        if not type_location:
            logging.info("type location")
            error_messages.append("Location type is missing")
        if not address_locality:
            logging.info("address_locality")
            error_messages.append("Address (locality) is missing")
        if not address_country:
            logging.info("address_country")
            error_messages.append("Address (country) is missing")
        if not address_street:
            logging.info("address_street")
            error_messages.append("Address (street) is missing")
        if not contact_point_telephone:
            logging.info("contact_point_telephone")
            error_messages.append("Contact Point (telephone) is missing")
        if not contact_point_email:
            logging.info("contact_point_email")
            error_messages.append("Contact Point (email) is missing")
        if not has_agri_parcel_str:
            logging.info("has_agri_parcel")
            error_messages.append("Has agri parcel is missing")
        if error_messages:
            return jsonify({"errors": error_messages}), 400
        related_source_str = farm_data.get('related_source')
        related_source = related_source_str.split(',') if related_source_str else []

        if ';' in location_str:
            location = [list(map(float, pair.split(','))) for pair in location_str.split(';')]
        else:
            location = list(map(float, location_str.split(',')))
        location = {'coordinates': location}  
        has_building = has_building_str.split(',') if has_building_str else []
        has_agri_parcel = has_agri_parcel_str.split(',') if has_agri_parcel_str else []
        see_also = see_also_str.split(',') if see_also_str else []
        land_location = [list(map(float, pair.split(','))) for pair in land_location_str.split(';')] if land_location_str else []
        if ';' in land_location_str:
            land_location = [list(map(float, pair.split(','))) for pair in land_location_str.split(';')]
        else:
            land_location = list(map(float, land_location_str.split(',')))
        land_location = {'coordinates': land_location} 
        date_created = farm_data.get('date_created')
        date_modified = farm_data.get('date_modified')
        description = farm_data.get('description')
        owned_by = farm_data.get('owned_by')
        has_building = farm_data.get('has_building')
        new_farm_data = AgriFarm(
            name=name,
            location= location,
            location_type = type_location,
            address_locality=address_locality,
            address_country=address_country,
            address_street=address_street,
            contact_point_email=contact_point_email,
            contact_point_telephone=contact_point_telephone,
            has_agri_parcel=has_agri_parcel,
            date_created=date_created,
            date_modified=date_modified,
            description=description,
            related_source=related_source,
            see_also=see_also,
            land_location=land_location,
            land_location_type=land_location_type,
            owned_by=owned_by,
            has_building=has_building
        )
        
        smart_data_model = new_farm_data.to_smart_data_model()
        send_to_context_broker("AgriFarm", smart_data_model)
        return smart_data_model, 201

season_model = ns_smart_data_models.model('Season', {
    'dateRange': fields.String(required=True, description='Date range', example="-09-28/-10-12"),
    'description': fields.String(required=True, description='Description', example="Best Season")
})


agri_crop_model = ns_smart_data_models.model('AgriCrop', {
    'date_created': fields.DateTime(required=True, description='Date created', example="2017-01-01T01:20:00Z"),
    'date_modified': fields.DateTime(required=True, description='Date modified', example="2017-05-04T12:30:00Z"),
    'name': fields.String(required=True, description='Crop name', example="Wheat"),
    'alternate_name': fields.String(required=False, description='Alternate name', example="Triticum aestivum"),
    'agro_voc_concept': fields.String(required=False, description='Agro voc concept', example="http://aims.fao.org/aos/agrovoc/c_7951"),
    'see_also': fields.String(required=False, description='See also', example="https://example.org/concept/wheat,https://datamodel.org/example/wheat"),
    'description': fields.String(required=False, description='Description', example="Spring wheat"),
    'related_source': fields.String(required=False, description='Related source', example="urn:ngsi-ld:AgriApp:72d9fb43-53f8-4ec8-a33c-fa931360259a;app:weat"),
    'has_agri_soil': fields.String(required=True, description='Has agri soil', example="urn:ngsi-ld:AgriSoil:00411b56-bd1b-4551-96e0-a6e7fde9c840,urn:ngsi-ld:AgriSoil:e8a8389a-edf5-4345-8d2c-b98ac1ce8e2a"),
    'has_agri_fertiliser': fields.String(required=True, description='Has agri fertiliser', example="urn:ngsi-ld:AgriFertiliser:1b0d6cf7-320c-4a2b-b2f1-4575ea850c73,urn:ngsi-ld:AgriFertiliser:380973c8-4d3b-4723-a899-0c0c5cc63e7e"),
    'has_agri_pest': fields.String(required=False, description='Has agri pest', example="urn:ngsi-ld:AgriPest:1b0d6cf7-320c-4a2b-b2f1-4575ea850c73,urn:ngsi-ld:AgriPest:380973c8-4d3b-4723-a899-0c0c5cc63e7e"),
    'planting_from': fields.String(required=True, description='Planting from', example='[{"dateRange": "-09-28/-10-12", "description": "Best Season"}]'),
    'harvesting_interval': fields.String(required=True, description='Harvesting interval', example='[{"dateRange": "-09-28/-10-12", "description": "Best Season"}]'),
    'watering_frequency': fields.String(required=False, description='Watering frequency', example="daily"),
})

@ns_smart_data_models.doc(security='Bearer Auth')
@ns_smart_data_models.route('/agri_crop')
class AgriCropResource(Resource):
    @api_key_required
    @ns_smart_data_models.expect(agri_crop_model, validate=True)
    @ns_smart_data_models.response(201, 'AgriCrop successfully created.')
    def post(self):
        crop_data = request.get_json()

        name = crop_data.get('name')
        has_agri_soil_str = crop_data.get('has_agri_soil')
        planting_from_str = crop_data.get('planting_from')

        error_messages = []
        if not name:
            logging.append("Name")
            error_messages.append("Name is missing")
        if not has_agri_soil_str:
            logging.append("has_agri_soil")
            error_messages.append("Has agri soil is missing")
        if not planting_from_str:
            logging.append("planting_from")
            error_messages.append("Planting from is missing")
        if error_messages:
            return jsonify({"errors": error_messages}), 400
        
        has_agri_soil = has_agri_soil_str.split(',') if has_agri_soil_str else []
        planting_from = loads(planting_from_str) if planting_from_str else []

        alternate_name = crop_data.get('alternate_name')
        agro_voc_concept = crop_data.get('agro_voc_concept')
        description = crop_data.get('description')
        date_created = crop_data.get('date_created')
        date_modified = crop_data.get('date_modified')
        see_also = crop_data.get('see_also')
        related_source = crop_data.get('related_source')
        has_agri_fertiliser_str = crop_data.get('has_agri_fertiliser')
        has_agri_fertiliser = has_agri_fertiliser_str.split(',') if has_agri_fertiliser_str else []

        has_agri_pest_str = crop_data.get('has_agri_pest')
        has_agri_pest = has_agri_pest_str.split(',') if has_agri_pest_str else []

        harvesting_interval_str = crop_data.get('harvesting_interval')
        harvesting_interval = loads(harvesting_interval_str) if harvesting_interval_str else []

        watering_frequency = crop_data.get('watering_frequency')

        new_crop = AgriCrop(
            name=name,
            alternate_name=alternate_name,
            agro_voc_concept=agro_voc_concept,
            description=description,
            date_created=date_created,
            date_modified=date_modified,
            see_also=see_also,
            related_source=related_source,
            has_agri_soil=has_agri_soil,
            has_agri_fertiliser=has_agri_fertiliser,
            has_agri_pest=has_agri_pest,
            planting_from=planting_from,
            harvesting_interval=harvesting_interval,
            watering_frequency=watering_frequency
        )
        
        smart_data_model = new_crop.to_smart_data_model()
        send_to_context_broker("AgriCrop", smart_data_model)
        return smart_data_model, 201
    

agri_greenhouse_model = ns_smart_data_models.model('AgriGreenHouse', {
    'relative_humidity': fields.Float(required=True, description='Relative humidity', example=45.0),
    'co2': fields.Float(required=True, description='CO2', example=400.0),
    'date_created': fields.DateTime(description='Date created', example="2023-01-01T01:20:00Z"),
    'date_modified': fields.DateTime(description='Date modified', example="2023-03-01T12:30:00Z"),
    'owned_by': fields.String(description='Owned by', example="urn:ngsi-ld:Person:abcd1234-3434-49d1-a212-2f30a9824d99"),
    'related_source': fields.String(description='Related source', example="urn:ngsi-ld:AgriApp:98765fb2-2231-41c3-1234-56f1044f7d98,urn:ngsi-ld:AgriApp:abcd1234-3434-49d1-a212-2f30a9824d99"),
    'see_also': fields.String(description='See also', example="https://example.org/concept/greenhouse,https://datamodel.org/example/greenhouse"),
    'belongs_to': fields.String(description='Belongs to', example="urn:ngsi-ld:AgriFarm:1a2b3c4d-5e6f-7g8h-9i0j-klmnopqrstu"),
    'has_agri_parcel_parent': fields.String(description='Has agri parcel parent', example="urn:ngsi-ld:AgriParcel:12345abc-6de7-8901-2345-fghijk6789"),
    'has_agri_parcel_children': fields.String(description='Has agri parcel children', example="urn:ngsi-ld:AgriParcel:54321cba-7de6-8901-2345-fghijk6789,urn:ngsi-ld:AgriParcel:abc123de-456f-789g-0hij-klmnopqrstuv"),
    'has_weather_observed': fields.String(description='Has weather observed', example="urn:ngsi-ld:WeatherObserved:abcdefgh-ijkl-mnop-qrst-uvwxyz0123"),
    'has_water_quality_observed': fields.String(description='Has water quality observed', example="urn:ngsi-ld:WaterQualityObserved:abc123def-456ghi-789jkl-0mnopqrstuvwxyz,urn:ngsi-ld:WaterQualityObserved:def456ghi-789jkl-0mnop-abc123qrstuvwxyz"),
    'leaf_temperature': fields.Float(description='Leaf temperature', example=25.0),
    'daily_light': fields.Float(description='Daily light', example=1000.0),
    'drain_flow': fields.Float(description='Drain flow', example=10.0),
    'has_device': fields.String(description='Has device', example="urn:ngsi-ld:Device:abcd1234-efgh-5678-ijkl-9mnopqrstuvwxyz,urn:ngsi-ld:Device:wxyz1234-lmno-5678-pqrs-9abcdefghijk"),
})

@ns_smart_data_models.doc(security='Bearer Auth')
@ns_smart_data_models.route('/agri_green_house')
class AgriGreenHouseResource(Resource):
    @api_key_required
    @ns_smart_data_models.expect(agri_greenhouse_model, validate=True)
    @ns_smart_data_models.response(201, 'AgriGreenHouse successfully created.')
    def post(self):
        greenhouse_data  = request.get_json()

        relative_humidity = greenhouse_data.get('relative_humidity')
        co2 = greenhouse_data.get('co2')
        error_messages = []

        if not relative_humidity:
            logging.info("relative_humidity")
            error_messages.append("Relative humidity is missing")
        if not co2:
            logging.info("co2")
            error_messages.append("CO2 is missing")

        if error_messages:
            return jsonify({"errors": error_messages}), 400
        
        date_created = greenhouse_data.get('date_created')
        date_modified = greenhouse_data.get('date_modified')
        owned_by = greenhouse_data.get('owned_by')
        belongs_to = greenhouse_data.get('belongs_to')
        has_agri_parcel_parent_str = greenhouse_data.get('has_agri_parcel_parent')
        has_agri_parcel_parent =  has_agri_parcel_parent_str.split(',') if has_agri_parcel_parent_str else []
        has_weather_observed_str = greenhouse_data.get('has_weather_observed')
        has_weather_observed =  has_weather_observed_str.split(',') if has_weather_observed_str else []
        leaf_temperature = greenhouse_data.get('leaf_temperature')
        daily_light = greenhouse_data.get('daily_light')
        drain_flow = greenhouse_data.get('drain_flow')
        drain_flow_max_value = greenhouse_data.get('drain_flow_max_value')
        drain_flow_min_value = greenhouse_data.get('drain_flow_min_value')

        related_source_str = greenhouse_data.get('related_source')
        related_source = related_source_str.split(',') if related_source_str else []
        see_also_str = greenhouse_data.get('see_also')
        see_also =  see_also_str.split(',') if see_also_str else []
        has_agri_parcel_children_str = greenhouse_data.get('has_agri_parcel_children')
        has_agri_parcel_children =  has_agri_parcel_children_str.split(',') if has_agri_parcel_children_str else []
        has_water_quality_observed_str = greenhouse_data.get('has_water_quality_observed')
        has_water_quality_observed = has_water_quality_observed_str.split(',') if has_water_quality_observed_str else []
        has_device_str = greenhouse_data.get('has_device')
        has_device =  has_device_str.split(',') if has_device_str else []
        

        new_greenhouse = AgriGreenHouse(
            date_created=date_created,
            date_modified=date_modified,
            owned_by=owned_by,
            related_source=related_source,
            see_also=see_also,
            belongs_to=belongs_to,
            has_agri_parcel_parent=has_agri_parcel_parent,
            has_agri_parcel_children=has_agri_parcel_children,
            has_weather_observed=has_weather_observed,
            has_water_quality_observed=has_water_quality_observed,
            relative_humidity=relative_humidity,
            leaf_temperature=leaf_temperature,
            co2=co2,
            daily_light=daily_light,
            drain_flow=drain_flow,
            drain_flow_max_value=drain_flow_max_value,
            drain_flow_min_value=drain_flow_min_value,
            has_device=has_device
        )
        
        smart_data_model = new_greenhouse.to_smart_data_model()
        send_to_context_broker("AgriGreenHouse", smart_data_model)
        return smart_data_model, 201


agri_parcel_model = ns_smart_data_models.model('AgriParcel', {
    'date_created': fields.DateTime(required=True, description='Creation date', example="2017-01-01T01:20:00Z"),
    'date_modified': fields.DateTime(required=True, description='Modification date', example="2017-05-04T12:30:00Z"),
    'location': fields.String(required=True, description='Parcel location', example="100,0;101,0;101,1;100,1;100,0"),
    'location_type': fields.String(required=True, description='Parcel location type', example="Polygon"),
    'area': fields.Float(required=True, description='Parcel area', example=200),
    'description': fields.String(required=True, description='Parcel description', example="Spring wheat"),
    'category': fields.String(required=True, description='Parcel category', example="arable"),
    'belongs_to': fields.String(required=True, description='Farm the parcel belongs to', example="urn:ngsi-ld:AgriFarm:f67adcbc-4479-22bc-9de1-cb228de7a765"),
    'owned_by': fields.String(required=False, description='Person who owns the parcel', example="urn:ngsi-ld:Person:fce9dcbc-4479-11e8-9de1-cb228de7a15c"),
    'has_agri_parcel_parent': fields.String(required=False, description='Parent parcel relationship', example="urn:ngsi-ld:AgriParcel:1ea0f120-4474-11e8-9919-672036642081"),
    'has_agri_parcel_children': fields.String(required=False, description='Child parcels relationship', example='urn:ngsi-ld:AgriParcel:26ba4be0-4474-11e8-8ec1-ab9e0ea93835,urn:ngsi-ld:AgriParcel:2d5b8874-4474-11e8-8d6b-dbe14425b5e4'),
    'has_agri_crop': fields.String(required=False, description='Parcel crop relationship', example="urn:ngsi-ld:AgriCrop:36021150-4474-11e8-a721-af07c5fae7c8"),
    'has_air_quality_observed': fields.String(required=False, description='Air quality observed relationship', example="urn:ngsi-ld:AirQualityObserved:B3F76EA170D030BCD9E036DCC9BEA22B"),
    'crop_status': fields.String(required=False, description='Crop status', example="seeded"),
    'last_planted_at': fields.DateTime(required=False, description='Last planted date', example="2016-08-23T10:18:16Z"),
    'has_agri_soil': fields.String(required=True, description='Parcel soil relationship', example="urn:ngsi-ld:AgriSoil:429d1338-4474-11e8-b90a-d3e34ceb73df"),
    'has_device': fields.String(required=False, description='Devices related to the parcel', example='urn:ngsi-ld:Device:4a40aeba-4474-11e8-86bf-03d82e958ce6,urn:ngsi-ld:Device:63217d24-4474-11e8-9da2-03d82e958ce6'),
    'soil_texture_type': fields.String(required=False, description='Soil texture type', example="Clay"),
    'irrigation_system_type': fields.String(required=False, description='Irrigation system type', example="Drip irrigation"),
    'related_source': fields.String(description='Related source', example="urn:ngsi-ld:AgriApp:98765fb2-2231-41c3-1234-56f1044f7d98,urn:ngsi-ld:AgriApp:abcd1234-3434-49d1-a212-2f30a9824d99"),
    'see_also': fields.String(required=False, description='Related links', example="https://example.org/concept/agriparcel,https://datamodel.org/example/agriparcel"),
})

@ns_smart_data_models.doc(security='Bearer Auth')
@ns_smart_data_models.route('/agri_parcel')
class AgriParcelResource(Resource):
    @api_key_required
    @ns_smart_data_models.expect(agri_parcel_model, validate=True)
    @ns_smart_data_models.response(201, 'AgriParcel successfully created.')
    def post(self):
        parcel_data = request.get_json()

        location_str = parcel_data.get('location')
        location_type = parcel_data.get('location_type')
        area = parcel_data.get('area')
        description = parcel_data.get('description')
        category = parcel_data.get('category')
        belongs_to = parcel_data.get('belongs_to')
        has_agri_soil = parcel_data.get('has_agri_soil')
        
        error_messages = []
        if not location_str:
            error_messages.append("Location is missing")
        if not location_type:
            error_messages.append("Location type is missing")
        if not area:
            error_messages.append("Area is missing")
        if not description:
            error_messages.append("Description is missing")
        if not category:
            error_messages.append("Category is missing")
        if not belongs_to:
            error_messages.append("Belongs to is missing")
        if not has_agri_soil:
            error_messages.append("Has agri soil is missing")
        if error_messages:
            return jsonify({"errors": error_messages}), 400
        
        if ';' in location_str:
            location = [list(map(float, pair.split(','))) for pair in location_str.split(';')]
        else:
            location = list(map(float, location_str.split(',')))
        location = {'coordinates': location}  
        
        date_created = parcel_data.get('date_created')
        date_modified = parcel_data.get('date_modified')
        has_agri_parcel_parent = parcel_data.get('has_agri_parcel_parent')
        soil_texture_type = parcel_data.get('soil_texture_type')
        related_source_str = parcel_data.get('related_source')
        related_source = related_source_str.split(',') if related_source_str else None


        see_also_str = parcel_data.get('see_also')
        see_also = see_also_str.split(',') if see_also_str else None
        
        owned_by = parcel_data.get('owned_by')
        has_agri_parcel_children_str = parcel_data.get('has_agri_parcel_children')
        has_agri_parcel_children = has_agri_parcel_children_str.split(',') if has_agri_parcel_children_str else None

        has_agri_crop = parcel_data.get('has_agri_crop')
        has_air_quality_observed = parcel_data.get('has_air_quality_observed')
        crop_status = parcel_data.get('crop_status')
        last_planted_at = parcel_data.get('last_planted_at')
        has_device_str = parcel_data.get('has_device')
        has_device = has_device_str.split(',') if has_device_str else None

        irrigation_system_type = parcel_data.get('irrigation_system_type')

        new_parcel = AgriParcel(
            date_created=date_created,
            date_modified=date_modified,
            location= location,
            type_location= location_type,
            area=area,
            description=description,
            category=category,
            belongs_to=belongs_to,
            has_agri_parcel_parent=has_agri_parcel_parent,
            has_agri_soil=has_agri_soil,
            soil_texture_type=soil_texture_type,
            related_source=related_source,
            see_also=see_also,
            owned_by=owned_by,
            has_agri_parcel_children=has_agri_parcel_children,
            has_agri_crop=has_agri_crop,
            has_air_quality_observed=has_air_quality_observed,
            crop_status=crop_status,
            last_planted_at=last_planted_at,
            has_device=has_device,
            irrigation_system_type=irrigation_system_type
        )
        
        smart_data_model = new_parcel.to_smart_data_model()
        send_to_context_broker("AgriParcel", smart_data_model)
        return smart_data_model, 201

agri_parcel_operation_model = ns_smart_data_models.model('AgriParcelOperation', {
    'date_created': fields.DateTime(required=True, description='Creation date', example="2017-01-01T01:20:00Z"),
    'date_modified': fields.DateTime(required=True, description='Modification date', example="2017-05-04T12:30:00Z"),
    'related_source': fields.String(required=False, description='Related source', example="urn:ngsi-ld:AgriApp:72d9fb43-53f8-4ec8-a33c-fa931360259a,urn:ngsi-ld:AgriApp:72d9fb43-53f8-4ec8-a33c-fa941260259b"),
    'see_also': fields.String(required=False, description='Related links', example="https://example.org/concept/agriparcelop,https://datamodel.org/example/agriparcelop"),
    'has_agri_parcel': fields.String(required=True, description='Associated Agri Parcel', example="urn:ngsi-ld:AgriParcel:318366a9-7643-4d8e-9a11-c76a8c29d8eb"),
    'operation_type': fields.String(required=True, description='Operation type', example="fertiliser"),
    'description': fields.String(required=True, description='Operation description', example="Monthly fertiliser application"),
    'result': fields.String(required=True, description='Operation result', example="ok"),
    'planned_start_at': fields.DateTime(required=True, description='Planned start date', example="2016-08-22T10:18:16Z"),
    'planned_end_at': fields.DateTime(required=True, description='Planned end date', example="2016-08-28T10:18:16Z"),
    'status': fields.String(required=True, description='Operation status', example="finished"),
    'has_operator': fields.String(required=False, description='Operator responsible', example="urn:ngsi-ld:Person:fce9dcbc-4479-11e8-9de1-cb228de7a15c"),
    'started_at': fields.DateTime(required=True, description='Actual start date', example="2016-08-22T10:18:16Z"),
    'ended_at': fields.DateTime(required=True, description='Actual end date', example="2016-08-28T10:18:16Z"),
    'reported_at': fields.DateTime(required=True, description='Reported date', example="2016-08-28T10:18:16Z"),
    'has_agri_product_type': fields.String(required=False, description='Agri Product Type', example="urn:ngsi-ld:AgriProductType:a8f616b8-13fb-473a-8e61-b7a80c6c93ec"),
    'quantity': fields.Float(required=True, description='Quantity', example=40),
    'water_source': fields.String(required=False, description='Water Source', example="rainwater capture"),
    'work_order': fields.String(required=False, description='Work order', example="https://example.com/agriparcelrecords/workorder1"),
    'work_record': fields.String(required=False, description='Work record', example="https://example.com/agriparcelrecords/workrecord1"),
    'irrigation_record': fields.String(required=False, description='Irrigation record', example="https://example.com/agriparcelrecords/irrigationrecord1"),
    'diesel_fuel_consumption': fields.Float(required=True, description='Diesel fuel consumption (liters)', example=33),
    'gasoline_fuel_consumption': fields.Float(required=True, description='Gasoline fuel consumption (liters)', example=33),
    'diesel_fuel_consumption_max_value': fields.Float(required=False, description='Max Diesel fuel consumption (liters)', example=50),
    'diesel_fuel_consumption_min_value': fields.Float(required=False, description='Min Diesel fuel consumption (liters)', example=25),
    'diesel_fuel_consumption_unit_text': fields.String(required=False, description='Unit of Diesel fuel consumption', example='liters'),
    'gasoline_fuel_consumption_max_value': fields.Float(required=False, description='Max Gasoline fuel consumption (liters)', example=50),
    'gasoline_fuel_consumption_min_value': fields.Float(required=False, description='Min Gasoline fuel consumption (liters)', example=25),
    'gasoline_fuel_consumption_unit_text': fields.String(required=False, description='Unit of Gasoline fuel consumption', example='liters')
    })


@ns_smart_data_models.doc(security='Bearer Auth')
@ns_smart_data_models.route('/agri_parcel_operation')
class AgriParcelOperationResource(Resource):
    @api_key_required
    @ns_smart_data_models.expect(agri_parcel_operation_model, validate=True)
    @ns_smart_data_models.response(201, 'AgriParcelOperation successfully created.')
    def post(self):
        operation_data = request.get_json()

        has_agri_parcel = operation_data.get('has_agri_parcel')
        operation_type = operation_data.get('operation_type')
        description = operation_data.get('description')
        result = operation_data.get('result')
        planned_start_at = operation_data.get('planned_start_at')
        planned_end_at = operation_data.get('planned_end_at')
        status = operation_data.get('status')
        started_at = operation_data.get('started_at')
        ended_at = operation_data.get('ended_at')
        reported_at = operation_data.get('reported_at')
        quantity = operation_data.get('quantity')
        diesel_fuel_consumption = operation_data.get('diesel_fuel_consumption')
        gasoline_fuel_consumption = operation_data.get('gasoline_fuel_consumption')
        diesel_fuel_consumption_max_value= operation_data.get('diesel_fuel_consumption_max_value')
        diesel_fuel_consumption_min_value = operation_data.get('diesel_fuel_consumption_max_value')
        diesel_fuel_consumption_unit_text = operation_data.get('diesel_fuel_consumption_unit_text')
        gasoline_fuel_consumption_max_value = operation_data.get('gasoline_fuel_consumption_max_value')
        gasoline_fuel_consumption_min_value = operation_data.get('gasoline_fuel_consumption_min_value')
        gasoline_fuel_consumption_unit_text = operation_data.get('gasoline_fuel_consumption_unit_text')

        
        error_messages = []
        if not has_agri_parcel:
            error_messages.append("Has agri parcel is missing")
        if not operation_type:
            error_messages.append("Operation type is missing")
        if not description:
            error_messages.append("Description is missing")
        if not result:
            error_messages.append("Result is missing")
        if not planned_start_at:
            error_messages.append("Planned start at is missing")
        if not planned_end_at:
            error_messages.append("Planned end at is missing")
        if not status:
            error_messages.append("Status is missing")
        if not started_at:
            error_messages.append("Started at is missing")
        if not ended_at:
            error_messages.append("Ended at is missing")
        if not reported_at:
            error_messages.append("Reported at is missing")
        if not quantity:
            error_messages.append("Quantity is missing")
        if not diesel_fuel_consumption:
            error_messages.append("Diesel fuel consumption is missing")
        if not gasoline_fuel_consumption:
            error_messages.append("Gasoline fuel consumption is missing")
        if not diesel_fuel_consumption_max_value:
            error_messages.append("Diesel Max fuel consumption is missing")
        if not diesel_fuel_consumption_min_value:
            error_messages.append("Diesel Min fuel consumption is missing")
        if not diesel_fuel_consumption_unit_text:
            error_messages.append("Diesel Unit fuel consumption is missing")
        if not gasoline_fuel_consumption_max_value:
            error_messages.append("Gasoline Max fuel consumption is missing")
        if not gasoline_fuel_consumption_min_value:
            error_messages.append("Gasoline Min fuel consumption is missing")
        if not gasoline_fuel_consumption_unit_text:
            error_messages.append("Gasoline Unit fuel consumption is missing")
        if error_messages:
            return jsonify({"errors": error_messages}), 400
        date_created = operation_data.get('date_created')
        date_modified = operation_data.get('date_modified')
        related_source_str = operation_data.get('related_source')
        related_source = related_source_str.split(',') if related_source_str else []
        see_also_str = operation_data.get('see_also')
        see_also = see_also_str.split(',') if see_also_str else []
        has_operator = operation_data.get('has_operator')
        has_agri_product_type = operation_data.get('has_agri_product_type')
        water_source = operation_data.get('water_source')
        work_order = operation_data.get('work_order')
        work_record = operation_data.get('work_record')
        irrigation_record = operation_data.get('irrigation_record')

        new_operation = AgriParcelOperation(
            date_created=date_created,
            date_modified=date_modified,
            has_agri_parcel=has_agri_parcel,
            operation_type=operation_type,
            description=description,
            result=result,
            planned_start_at=planned_start_at,
            planned_end_at=planned_end_at,
            status=status,
            started_at=started_at,
            ended_at=ended_at,
            reported_at=reported_at,
            quantity=quantity,
            related_source=related_source,
            see_also=see_also,
            has_operator=has_operator,
            has_agri_product_type=has_agri_product_type,
            water_source=water_source,
            work_order=work_order,
            work_record=work_record,
            irrigation_record=irrigation_record,
            diesel_fuel_consumption=diesel_fuel_consumption,
            gasoline_fuel_consumption=gasoline_fuel_consumption,
            diesel_fuel_consumption_max_value=diesel_fuel_consumption_max_value,
            diesel_fuel_consumption_min_value=diesel_fuel_consumption_min_value,
            diesel_fuel_consumption_unit_text=diesel_fuel_consumption_unit_text,
            gasoline_fuel_consumption_max_value=gasoline_fuel_consumption_max_value,
            gasoline_fuel_consumption_min_value=gasoline_fuel_consumption_min_value,
            gasoline_fuel_consumption_unit_text=gasoline_fuel_consumption_unit_text
           

        )
        
        smart_data_model = new_operation.to_smart_data_model()
        send_to_context_broker("AgriParcelOperation", smart_data_model)
        return smart_data_model, 201

agri_parcel_record_model = ns_smart_data_models.model('AgriParcelRecord', {
    'date_created': fields.DateTime(required=True, example="2017-01-01T01:20:00Z"),
    'date_modified': fields.DateTime(required=True, example="2017-05-04T12:30:00Z"),
    'has_agri_parcel': fields.String(required=True, description='Associated Agri Parcel', example="urn:ngsi-ld:AgriParcel:2d5b8874-4474-11e8-8d6b-dbe14425b5e4"),
    'type_location': fields.String(required=False, description='Type of Location', example="Polygon"),
    'location': fields.String(required=True, description='Location', example="100.0, 0.0;101.0,0.0;101.0,1.0;100.0,1.0;100.0,0.0"),
    'soil_temperature_unit': fields.String(required=False, description='Unit of Soil Temperature', example='CEL'),
    'soil_temperature': fields.Float(required=True, description='Soil temperature', example=10.5),
    'air_temperature_unit': fields.String(required=False, description='Unit of Air Temperature', example='CEL'),
    'air_temperature_timestamp': fields.DateTime(required=False, description='Timestamp of Air Temperature Measurement', example="2023-05-16T01:20:00Z"),
    'air_temperature': fields.Float(required=True, description='Air temperature', example=15.3),
    'relative_humidity': fields.Float(required=True, description='Relative humidity', example=60.0),
    'relative_humidity_unit': fields.String(required=False, description='Unit of Relative Humidity', example='P1'),
    'relative_humidity_timestamp': fields.DateTime(required=False, description='Timestamp of Relative Humidity Measurement', example="2023-05-16T01:20:00Z"),
    'description': fields.String(required=False, example="Soil and weather conditions"),
    'related_source': fields.String(required=False, example="urn:ngsi-ld:AgriApp:72551db2-91d1-43c3-8534-10f1044f7d98,urn:ngsi-ld:AgriApp:72551db2-91d1-43c3-8534-10f1044f7d99"),
    'see_also': fields.String(required=False, example="https://example.org/concept/agriparcelrecord,https://example.org/concept/agriparcelrecord2"),
    'soil_moisture_vwc': fields.Float(required=False, example=0.35),
    'soil_moisture_ec': fields.Float(required=False, example=0.15),
    'soil_salinity': fields.Float(required=False, example=0.02),
    'leaf_wetness': fields.Float(required=False, example=0.8),
    'leaf_relative_humidity': fields.Float(required=False, example=70.0),
    'leaf_relative_humidity_unit': fields.String(required=False, description='Unit of Leaf Relative Humidity', example='P1'),
    'leaf_relative_humidity_timestamp': fields.DateTime(required=False, description='Timestamp of Leaf Relative Humidity Measurement', example="2023-05-16T01:20:00Z"),
    'leaf_temperature': fields.Float(required=False, example=12.2),
    'solar_radiation': fields.Float(required=False, example=900.0),
    'atmospheric_pressure': fields.Float(required=False, example=1013.0),
    'has_device': fields.String(required=False, example="urn:ngsi-ld:Device:8a95babe-2f0e-43e7-a1ca-03d2b9ac0f3e,urn:ngsi-ld:Device:8a95babe-2f0e-43e7-a1ca-03d2b9ac0f3f"),
    'observed_at': fields.DateTime(required=True, example="2021-09-01T10:00:00Z"),
    'soil_salinity_unit': fields.String(required=False, description='Unit of Soil Salinity', example='D10'),
    'soil_salinity_timestamp': fields.DateTime(required=False, description='Timestamp of Soil Salinity Measurement', example="2023-05-16T01:20:00Z"),
    'leaf_wetness_unit': fields.String(required=False, description='Unit of Leaf Wetness', example='P1'),
    'leaf_wetness_timestamp': fields.DateTime(required=False, description='Timestamp of Leaf Wetness Measurement', example="2023-05-16T01:20:00Z"),
    'leaf_temperature_unit': fields.String(required=False, description='Unit of Leaf Temperature', example='CEL'),
    'leaf_temperature_timestamp': fields.DateTime(required=False, description='Timestamp of Leaf Temperature Measurement', example="2023-05-16T01:20:00Z"),
    'solar_radiation_unit': fields.String(required=False, description='Unit of Solar Radiation', example='CEL'),
    'solar_radiation_timestamp': fields.DateTime(required=False, description='Timestamp of Solar Radiation Measurement', example="2023-05-16T01:20:00Z"),
    'atmospheric_pressure_unit': fields.String(required=False, description='Unit of Atmospheric Pressure', example='A97'),
    'atmospheric_pressure_timestamp': fields.DateTime(required=False, description='Timestamp of Atmospheric Pressure Measurement', example="2023-05-16T01:20:00Z"),
    'soil_moisture_vwc_unit': fields.String(required=False, description='Unit of Soil Moisture VWC', example='C62'),
    'soil_moisture_vwc_timestamp': fields.DateTime(required=False, description='Timestamp of Soil Moisture VWC Measurement', example="2023-05-16T01:20:00Z"),
    'soil_moisture_ec_unit': fields.String(required=False, description='Unit of Soil Moisture EC', example='D10'),
    'soil_moisture_ec_timestamp': fields.DateTime(required=False, description='Timestamp of Soil Moisture EC Measurement', example="2023-05-16T01:20:00Z"),
    'depth': fields.Float(required=True, description='Relative humidity', example=20.0),
    'depth_unit_code': fields.String(required=False, description='UnitCode of Depth', example='CMT'),
    'timestamp': fields.DateTime(required=False, description='Timestamp', example="2023-05-16T01:20:00Z"),

    
})

@ns_smart_data_models.doc(security='Bearer Auth')
@ns_smart_data_models.route('/agri_parcel_record')
class AgriParcelRecordResource(Resource):
    @api_key_required
    @ns_smart_data_models.expect(agri_parcel_record_model, validate=True)
    @ns_smart_data_models.response(201, 'AgriParcelRecord successfully created.')
    def post(self):
        record_data = request.get_json()

        has_agri_parcel = record_data.get('has_agri_parcel')
        location_str = record_data.get('location')
        type_location = record_data.get('type_location')
        soil_temperature = record_data.get('soil_temperature')
        soil_temperature_unit = record_data.get('soil_temperature_unit')
        air_temperature = record_data.get('air_temperature')
        air_temperature_unit = record_data.get('air_temperature_unit')
        air_temperature_timestamp = record_data.get('air_temperature_timestamp')
        relative_humidity = record_data.get('relative_humidity')
        relative_humidity_unit = record_data.get('relative_humidity_unit')
        relative_humidity_timestamp = record_data.get('relative_humidity_timestamp')

        error_messages = []
        if not has_agri_parcel:
            error_messages.append("Has agri parcel is missing")
        if not location_str:
            error_messages.append("Location is missing")
        if not type_location:
            error_messages.append("Location Type is missing")
        if not soil_temperature:
            error_messages.append("Soil temperature is missing")
        if not soil_temperature_unit:
            error_messages.append("Soil temperature unit is missing")
        if not air_temperature:
            error_messages.append("Air temperature is missing")
        if not air_temperature_unit:
            error_messages.append("Air temperature unit is missing")
        if not air_temperature_timestamp:
            error_messages.append("Air temperature timestamp is missing")
        if not relative_humidity:
            error_messages.append("Relative humidity is missing")
        if not relative_humidity_unit:
            error_messages.append("Relative humidity unit is missing")
        if not relative_humidity_timestamp:
            error_messages.append("Relative humidity timestamp is missing")

        if error_messages:
            return jsonify({"errors": error_messages}), 400
        
        if ';' in location_str:
            location = [list(map(float, pair.split(','))) for pair in location_str.split(';')]
        else:
            location = list(map(float, location_str.split(',')))
        location = {'coordinates': location}  



        date_created = record_data.get('date_created')
        date_modified = record_data.get('date_modified')
        related_source_str = record_data.get('related_source')
        related_source = related_source_str.split(',') if related_source_str else []
        see_also_str = record_data.get('see_also')
        see_also = see_also_str.split(',') if see_also_str else []
        description = record_data.get('description')
        soil_moisture_vwc = record_data.get('soil_moisture_vwc')
        soil_moisture_ec = record_data.get('soil_moisture_ec')
        soil_salinity = record_data.get('soil_salinity')
        leaf_wetness = record_data.get('leaf_wetness')
        leaf_relative_humidity = record_data.get('leaf_relative_humidity')
        leaf_temperature = record_data.get('leaf_temperature')
        solar_radiation = record_data.get('solar_radiation')
        atmospheric_pressure = record_data.get('atmospheric_pressure')
        has_device_str = record_data.get('has_device')
        has_device = has_device_str.split(',') if has_device_str else []
        observed_at = record_data.get('observed_at')
        soil_salinity_unit = record_data.get('soil_salinity_unit')
        soil_salinity_timestamp = record_data.get('soil_salinity_timestamp')
        leaf_wetness_unit = record_data.get('leaf_wetness_unit')
        leaf_wetness_timestamp = record_data.get('leaf_wetness_timestamp')
        leaf_temperature_unit = record_data.get('leaf_temperature_unit')
        leaf_temperature_timestamp = record_data.get('leaf_temperature_timestamp')
        solar_radiation_unit = record_data.get('solar_radiation_unit')
        solar_radiation_timestamp = record_data.get('solar_radiation_timestamp')
        atmospheric_pressure_unit = record_data.get('atmospheric_pressure_unit')
        atmospheric_pressure_timestamp = record_data.get('atmospheric_pressure_timestamp')
        soil_moisture_vwc_unit = record_data.get('soil_moisture_vwc_unit')
        soil_moisture_vwc_timestamp = record_data.get('soil_moisture_vwc_timestamp')
        soil_moisture_ec_unit = record_data.get('soil_moisture_ec_unit')
        soil_moisture_ec_timestamp = record_data.get('soil_moisture_ec_timestamp')
        leaf_relative_humidity_unit = record_data.get('leaf_relative_humidity_unit')
        leaf_relative_humidity_timestamp = record_data.get('leaf_relative_humidity_timestamp')
        depth = record_data.get('depth')
        depth_unit_code = record_data.get('depth_unit_code')
        timestamp = record_data.get('timestamp')


        new_record = AgriParcelRecord(
            date_created=date_created,
            date_modified=date_modified,
            has_agri_parcel=has_agri_parcel,
            type_location=type_location,
            location = location,
            soil_temperature=soil_temperature,
            soil_temperature_unit=soil_temperature_unit,
            air_temperature=air_temperature,
            air_temperature_unit=air_temperature_unit,
            air_temperature_timestamp = air_temperature_timestamp,
            relative_humidity=relative_humidity,
            relative_humidity_unit=relative_humidity_unit,
            relative_humidity_timestamp=relative_humidity_timestamp,
            description=description,
            related_source=related_source,
            see_also=see_also,
            soil_moisture_vwc=soil_moisture_vwc,
            soil_moisture_ec=soil_moisture_ec,
            soil_salinity=soil_salinity,
            leaf_wetness=leaf_wetness,
            leaf_relative_humidity=leaf_relative_humidity,
            leaf_temperature=leaf_temperature,
            solar_radiation=solar_radiation,
            atmospheric_pressure=atmospheric_pressure,
            has_device=has_device,
            observed_at=observed_at,
            soil_salinity_unit= soil_salinity_unit,
            soil_salinity_timestamp = soil_salinity_timestamp,
            leaf_wetness_unit = leaf_wetness_unit,
            leaf_wetness_timestamp = leaf_wetness_timestamp,
            leaf_temperature_unit = leaf_temperature_unit,
            leaf_temperature_timestamp = leaf_temperature_timestamp,
            solar_radiation_unit = solar_radiation_unit,
            solar_radiation_timestamp = solar_radiation_timestamp,
            atmospheric_pressure_unit = atmospheric_pressure_unit,
            atmospheric_pressure_timestamp = atmospheric_pressure_timestamp,
            soil_moisture_vwc_unit = soil_moisture_vwc_unit,
            soil_moisture_vwc_timestamp = soil_moisture_vwc_timestamp,
            soil_moisture_ec_unit = soil_moisture_ec_unit,
            soil_moisture_ec_timestamp = soil_moisture_ec_timestamp,
            leaf_relative_humidity_unit = leaf_relative_humidity_unit,
            leaf_relative_humidity_timestamp= leaf_relative_humidity_timestamp,
            depth=depth,
            depth_unit=depth_unit_code,
            timestamp=timestamp


        )
        
        smart_data_model = new_record.to_smart_data_model()
        send_to_context_broker("AgriParcelRecord", smart_data_model)
        return smart_data_model, 201

agri_soil_model = ns_smart_data_models.model('AgriSoil', {
    'date_created': fields.DateTime(required=True, example="2017-01-01T01:20:00Z"),
    'date_modified': fields.DateTime(required=True, example="2017-05-04T12:30:00Z"),
    'name': fields.String(required=True, description='Name', example="Clay"),
    'alternate_name': fields.String(required=False, description='Alternate name', example="Heavy soil"),
    'description': fields.String(required=False, description='Description', example="Fine grained, poor draining soil. Particle size less than 0.002mm"),
    'agro_voc_concept': fields.String(required=False, description='AgroVoc Concept URL', example="http://aims.fao.org/aos/agrovoc/c_7951"),
    'see_also': fields.String(required=False, description='See also URLs', example="https://example.org/concept/clay"),
    'related_source': fields.String(required=False, description='Related source', example="urn:ngsi-ld:AgriApp:72d9fb43-53f8-4ec8-a33c-fa931360259a,urn:ngsi-ld:AgriApp:72d9fb43-53f8-4ec8-a33c-fa931360259a"),
    'has_agri_product_type': fields.String(required=False, description='Associated Agri Product Type', example="urn:ngsi-ld:AgriProductType:ea54eedf-d5a7-4e44-bddd-50e9935237c0,urn:ngsi-ld:AgriProductType:275b4c08-5e52-4bb7-8523-74ce5d0007de")
})


@ns_smart_data_models.doc(security='Bearer Auth')
@ns_smart_data_models.route('/agri_soil')
class AgriSoilResource(Resource):
    @api_key_required
    @ns_smart_data_models.expect(agri_soil_model, validate=True)
    @ns_smart_data_models.response(201, 'AgriSoil successfully created.')
    def post(self):
        soil_data = request.get_json()

        name = soil_data.get('name')

        error_messages = []
        if not name:
            error_messages.append("Name is missing")
        if error_messages:
            return jsonify({"errors": error_messages}), 400
        date_created = soil_data.get('date_created')
        date_modified = soil_data.get('date_modified')
        alternate_name = soil_data.get('alternate_name')
        description = soil_data.get('description')
        agro_voc_concept = soil_data.get('agro_voc_concept')
        see_also = soil_data.get('see_also').split(',') if soil_data.get('see_also') else []
        related_source = soil_data.get('related_source').split(',') if soil_data.get('related_source') else []
        has_agri_product_type = soil_data.get('has_agri_product_type').split(',') if soil_data.get('has_agri_product_type') else []
        

        new_soil = AgriSoil(
            date_created=date_created,
            date_modified=date_modified,
            name=name,
            alternate_name=alternate_name,
            description=description,
            agro_voc_concept=agro_voc_concept,
            see_also=see_also,
            related_source=related_source,
            has_agri_product_type=has_agri_product_type
        )
        
        smart_data_model = new_soil.to_smart_data_model()
        send_to_context_broker("AgriSoil", smart_data_model)
        return smart_data_model, 201

agri_soil_state_model = ns_smart_data_models.model('AgriSoilState', {
    'date_created': fields.DateTime(required=True, example="2017-01-01T01:20:00Z"),
    'date_modified': fields.DateTime(required=True, example="2017-05-04T12:30:00Z"),
    'date_of_measurement': fields.DateTime(required=True, description='Date of measurement', example="2017-01-01T01:20:00Z"),
    'acidity': fields.Float(required=True, description='Acidity', example=7),
    'acidity_unit_code': fields.String(required=False, description='UnitCode of Acidity', example='pH'),
    'acidity_timestamp': fields.DateTime(required=False, description='Timestamp of Acidity', example="2023-05-16T01:20:00Z"),
    'electrical_conductivity': fields.Float(required=False, description='Electrical Conductivity', example=1),
    'electrical_conductivity_unit': fields.String(required=False, description='UnitCode of Electrical Conductivity', example='ohm/meter'),
    'electrical_conductivity_timestamp': fields.DateTime(required=False, description='Timestamp of Electrical Conductivity', example="2023-05-16T01:20:00Z"),
    'density': fields.Float(required=False, description='Density', example=10),
    'density_unit': fields.String(required=False, description='UnitCode of Density', example='kg/m3'),
    'density_timestamp': fields.DateTime(required=False, description='Timestamp of Density', example="2023-05-16T01:20:00Z"),
    'density': fields.Float(required=False, description='Density', example=10),
    'humus': fields.Float(required=True, description='Humus', example=5),
    'humus_unit_code': fields.String(required=False, description='UnitCode of Humus', example='percent'),
    'humus_timestamp': fields.DateTime(required=False, description='Timestamp of Humus', example="2023-05-16T01:20:00Z"),
    'has_agri_soil': fields.String(required=False, description='Associated Agri Soil', example="urn:ngsi-ld:AgriSoil:1ea0f120-4474-11e8-9919-672036642081"),
    'has_agri_parcel': fields.String(required=False, description='Associated Agri Parcel', example="urn:ngsi-ld:AgriParcel:1ea0f120-4474-11e8-9919-672036642081"),
    'has_agri_greenhouse': fields.String(required=False, description='Associated Agri Greenhouse', example="urn:ngsi-ld:AgriGreenhouse:1ea0f120-4474-11e8-9919-672036642081"),
})


@ns_smart_data_models.doc(security='Bearer Auth')
@ns_smart_data_models.route('/agri_soil_state')
class AgriSoilStateResource(Resource):
    @api_key_required
    @ns_smart_data_models.expect(agri_soil_state_model, validate=True)
    @ns_smart_data_models.response(201, 'AgriSoilState successfully created.')
    def post(self):
        soil_state_data = request.get_json()

        date_of_measurement = soil_state_data.get('date_of_measurement')
        acidity = soil_state_data.get('acidity')
        acidity_unit_code = soil_state_data.get('acidity_unit_code')
        acidity_timestamp = soil_state_data.get('acidity_timestamp')
        humus = soil_state_data.get('humus')
        humus_unit_code = soil_state_data.get('humus_unit_code')
        humus_timestamp = soil_state_data.get('humus_timestamp')


        error_messages = []
        if not date_of_measurement:
            error_messages.append("Date of measurement is missing")
        if not acidity:
            error_messages.append("Acidity is missing")
        if not acidity_unit_code:
            error_messages.append("Acidity Unit Code is missing")
        if not acidity_timestamp:
            error_messages.append("Acidity timestamp is missing")
        if not humus:
            error_messages.append("Humus is missing")
        if not humus_unit_code:
            error_messages.append("Humus Unit Code is missing")
        if not humus_timestamp:
            error_messages.append("Humus Timestamp is missing")
        if error_messages:
            return jsonify({"errors": error_messages}), 400
        date_created = soil_state_data.get('date_created')
        date_modified = soil_state_data.get('date_modified')
        electrical_conductivity = soil_state_data.get('electrical_conductivity')
        electrical_conductivity_unit = soil_state_data.get('electrical_conductivity_unit')
        electrical_conductivity_timestamp = soil_state_data.get('electrical_conductivity_timestamp')
        density = soil_state_data.get('density')
        density_unit = soil_state_data.get('density_unit')
        density_timestamp = soil_state_data.get('density_timestamp')
        has_agri_soil = soil_state_data.get('has_agri_soil')
        has_agri_parcel = soil_state_data.get('has_agri_parcel')
        has_agri_greenhouse = soil_state_data.get('has_agri_greenhouse')
        

        new_soil_state = AgriSoilState(
            date_created=date_created,
            date_modified=date_modified,
            date_of_measurement=date_of_measurement,
            acidity=acidity,
            acidity_unit=acidity_unit_code,
            acidity_timestamp=acidity_timestamp,
            humus=humus,
            humus_unit=humus_unit_code,
            humus_timestamp=humus_timestamp,
            electrical_conductivity=electrical_conductivity,
            electrical_conductivity_unit=electrical_conductivity_unit,
            electrical_conductivity_timestamp=electrical_conductivity_timestamp,
            density=density,
            density_unit=density_unit,
            density_timestamp=density_timestamp,
            has_agri_soil=has_agri_soil,
            has_agri_parcel=has_agri_parcel,
            has_agri_greenhouse=has_agri_greenhouse
        )
        
        smart_data_model = new_soil_state.to_smart_data_model()
        send_to_context_broker("AgriSoilState", smart_data_model)
        return smart_data_model, 201


agri_yield_model = ns_smart_data_models.model('AgriYield', {
    'has_agri_crop': fields.String(required=False, example="urn:ngsi-ld:AgriCrop:1ea0f120-4474-11e8-9919-672036642081"),
    'has_agri_parcel': fields.String(required=False, example="urn:ngsi-ld:AgriParcel:1ea0f120-4474-11e8-9919-672036642081"),
    'start_date_of_gathering_at': fields.DateTime(required=True, description='Start date of gathering', example="2017-01-01T01:20:00Z"),
    'end_date_of_gathering_at': fields.DateTime(required=True, description='End date of gathering', example="2017-01-01T01:20:00Z"),
    'yield_value': fields.Float(required=True, description='Yield value', example=50),
    'yield_max_value': fields.Float(required=False, description='Yield max value', example=70),
    'yield_min_value': fields.Float(required=False, description='Yield min value', example=30),
    'yield_unit_text': fields.String(required=False, description='Yield measurement unit', example='Tons per hectare')
})


@ns_smart_data_models.doc(security='Bearer Auth')
@ns_smart_data_models.route('/agri_yield')
class AgriYieldResource(Resource):
    @api_key_required
    @ns_smart_data_models.expect(agri_yield_model, validate=True)
    @ns_smart_data_models.response(201, 'AgriYield successfully created.')
    def post(self):
        yield_data = request.get_json()

        start_date_of_gathering_at = yield_data.get('start_date_of_gathering_at')
        end_date_of_gathering_at = yield_data.get('end_date_of_gathering_at')
        yield_value = yield_data.get('yield_value')
        yield_max_value = yield_data.get('yield_max_value')
        yield_min_value = yield_data.get('yield_min_value')
        yield_unit_text = yield_data.get('yield_unit_text')

        error_messages = []
        if not start_date_of_gathering_at:
            error_messages.append("Start date of gathering is missing")
        if not end_date_of_gathering_at:
            error_messages.append("End date of gathering is missing")
        if not yield_value:
            error_messages.append("Yield value is missing")
        if not yield_max_value:
            error_messages.append("Yield max value is missing")
        if not yield_min_value:
            error_messages.append("Yield min value is missing")
        if not yield_unit_text:
            error_messages.append("Yield unit value is missing")
        if error_messages:
            return jsonify({"errors": error_messages}), 400
        has_agri_crop = yield_data.get('has_agri_crop')
        has_agri_parcel = yield_data.get('has_agri_parcel')

        

        new_yield = AgriYield(
            has_agri_crop=has_agri_crop,
            has_agri_parcel=has_agri_parcel,
            start_date_of_gathering_at=start_date_of_gathering_at,
            end_date_of_gathering_at=end_date_of_gathering_at,
            yield_value=yield_value,
            yield_max_value=yield_max_value,
            yield_min_value=yield_min_value,
            yield_unit_text=yield_unit_text
        )

        smart_data_model = new_yield.to_smart_data_model()
        send_to_context_broker("AgriYield", smart_data_model)
        return smart_data_model, 201

agri_carbon_footprint_model = ns_smart_data_models.model('AgriCarbonFootprint', {
    'has_agri_crop': fields.String(required=False, example="urn:ngsi-ld:AgriCrop:1ea0f120-4474-11e8-9919-672036642081"),
    'has_agri_parcel': fields.String(required=False, example="urn:ngsi-ld:AgriParcel:1ea0f120-4474-11e8-9919-672036642081"),
    'has_agri_yield': fields.String(required=False, example="urn:ngsi-ld:AgriYield:1ea0f120-4474-11e8-9919-672036642081"),
    'carbon_footprint_value': fields.Float(required=True, description='Carbon footprint value', example=5),
    'carbon_footprint_accuracy_percent': fields.Float(description='Carbon footprint accuracy percent', example=10),
    'carbon_footprint_min_value': fields.Float(description='Carbon footprint min value', example=30),
    'carbon_footprint_unit_text': fields.String(description='Carbon footprint measurement unit', example="Tons"),
    'estimation_start_at': fields.DateTime(required=True, description='Estimation start date', example="2017-01-01T01:20:00Z"),
    'estimation_end_at': fields.DateTime(required=True, description='Estimation end date', example="2017-01-01T01:20:00Z")
})


@ns_smart_data_models.doc(security='Bearer Auth')
@ns_smart_data_models.route('/agri_carbon_footprint')
class AgriCarbonFootprintResource(Resource):
    @api_key_required
    @ns_smart_data_models.expect(agri_carbon_footprint_model, validate=True)
    @ns_smart_data_models.response(201, 'AgriCarbonFootprint successfully created.')
    def post(self):
        carbon_footprint_data = request.get_json()

        carbon_footprint_value = carbon_footprint_data.get('carbon_footprint_value')
        carbon_footprint_accuracy_percent = carbon_footprint_data.get('carbon_footprint_accuracy_percent')
        carbon_footprint_min_value = carbon_footprint_data.get('carbon_footprint_min_value')
        carbon_footprint_unit_text = carbon_footprint_data.get('carbon_footprint_unit_text')
        estimation_start_at = carbon_footprint_data.get('estimation_start_at')
        estimation_end_at = carbon_footprint_data.get('estimation_end_at')

        error_messages = []
        if not carbon_footprint_value:
            error_messages.append("Carbon footprint value is missing")
        if not carbon_footprint_accuracy_percent:
            error_messages.append("Carbon footprint accuracy percent is missing")
        if not carbon_footprint_min_value:
            error_messages.append("Carbon footprint min value is missing")
        if not carbon_footprint_unit_text:
            error_messages.append("Carbon footprint unit text is missing")
        if not estimation_start_at:
            error_messages.append("Estimation start date is missing")
        if not estimation_end_at:
            error_messages.append("Estimation end date is missing")
        if error_messages:
            return jsonify({"errors": error_messages}), 400
        has_agri_crop = carbon_footprint_data.get('has_agri_crop')
        has_agri_parcel = carbon_footprint_data.get('has_agri_parcel')
        has_agri_yield = carbon_footprint_data.get('has_agri_yield')
        carbon_footprint_accuracy_percent = carbon_footprint_data.get('carbon_footprint_accuracy_percent')
        carbon_footprint_min_value = carbon_footprint_data.get('carbon_footprint_min_value')
        carbon_footprint_unit_text = carbon_footprint_data.get('carbon_footprint_unit_text')


        new_carbon_footprint_data = AgriCarbonFootPrint(
            has_agri_crop=has_agri_crop,
            has_agri_parcel=has_agri_parcel,
            has_agri_yield=has_agri_yield,
            carbon_footprint_value=carbon_footprint_value,
            carbon_footprint_accuracy_percent=carbon_footprint_accuracy_percent,
            carbon_footprint_min_value=carbon_footprint_min_value,
            carbon_footprint_unit_text=carbon_footprint_unit_text,
            estimation_start_at=estimation_start_at,
            estimation_end_at=estimation_end_at
        )

        smart_data_model = new_carbon_footprint_data.to_smart_data_model()
        send_to_context_broker("AgriCarbonFootPrint", smart_data_model)
        return smart_data_model, 201

