from datetime import datetime

from app.utils import generate_urn


ModelBase = object

class AgriSoil(ModelBase):
    """
        AgriSoil class represents a type of agricultural soil.
            
        Attributes:
            - name (str): The name of the soil.
            - date_created (datetime, optional): The date the record was created.
            - date_modified (datetime, optional): The date the record was last modified.
            - alternate_name (str, optional): An alternate name for the soil.
            - description (str, optional): A description of the soil.
            - agro_voc_concept (str, optional): An agricultural vocabulary concept associated with the soil.
            - see_also (str, optional): A related reference to the soil.
            - related_source (str, optional): A source related to the soil.
            - has_agri_product_type (str, optional): Represents the relationship with the agricultural product type.
    """

    
    def __init__(self, name, date_created=None, date_modified=None, alternate_name=None,
                 description=None, agro_voc_concept=None, see_also=None, related_source=None, 
                 has_agri_product_type=None):
        self.id = generate_urn("AgriSoil")
        self.type = "AgriSoil"   
        self.name = name
        self.date_created = date_created or datetime.utcnow()
        self.date_modified = date_modified or datetime.utcnow()
        self.alternate_name = alternate_name
        self.description = description
        self.agro_voc_concept = agro_voc_concept
        self.see_also = see_also
        self.related_source = related_source
        self.has_agri_product_type = has_agri_product_type

    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<AgriSoil {self.name}>'

    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.
        
        Returns:
            A dictionary representing the current Smart Data Model.
        """
        agri_soil_data = {
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
            "name":  {
                "value": self.name
            },
            "alternateName": {
                "value": self.alternate_name
            },
            "description": {
                "value": self.description
            },
            "agroVocConcept": {
                "type": "Property",
                "value": {
                    "@type": "URL",
                    "@value": self.agro_voc_concept
                }
            },
            "seeAlso": {
                "value": self.see_also.split(',') if isinstance(self.see_also, str) else self.see_also
            },
            "relatedSource": {
                "value": [
                    {
                        "application": self.related_source.split(',') if isinstance(self.related_source, str) else self.related_source,
                        "applicationEntityId": "app:soil1"
                    }
                ]
            },
            "hasAgriProductType": {
                "type": "Relationship",
                "object": self.has_agri_product_type.split(',') if isinstance(self.has_agri_product_type, str) else self.has_agri_product_type,
            },
        }

        return agri_soil_data


    def validate_smart_data_model(data):
        required_fields = ['dateCreated', 'dateModified', 'name']
        for field in required_fields:
            if field not in data:
                return False, f'Required "{field}" does not exist'
        return True, ''