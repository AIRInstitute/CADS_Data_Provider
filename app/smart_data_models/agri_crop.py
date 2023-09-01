from datetime import datetime

from app.utils import generate_urn


ModelBase = object

class AgriCrop(ModelBase):
    """
        AgriCrop class represents an agricultural crop with its related properties.
        
        Attributes:
            - name (str): The name of the crop.
            - has_agri_soil (AgriSoil): An instance of the AgriSoil class representing the soil associated with this crop.
            - planting_from (datetime): The date when planting of this crop started.
            - date_created (datetime, optional): The date when the instance of this class was created, defaults to current datetime.
            - date_modified (datetime, optional): The date when the instance of this class was last modified, defaults to current datetime.
            - alternate_name (str, optional): An alternate name for the crop.
            - agro_voc_concept (str, optional): A link to the related AGROVOC concept.
            - see_also (str, optional): Other related links.
            - description (str, optional): A description of the crop.
            - related_source (str, optional): A source related to the crop.
            - has_agri_fertiliser (AgriFertiliser, optional): An instance of the AgriFertiliser class associated with this crop.
            - has_agri_pest (AgriPest, optional): An instance of the AgriPest class associated with this crop.
            - harvesting_interval (int, optional): The interval between successive harvests of this crop in days.
            - watering_frequency (int, optional): The frequency at which the crop should be watered in days.
    """
    
    def __init__(self, id, name, has_agri_soil, planting_from, date_created=None, date_modified=None,
                 alternate_name=None, agro_voc_concept=None, see_also=None, description=None,
                 related_source=None, has_agri_fertiliser=None, has_agri_pest=None,
                 harvesting_interval=None, watering_frequency=None):
        self.id = id
        self.type = "AgriCrop"
        self.name = name
        self.date_created = date_created or datetime.utcnow()
        self.date_modified = date_modified or datetime.utcnow()
        self.alternate_name = alternate_name
        self.agro_voc_concept = agro_voc_concept
        self.see_also = see_also
        self.description = description
        self.related_source = related_source
        self.has_agri_soil = has_agri_soil
        self.has_agri_fertiliser = has_agri_fertiliser
        self.has_agri_pest = has_agri_pest
        self.planting_from = planting_from
        self.harvesting_interval = harvesting_interval
        self.watering_frequency = watering_frequency

    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<AgriCrop {self.name}>'

    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.

        Returns:
            A dictionary representing the current Smart Data Model.
        """
        agri_crop_data = {
            "id": self.id,
            "type": self.type
        }

        if self.date_created:
            agri_crop_data["dateCreated"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.date_created
                }
            }

        if self.date_modified:
            agri_crop_data["dateModified"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.date_modified
                }
            }

        if self.name:
            agri_crop_data["name"] = self.name

        if self.alternate_name:
            agri_crop_data["alternateName"] = self.alternate_name

        if self.agro_voc_concept:
            agri_crop_data["agroVocConcept"] = {
                "type": "Property",
                "value": {
                    "@type": "URL",
                    "@value": self.agro_voc_concept
                }
            }

        if self.description:
            agri_crop_data["description"] = {
                "value": self.description
            }

        if self.related_source:
            agri_crop_data["relatedSource"] = {
                "value": [
                    {
                        "application": self.related_source,
                        "applicationEntityId": "app:crop1"
                    }
                ]
            }

        if self.has_agri_soil:
            agri_crop_data["hasAgriSoil"] = {
                "type": "Relationship",
                "object": self.has_agri_soil.split(',') if isinstance(self.has_agri_soil, str) else self.has_agri_soil
            }

        if self.has_agri_fertiliser:
            agri_crop_data["hasAgriFertiliser"] = {
                "type": "Relationship",
                "object": self.has_agri_fertiliser.split(',') if isinstance(self.has_agri_fertiliser, str) else self.has_agri_fertiliser
            }

        if self.has_agri_pest:
            agri_crop_data["hasAgriPest"] = {
                "type": "Relationship",
                "object": self.has_agri_pest.split(',') if isinstance(self.has_agri_pest, str) else self.has_agri_pest
            }

        if self.planting_from:
            agri_crop_data["plantingFrom"] = {"value": self.planting_from}

        if self.harvesting_interval:
            agri_crop_data["harvestingInterval"] = {"value": self.harvesting_interval}

        if self.watering_frequency:
            agri_crop_data["wateringFrequency"] = {"value": self.watering_frequency}

        return agri_crop_data



    def validate_smart_data_model(data):
        required_fields = ['dateCreated', 'dateModified', 'name', 'hasAgriSoil', 'plantingFrom']
        for field in required_fields:
            if field not in data:
                return False, f'Required "{field}" does not exist'
        return True, ''