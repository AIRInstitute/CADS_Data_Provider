from datetime import datetime

from app.utils import generate_urn 

ModelBase = object

class Building(ModelBase):
    """
    Building class represents a record of a building.
    
    Attributes:
        - address (object): The mailing address.
        - alternateName (str, optional): An alternative name for this item.
        - areaServed (str, optional): The geographic area where a service or offered item is provided.
        - category (list of str): Category of the building.
        - collapseRisk (float, optional): Probability of total collapse of the building.
        - containedInPlace (object, optional): Geojson reference to the item.
        - dataProvider (str, optional): Identifier for the data provider.
        - dateCreated (str, optional): Entity creation timestamp.
        - dateModified (str, optional): Timestamp of the last modification.
        - description (str, optional): Description of the item.
        - floorsAboveGround (int, optional): Floors above ground.
        - floorsBelowGround (int, optional): Floors below ground.
        - id (str): Unique identifier.
        - location (object, optional): Geojson reference to the item.
        - name (str, optional): Name of the item.
        - occupier (list of str, optional): Person or entity using the building.
        - openingHours (list of str, optional): Opening hours of the building.
        - owner (list of str): List of owner ids.
        - peopleCapacity (float, optional): Allowed people present.
        - peopleOccupancy (float, optional): People present at the building.
        - refMap (object, optional): Reference to the map containing the building.
        - seeAlso (object, optional): URIs pointing to additional resources.
        - source (str, optional): Original source of entity data as URL.
        - type (str): NGSI Entity type.
    """
    
    # This function initialization needs to be adjusted according to the attributes above
    def __init__(self, id, type, address, category, alternateName=None, areaServed=None, 
                 collapseRisk=None, containedInPlace=None, dataProvider=None, 
                 dateCreated=None, dateModified=None, description=None, 
                 floorsAboveGround=None, floorsBelowGround=None, location=None, name=None,
                 occupier=None, openingHours=None, owner=None, peopleCapacity=None,
                 peopleOccupancy=None, refMap=None, seeAlso=None, source=None):
        self.id = id
        self.type = type
        self.address = address
        self.category = category
        self.alternateName = alternateName
        self.areaServed = areaServed
        self.collapseRisk = collapseRisk
        self.containedInPlace = containedInPlace
        self.dataProvider = dataProvider
        self.dateCreated = dateCreated
        self.dateModified = dateModified
        self.description = description
        self.floorsAboveGround = floorsAboveGround
        self.floorsBelowGround = floorsBelowGround
        self.location = location
        self.name = name
        self.occupier = occupier
        self.openingHours = openingHours
        self.owner = owner
        self.peopleCapacity = peopleCapacity
        self.peopleOccupancy = peopleOccupancy
        self.refMap = refMap
        self.seeAlso = seeAlso
        self.source = source

    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<Building {self.id}>'

    def to_smart_data_model(self):
        """
        Convert the current object into a dictionary adhering to the Smart Data Model standard.
        Returns a dictionary representing the current Smart Data Model.
        """
        building_data = {
            "id": self.id,
            "type": self.type,
            "address": {
                "type": "Property",
                "value": self.address
            },
            "category": {
                "type": "Property",
                "value": self.category
            }
        }
        
        if self.alternateName:
            building_data["alternateName"] = {
                "type": "Property",
                "value": self.alternateName
            }

        if self.areaServed:
            building_data["areaServed"] = {
                "type": "Property",
                "value": self.areaServed
            }

        if self.collapseRisk is not None:
            building_data["collapseRisk"] = {
                "type": "Property",
                "value": self.collapseRisk
            }

        if self.containedInPlace:
            building_data["containedInPlace"] = {
                "type": "Property",
                "value": self.containedInPlace
            }

        if self.dataProvider:
            building_data["dataProvider"] = {
                "type": "Property",
                "value": self.dataProvider
            }

        if self.dateCreated:
            building_data["dateCreated"] = {
                "type": "Property",
                "value": self.dateCreated
            }

        if self.dateModified:
            building_data["dateModified"] = {
                "type": "Property",
                "value": self.dateModified
            }

        if self.description:
            building_data["description"] = {
                "type": "Property",
                "value": self.description
            }

        if self.floorsAboveGround is not None:
            building_data["floorsAboveGround"] = {
                "type": "Property",
                "value": self.floorsAboveGround
            }

        if self.floorsBelowGround is not None:
            building_data["floorsBelowGround"] = {
                "type": "Property",
                "value": self.floorsBelowGround
            }

        if self.location:
            building_data["location"] = {
                "type": "Property",
                "value": self.location
            }

        if self.name:
            building_data["name"] = {
                "type": "Property",
                "value": self.name
            }

        if self.occupier:
            building_data["occupier"] = {
                "type": "Property",
                "value": self.occupier
            }

        if self.openingHours:
            building_data["openingHours"] = {
                "type": "Property",
                "value": self.openingHours
            }

        if self.owner:
            building_data["owner"] = {
                "type": "Property",
                "value": self.owner
            }

        if self.peopleCapacity is not None:
            building_data["peopleCapacity"] = {
                "type": "Property",
                "value": self.peopleCapacity
            }

        if self.peopleOccupancy is not None:
            building_data["peopleOccupancy"] = {
                "type": "Property",
                "value": self.peopleOccupancy
            }

        if self.refMap:
            building_data["refMap"] = {
                "type": "Property",
                "value": self.refMap
            }

        if self.seeAlso:
            building_data["seeAlso"] = {
                "type": "Property",
                "value": self.seeAlso
            }

        if self.source:
            building_data["source"] = {
                "type": "Property",
                "value": self.source
            }
        
        return building_data


    @staticmethod
    def validate_smart_data_model(data):
        required_fields = ['id', 'type', 'address', 'category']
        for field in required_fields:
            if field not in data:
                return False, f'Required "{field}" does not exist'
        return True, ''
