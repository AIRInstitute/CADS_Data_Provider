from datetime import datetime

from app.utils import generate_urn


ModelBase = object

class AgriCarbonFootPrint(ModelBase):
    """
        AgriCarbonFootPrint class represents a record of the carbon footprint of agricultural activities.
            
        Attributes:
            - has_agri_crop (str, optional): Represents the relationship with the crop.
            - has_agri_parcel (str, optional): Represents the relationship with the agricultural parcel.
            - has_agri_yield (str, optional): Represents the relationship with the agricultural yield.
            - carbon_footprint_value (float): The value of the carbon footprint.
            - carbon_footprint_accuracy_percent (float, optional): The accuracy percentage of the carbon footprint value.
            - carbon_footprint_min_value (float, optional): The minimum value of the carbon footprint.
            - carbon_footprint_unit_text (str, optional): The unit of the carbon footprint measurement. Default is "Tons".
            - estimation_start_at (datetime): The start date of the estimation period.
            - estimation_end_at (datetime): The end date of the estimation period.
    """

    def __init__(self, carbon_footprint_value, estimation_start_at, estimation_end_at,
                 has_agri_crop=None, has_agri_parcel=None, has_agri_yield=None,
                 carbon_footprint_accuracy_percent=None, carbon_footprint_min_value=None,
                 carbon_footprint_unit_text="Tons"):
        self.id = generate_urn("AgriCarbonFootprint")
        self.type = "AgriCarbonFootprint"
        self.has_agri_crop = has_agri_crop
        self.has_agri_parcel = has_agri_parcel
        self.has_agri_yield = has_agri_yield
        self.carbon_footprint_value = carbon_footprint_value
        self.carbon_footprint_accuracy_percent = carbon_footprint_accuracy_percent
        self.carbon_footprint_min_value = carbon_footprint_min_value
        self.carbon_footprint_unit_text = carbon_footprint_unit_text
        self.estimation_start_at = estimation_start_at
        self.estimation_end_at = estimation_end_at

    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<AgriCarbonFootPrint {self.id}>'

    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.
        
        Returns:
            A dictionary representing the current Smart Data Model.
        """
        agri_carbon_footprint_data = {
            "id": self.id,
            "type": self.type,
            "hasAgriCrop": {
                "type": "Relationship",
                "object": self.has_agri_crop
            },
            "hasAgriParcel": {
                "type": "Relationship",
                "object": self.has_agri_parcel
            },
            "hasAgriYield": {
                "type": "Relationship",
                "object": self.has_agri_yield
            },
            "carbonFootprint": {
                "type": "Property",
                "value": {
                    "value": self.carbon_footprint_value,
                    "accuracyPercent": self.carbon_footprint_accuracy_percent,
                    "minValue": self.carbon_footprint_min_value,
                    "unitText": self.carbon_footprint_unit_text
                }
            },
            "estimationStartAt": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.estimation_start_at
                }
            },
            "estimationEndAt": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.estimation_end_at
                }
            }
        }
        return agri_carbon_footprint_data


    def validate_smart_data_model(data):
            required_fields = ['carbonFootprint', 'estimationStartAt', 'estimationEndAt']
            for field in required_fields:
                if field not in data:
                    return False, f'Required "{field}" does not exist'
            return True, ''