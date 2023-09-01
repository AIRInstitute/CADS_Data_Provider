from datetime import datetime

from app.utils import generate_urn


ModelBase = object

class AgriCarbonFootPrint(ModelBase):
    """
        AgriCarbonFootPrint class represents a record of the carbon footprint of agricultural activities.
            
        Attributes:
            - has_agri_crop (str, optional): Represents the relationship with the crop.
            - has_agri_parcel (str, optional): Represents the relationship with the agricultural parcel.
            - has_agri_yeld (str, optional): Represents the relationship with the agricultural yeld.
            - carbon_footprint_value (float): The value of the carbon footprint.
            - carbon_footprint_accuracy_percent (float, optional): The accuracy percentage of the carbon footprint value.
            - carbon_footprint_min_value (float, optional): The minimum value of the carbon footprint.
            - carbon_footprint_unit_text (str, optional): The unit of the carbon footprint measurement. Default is "Tons".
            - estimation_start_at (datetime): The start date of the estimation period.
            - estimation_end_at (datetime): The end date of the estimation period.
    """

    def __init__(self, id, carbon_footprint_value, estimation_start_at, estimation_end_at,
                 has_agri_crop=None, has_agri_parcel=None, has_agri_yeld=None,
                 carbon_footprint_accuracy_percent=None, carbon_footprint_min_value=None,
                 carbon_footprint_unit_text="Tons"):
        self.id = id
        self.type = "AgriCarbonFootprint"
        self.has_agri_crop = has_agri_crop
        self.has_agri_parcel = has_agri_parcel
        self.has_agri_yeld = has_agri_yeld
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
        }
        if self.has_agri_crop:
            agri_carbon_footprint_data["hasAgriCrop"] = {
                "type": "Relationship",
                "object": self.has_agri_crop
            }

        if self.has_agri_parcel:
            agri_carbon_footprint_data["hasAgriParcel"] = {
                "type": "Relationship",
                "object": self.has_agri_parcel
            }

        if self.has_agri_yeld:
            agri_carbon_footprint_data["hasAgriYeld"] = {
                "type": "Relationship",
                "object": self.has_agri_yeld
            }

        if self.carbon_footprint_value:
            agri_carbon_footprint_data["carbonFootprint"] = {
                "type": "Property",
                "value": {
                    "value": self.carbon_footprint_value,
                    "accuracyPercent": self.carbon_footprint_accuracy_percent,
                    "minValue": self.carbon_footprint_min_value,
                    "unitText": self.carbon_footprint_unit_text
                }
            }

        if self.estimation_start_at:
            agri_carbon_footprint_data["estimationStartAt"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.estimation_start_at
                }
            }

        if self.estimation_end_at:
            agri_carbon_footprint_data["estimationEndAt"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.estimation_end_at
                }
            }
        return agri_carbon_footprint_data


    def validate_smart_data_model(data):
            required_fields = ['carbonFootprint', 'estimationStartAt', 'estimationEndAt']
            for field in required_fields:
                if field not in data:
                    return False, f'Required "{field}" does not exist'
            return True, ''