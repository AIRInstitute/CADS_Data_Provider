from datetime import datetime

from app.utils import generate_urn


ModelBase = object

class AgriSoilState(ModelBase):
    """
        AgriSoilState class represents a record of the state of agricultural soil.
            
        Attributes:
            - date_of_measurement (datetime): The date when the measurements were taken.
            - acidity (float): The acidity of the soil.
            - acidity_unit (str): The unit of the acidity measurement.
            - acidity_timestamp (str): The timestamp when the acidity was measured.
            - humus (float): The amount of humus in the soil.
            - humus_unit (str): The unit of the humus measurement.
            - humus_timestamp (str): The timestamp when the humus level was measured.
            - electrical_conductivity (float, optional): The electrical conductivity of the soil.
            - density (float, optional): The density of the soil.
            - has_agri_soil (str, optional): Represents the relationship with the soil.
            - has_agri_parcel (str, optional): Represents the relationship with the agricultural parcel.
            - has_agri_greenhouse (str, optional): Represents the relationship with the greenhouse.
            - date_created (datetime, optional): The date the record was created.
            - date_modified (datetime, optional): The date the record was last modified.
            - electrical_conductivity_unit (str, optional): The unit of the electrical conductivity measurement.
            - electrical_conductivity_timestamp (str, optional): The timestamp when the electrical conductivity was measured.
            - density_unit (str, optional): The unit of the density measurement.
            - density_timestamp (str, optional): The timestamp when the density was measured.
    """
    
    def __init__(self, date_of_measurement, acidity, acidity_unit, acidity_timestamp,  humus, humus_unit, humus_timestamp, electrical_conductivity=None, density=None,
                 has_agri_soil=None, has_agri_parcel=None, has_agri_greenhouse=None, date_created=None, date_modified=None,
                 electrical_conductivity_unit=None, electrical_conductivity_timestamp=None,
                 density_unit=None, density_timestamp=None):    
        self.id = generate_urn("AgriSoilState")
        self.type = "AgriSoilState"       
        self.date_created = date_created or datetime.utcnow()
        self.date_modified = date_modified or datetime.utcnow()
        self.date_of_measurement = date_of_measurement
        self.acidity = acidity
        self.acidity_unit = acidity_unit
        self.acidity_timestamp = acidity_timestamp
        self.humus = humus
        self.electrical_conductivity = electrical_conductivity
        self.electrical_conductivity_unit = electrical_conductivity_unit
        self.electrical_conductivity_timestamp = electrical_conductivity_timestamp
        self.density = density
        self.has_agri_soil = has_agri_soil
        self.has_agri_parcel = has_agri_parcel
        self.has_agri_greenhouse = has_agri_greenhouse
        self.humus_unit = humus_unit
        self.humus_timestamp = humus_timestamp
        self.density_unit = density_unit
        self.density_timestamp = density_timestamp


    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<AgriSoilState {self.id}>'

    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.
        
        Returns:
            A dictionary representing the current Smart Data Model.
        """
        agri_soil_state_data = {
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
            "dateOfMeasurement": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.date_of_measurement
                }
            },
            "acidity": {
                "type": "Property",
                "value": self.acidity,
                "unitCode":  self.acidity_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                        "@value": self.acidity_timestamp
                    }
                }
            },
            "electricalConductivity": {
                "type": "Property",
                "value": self.electrical_conductivity,
                "unitCode":  self.electrical_conductivity_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                        "@value": self.electrical_conductivity_timestamp
                    }
                }
            },
            "density":  {
                "type": "Property",
                "value": self.density,
                "unitCode":  self.density_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                        "@value": self.density_timestamp
                    }
                }
            },
            "humus": {
                "type": "Property",
                "value": self.humus,
                "unitCode":  self.humus_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                        "@value": self.humus_timestamp
                    }
                }
            },
            "hasAgriSoil": {
                "type": "Relationship",
                "object": self.has_agri_soil
            },
            "hasAgriParcel": {
                "type": "Relationship",
                "object": self.has_agri_parcel
            },
             "hasAgriGreenhouse": {
                "type": "Relationship",
                "object": self.has_agri_greenhouse
            } 
        }

        return agri_soil_state_data

    def validate_smart_data_model(data):
        required_fields = ['dateCreated', 'dateModified', 'dateOfMeasurement', 'acidity', 'humus']
        for field in required_fields:
            print(field)
            if field not in data:
                return False, f'Required "{field}" does not exist'
        return True, ''