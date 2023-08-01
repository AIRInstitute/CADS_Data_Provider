from datetime import datetime

from app.utils import generate_urn


ModelBase = object

class AgriGreenHouse(ModelBase):
    """
        AgriGreenhouse class represents a greenhouse in agriculture.
        
        Attributes:
            date_created (datetime): The creation date of this instance, defaults to current datetime.
            date_modified (datetime): The last modification date of this instance, defaults to current datetime.
            owned_by (str, optional): The entity that owns the greenhouse.
            related_source (str, optional): A source related to the greenhouse.
            see_also (str, optional): Other related links.
            belongs_to (str, optional): The larger entity the greenhouse belongs to.
            has_agri_parcel_parent (str, optional): The parent agricultural parcel of the greenhouse.
            has_agri_parcel_children (str, optional): The child agricultural parcels of the greenhouse.
            has_weather_observed (str, optional): The observed weather of the greenhouse.
            has_water_quality_observed (str, optional): The observed water quality of the greenhouse.
            relative_humidity (float): The relative humidity in the greenhouse.
            leaf_temperature (float, optional): The leaf temperature in the greenhouse.
            co2 (float): The CO2 level in the greenhouse.
            daily_light (float, optional): The daily light in the greenhouse.
            drain_flow (float, optional): The drain flow in the greenhouse.
            drain_flow_max_value (float, optional): The maximum drain flow in the greenhouse.
            drain_flow_min_value (float, optional): The minimum drain flow in the greenhouse.
            has_device (str, optional): The device associated with the greenhouse.
    """
    def __init__(self, relative_humidity, co2, owned_by=None, related_source=None, see_also=None, belongs_to=None,
                 has_agri_parcel_parent=None, has_agri_parcel_children=None, has_weather_observed=None,
                 has_water_quality_observed=None, leaf_temperature=None, daily_light=None, drain_flow=None, drain_flow_max_value=None, 
                 drain_flow_min_value=None, has_device=None, date_created=None, date_modified=None):
        self.id = generate_urn("AgriGreenHouse")
        self.type = "AgriGreenHouse"
        self.date_created = date_created or datetime.utcnow()
        self.date_modified = date_modified or datetime.utcnow()
        self.owned_by = owned_by
        self.related_source = related_source
        self.see_also = see_also
        self.belongs_to = belongs_to
        self.has_agri_parcel_parent = has_agri_parcel_parent
        self.has_agri_parcel_children = has_agri_parcel_children
        self.has_weather_observed = has_weather_observed
        self.has_water_quality_observed = has_water_quality_observed
        self.relative_humidity = relative_humidity
        self.leaf_temperature = leaf_temperature
        self.co2 = co2
        self.daily_light = daily_light
        self.drain_flow = drain_flow
        self.drain_flow_max_value = drain_flow_max_value
        self.drain_flow_min_value = drain_flow_min_value
        self.has_device = has_device

    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<AgriGreenhouse {self.id}>'

    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.
        
        Returns:
            A dictionary representing the current Smart Data Model.
        """
        agri_greenhouse_data = {
            "id": self.id,
            "type": self.type,
            "dateCreated": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.date_created
                }
            },
            "dateModified": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.date_modified
                }
            },
            "ownedBy": {
                "type": "Relationship",
                "object": self.owned_by
            },
            "relatedSource": {
                "value": [
                    {
                        "application": self.related_source,
                        "applicationEntityId": "app:greenhouse1"
                    }
                ]
            },
            "seeAlso":  {
                "type": "Relationship",
                "object": self.see_also.split(',') if isinstance(self.see_also, str) else self.see_also
            },
            "belongsTo":  self.belongs_to,       
            "hasAgriParcelParent":  {
                "type": "Relationship",
                "object": self.has_agri_parcel_parent.split(',') if isinstance(self.has_agri_parcel_parent, str) else self.has_agri_parcel_parent
            },
            "hasAgriParcelChildren":  {
                "type": "Relationship",
                "object": self.has_agri_parcel_children.split(',') if isinstance(self.has_agri_parcel_children, str) else self.has_agri_parcel_children
            },
            "hasWeatherObserved": {
                "type": "Relationship",
                "object": self.has_weather_observed.split(',') if isinstance(self.has_weather_observed, str) else self.has_weather_observed
            },
            "hasWaterQualityObserved":{
                "type": "Relationship",
                "object": self.has_water_quality_observed.split(',') if isinstance(self.has_water_quality_observed, str) else self.has_water_quality_observed
            },
            "relativeHumidity": {
                "type": "Property",
                "value": self.relative_humidity
            },
            "leafTemperature": {
                "type": "Property",
                "value": self.leaf_temperature
            },
            "co2": {
                "type": "Property",
                "value": self.co2
            },
            "dailyLight": {
                "type": "Property",
                "value": self.daily_light
            },
            "drainFlow": {
                "type": "Property",
                "value": { 
                    "value": self.drain_flow,
                    "maxValue": self.drain_flow_max_value, 
                    "minValue": self.drain_flow_min_value
                }
            },
            "hasDevice":  {
                "type": "Relationship",
                "object": self.has_device.split(',') if isinstance(self.has_device, str) else self.has_device
            }
        }

        return agri_greenhouse_data

    def validate_smart_data_model(data):
        required_fields = ['dateCreated', 'dateModified', 'relativeHumidity', 'co2']
        for field in required_fields:
            if field not in data:
                return False, f'Required "{field}" does not exist'
        return True, ''   