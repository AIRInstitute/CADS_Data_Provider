from datetime import datetime

ModelBase = object


class Person(ModelBase):
    """
        Person class represents a record of a person.
        
        Attributes:
            - additionalName (str, optional): An additional name for a person.
            - address (str, optional): The mailing address.
            - alternateName (str, optional): An alternate name for this item.
            - areaServed (str, optional): The geographic area where a service is provided.
            - dataProvider (str, optional): Identifier for the provider of the data.
            - dateCreated (datetime, optional): Entity creation timestamp.
            - dateModified (datetime, optional): Timestamp of the last entity modification.
            - description (str, optional): A description of this item.
            - email (str, optional): Email address of owner.
            - familyName (str, optional): Family name.
            - givenName (str, optional): Given name.
            - id (str): Unique identifier of the entity.
            - location (str, optional): Geojson reference to the item.
            - name (str, optional): Name of this item.
            - owner (list, optional): List of unique IDs of the owner(s).
            - seeAlso (str, optional): List of URIs pointing to additional resources about the item.
            - source (str, optional): Original source of the entity data as a URL.
            - telephone (str, optional): Telephone number.
            - type (str): Type of data model.
    """

    def __init__(self, id, type, additionalName=None, address=None, alternateName=None, 
                 areaServed=None, dataProvider=None, dateCreated=None, dateModified=None, 
                 description=None, email=None, familyName=None, givenName=None, 
                 location=None, name=None, owner=None, seeAlso=None, 
                 source=None, telephone=None):
        self.id = id
        self.type = type
        self.additionalName = additionalName
        self.address = address
        self.alternateName = alternateName
        self.areaServed = areaServed
        self.dataProvider = dataProvider
        self.dateCreated = dateCreated
        self.dateModified = dateModified
        self.description = description
        self.email = email
        self.familyName = familyName
        self.givenName = givenName
        self.location = location
        self.name = name
        self.owner = owner
        self.seeAlso = seeAlso
        self.source = source
        self.telephone = telephone

    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<Person {self.id}>'

    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.
        
        Returns:
            A dictionary representing the current Smart Data Model.
        """
        person_data = {
            "id": self.id,
            "type": self.type
        }
        
        if self.additionalName:
            person_data["additionalName"] = {
                "type": "Property",
                "value": self.additionalName
            }

        if self.address:
            person_data["address"] = {
                "type": "Property",
                "value": self.address
            }

        if self.alternateName:
            person_data["alternateName"] = {
                "type": "Property",
                "value": self.alternateName
            }

        if self.areaServed:
            person_data["areaServed"] = {
                "type": "Property",
                "value": self.areaServed
            }

        if self.dataProvider:
            person_data["dataProvider"] = {
                "type": "Property",
                "value": self.dataProvider
            }

        if self.dateCreated:
            person_data["dateCreated"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.dateCreated.isoformat()
                }
            }

        if self.dateModified:
            person_data["dateModified"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.dateModified.isoformat()
                }
            }

        if self.description:
            person_data["description"] = {
                "type": "Property",
                "value": self.description
            }

        if self.email:
            person_data["email"] = {
                "type": "Property",
                "value": self.email
            }

        if self.familyName:
            person_data["familyName"] = {
                "type": "Property",
                "value": self.familyName
            }

        if self.givenName:
            person_data["givenName"] = {
                "type": "Property",
                "value": self.givenName
            }

        if self.location:
            person_data["location"] = {
                "type": "GeoProperty",
                "value": self.location
            }

        if self.name:
            person_data["name"] = {
                "type": "Property",
                "value": self.name
            }

        if self.owner:
            person_data["owner"] = {
                "type": "Property",
                "value": self.owner
            }

        if self.seeAlso:
            person_data["seeAlso"] = {
                "type": "Property",
                "value": self.seeAlso
            }

        if self.source:
            person_data["source"] = {
                "type": "Property",
                "value": self.source
            }

        if self.telephone:
            person_data["telephone"] = {
                "type": "Property",
                "value": self.telephone
            }

        return person_data


    @staticmethod
    def validate_smart_data_model(data):
        required_fields = ['id', 'type']
        for field in required_fields:
            if field not in data:
                return False, f'Required "{field}" does not exist'
        return True, ''

