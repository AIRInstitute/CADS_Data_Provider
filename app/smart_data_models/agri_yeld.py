from datetime import datetime

from app.utils import generate_urn


ModelBase = object

class AgriYeld(ModelBase):
    """
        AgriYeld class represents a record of agricultural yeld.
            
        Attributes:
            - has_agri_crop (str, optional): Represents the relationship with the crop.
            - has_agri_parcel (str, optional): Represents the relationship with the agricultural parcel.
            - start_date_of_gathering_at (datetime): The start date of gathering.
            - end_date_of_gathering_at (datetime): The end date of gathering.
            - yeld_value (float): The value of the yeld.
            - yeld_max_value (float, optional): The maximum value of the yeld.
            - yeld_min_value (float, optional): The minimum value of the yeld.
            - yeld_unit_text (str, optional): The unit of the yeld measurement. Default is "Tons per hectare".
    """

    def __init__(self, id, start_date_of_gathering_at, end_date_of_gathering_at, yeld_value,
                 has_agri_crop=None, has_agri_parcel=None, yeld_max_value=None, yeld_min_value=None,
                 yeld_unit_text="Tons per hectare"):
        self.id = id
        self.type = "AgriYeld"   
        self.has_agri_crop = has_agri_crop
        self.has_agri_parcel = has_agri_parcel
        self.start_date_of_gathering_at = start_date_of_gathering_at
        self.end_date_of_gathering_at = end_date_of_gathering_at
        self.yeld_value = yeld_value
        self.yeld_max_value = yeld_max_value
        self.yeld_min_value = yeld_min_value
        self.yeld_unit_text = yeld_unit_text

    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<AgriYeld {self.id}>'

    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.
        
        Returns:
            A dictionary representing the current Smart Data Model.
        """
        agri_yeld_data = {
            "id": self.id,
            "type": self.type
        }

        if self.has_agri_crop:
            agri_yeld_data["hasAgriCrop"] = {
                "type": "Relationship",
                "object": self.has_agri_crop
            }

        if self.has_agri_parcel:
            agri_yeld_data["hasAgriParcel"] = {
                "type": "Relationship",
                "object": self.has_agri_parcel
            }

        if self.start_date_of_gathering_at:
            agri_yeld_data["startDateOfGatheringAt"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.start_date_of_gathering_at
                }
            }

        if self.end_date_of_gathering_at:
            agri_yeld_data["endDateOfGatheringAt"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.end_date_of_gathering_at
                }
            }

        if self.yeld_value or self.yeld_max_value or self.yeld_min_value or self.yeld_unit_text:
            yeld_data = {"type": "Property", "value": {}}
            if self.yeld_value:
                yeld_data["value"]["value"] = self.yeld_value
            if self.yeld_max_value:
                yeld_data["value"]["maxValue"] = self.yeld_max_value
            if self.yeld_min_value:
                yeld_data["value"]["minValue"] = self.yeld_min_value
            if self.yeld_unit_text:
                yeld_data["value"]["unitText"] = self.yeld_unit_text
            agri_yeld_data["yeld"] = yeld_data

        return agri_yeld_data


    def validate_smart_data_model(data):
        required_fields = ['startDateOfGatheringAt', 'endDateOfGatheringAt', 'yeld']
        for field in required_fields:
            if field not in data:
                return False, f'Required "{field}" does not exist'
        return True, ''