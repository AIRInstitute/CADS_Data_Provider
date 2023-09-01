from datetime import datetime

from app.utils import generate_urn

ModelBase = object

class AgriApp(ModelBase):
    """
        AgriApp class represents a record of an agricultural application.
        
        Attributes:
            - address (str, optional): Address of the app.
            - alternateName (str, optional): Alternate name of the app.
            - areaServed (str, optional): Area where the app is served.
            - category (str, optional): Category of the app.
            - dataProvider (str, optional): Data provider for the app.
            - dateCreated (datetime, optional): Date when the app was created.
            - dateModified (datetime, optional): Date when the app was last modified.
            - description (str, optional): Description of the app.
            - endpoint (str, optional): Endpoint for accessing the app.
            - hasProvider (str, optional): Provider of the app.
            - id (str): ID of the app.
            - location (str, optional): Location where the app is primarily used.
            - name (str, optional): Name of the app.
            - owner (str, optional): Owner of the app.
            - relatedSource (str, optional): Related source for the app.
            - seeAlso (str, optional): Further information for the app.
            - source (str, optional): Source from where the app originated.
            - type (str): Type of data model.
            - version (str, optional): Version of the app.
    """

    def __init__(self, id, type, address=None, alternateName=None, areaServed=None, 
                 category=None, dataProvider=None, dateCreated=None, dateModified=None,
                 description=None, endpoint=None, hasProvider=None, location=None,
                 name=None, owner=None, relatedSource=None, seeAlso=None,
                 source=None, version=None):
        self.id = id
        self.type = type
        self.address = address
        self.alternateName = alternateName
        self.areaServed = areaServed
        self.category = category
        self.dataProvider = dataProvider
        self.dateCreated = dateCreated
        self.dateModified = dateModified
        self.description = description
        self.endpoint = endpoint
        self.hasProvider = hasProvider
        self.location = location
        self.name = name
        self.owner = owner
        self.relatedSource = relatedSource
        self.seeAlso = seeAlso
        self.source = source
        self.version = version

    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<AgriApp {self.id}>'

    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.
        
        Returns:
            A dictionary representing the current Smart Data Model.
        """
        agri_app_data = {
            "id": self.id,
            "type": self.type
        }
        
        if self.address:
            agri_app_data["address"] = {
                "type": "Property",
                "value": self.address
            }

        if self.alternateName:
            agri_app_data["alternateName"] = {
                "type": "Property",
                "value": self.alternateName
            }

        if self.areaServed:
            agri_app_data["areaServed"] = {
                "type": "Property",
                "value": self.areaServed
            }

        if self.category:
            agri_app_data["category"] = {
                "type": "Property",
                "value": self.category
            }

        if self.dataProvider:
            agri_app_data["dataProvider"] = {
                "type": "Property",
                "value": self.dataProvider
            }

        if self.dateCreated:
            agri_app_data["dateCreated"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.dateCreated.isoformat()
                }
            }

        if self.dateModified:
            agri_app_data["dateModified"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.dateModified.isoformat()
                }
            }

        if self.description:
            agri_app_data["description"] = {
                "type": "Property",
                "value": self.description
            }

        if self.endpoint:
            agri_app_data["endpoint"] = {
                "type": "Property",
                "value": self.endpoint
            }

        if self.hasProvider:
            agri_app_data["hasProvider"] = {
                "type": "Relationship",
                "object": self.hasProvider
            }

        if self.location:
            agri_app_data["location"] = {
                "type": "Property",
                "value": self.location
            }

        if self.name:
            agri_app_data["name"] = {
                "type": "Property",
                "value": self.name
            }

        if self.owner:
            agri_app_data["owner"] = {
                "type": "Property",
                "value": self.owner
            }

        if self.relatedSource:
            agri_app_data["relatedSource"] = {
                "type": "Property",
                "value": self.relatedSource
            }

        if self.seeAlso:
            agri_app_data["seeAlso"] = {
                "type": "Property",
                "value": self.seeAlso
            }

        if self.source:
            agri_app_data["source"] = {
                "type": "Property",
                "value": self.source
            }

        if self.version:
            agri_app_data["version"] = {
                "type": "Property",
                "value": self.version
            }
        
        return agri_app_data


    @staticmethod
    def validate_smart_data_model(data):
        required_fields = ['id', 'type']
        for field in required_fields:
            if field not in data:
                return False, f'Required "{field}" does not exist'
        return True, ''
