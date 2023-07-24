from datetime import datetime

from app.utils import generate_urn


ModelBase = object

class AgriYield(ModelBase):
    """
        AgriYield class represents a record of agricultural yield.
            
        Attributes:
            - has_agri_crop (str, optional): Represents the relationship with the crop.
            - has_agri_parcel (str, optional): Represents the relationship with the agricultural parcel.
            - start_date_of_gathering_at (datetime): The start date of gathering.
            - end_date_of_gathering_at (datetime): The end date of gathering.
            - yield_value (float): The value of the yield.
            - yield_max_value (float, optional): The maximum value of the yield.
            - yield_min_value (float, optional): The minimum value of the yield.
            - yield_unit_text (str, optional): The unit of the yield measurement. Default is "Tons per hectare".
    """

    def __init__(self, start_date_of_gathering_at, end_date_of_gathering_at, yield_value,
                 has_agri_crop=None, has_agri_parcel=None, yield_max_value=None, yield_min_value=None,
                 yield_unit_text="Tons per hectare"):
        self.id = generate_urn("AgriYield")
        self.type = "AgriYield"   
        self.has_agri_crop = has_agri_crop
        self.has_agri_parcel = has_agri_parcel
        self.start_date_of_gathering_at = start_date_of_gathering_at
        self.end_date_of_gathering_at = end_date_of_gathering_at
        self.yield_value = yield_value
        self.yield_max_value = yield_max_value
        self.yield_min_value = yield_min_value
        self.yield_unit_text = yield_unit_text

    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<AgriYield {self.id}>'

    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.
        
        Returns:
            A dictionary representing the current Smart Data Model.
        """
        agri_yield_data = {
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
            "startDateOfGatheringAt": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.start_date_of_gathering_at
                }
            },
            "endDateOfGatheringAt": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.end_date_of_gathering_at
                }
            },
            "yield":{
                "type": "Property",
                "value": {
                    "value": self.yield_value,
                    "maxValue": self.yield_max_value,
                    "minValue": self.yield_min_value,
                    "unitText": self.yield_unit_text
                }
            }
        }
        return agri_yield_data

    def validate_smart_data_model(data):
        required_fields = ['startDateOfGatheringAt', 'endDateOfGatheringAt', 'yield']
        for field in required_fields:
            print(field)
            if field not in data:
                return False, f'Required "{field}" does not exist'
        return True, ''