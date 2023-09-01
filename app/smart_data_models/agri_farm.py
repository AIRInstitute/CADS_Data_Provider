from datetime import datetime
from app.utils import convert_geojson, generate_urn


ModelBase = object

class AgriFarm(ModelBase):
    """
    AgriFarm class represents a farm with its related properties.

    Attributes:
        - name (str): The name of the farm.
        - location (str): The location of the farm.
        - address_locality (str): The locality of the farm's address.
        - address_country (str): The country of the farm's address.
        - address_street (str): The street of the farm's address.
        - contact_point_email (str): The contact email of the farm.
        - contact_point_telephone (str): The contact telephone of the farm.
        - has_agri_parcel (AgriParcel): The agricultural parcel related to this farm.
        - date_created (datetime, optional): The date when the instance of this class was created, defaults to current datetime.
        - date_modified (datetime, optional): The date when the instance of this class was last modified, defaults to current datetime.
        - description (str, optional): A description of the farm.
        - related_source (str, optional): A source related to the farm.
        - see_also (str, optional): Other related links.
        - land_location (str, optional): The specific location of the land of the farm.
        - owned_by (str, optional): The owner of the farm.
        - has_building (str, optional): The building associated with the farm.
    """
    def __init__(self, id, name, location,location_type, address_locality, address_country, address_street, contact_point_email, contact_point_telephone, has_agri_parcel, date_created=None, date_modified=None,
                 description=None, related_source=None, see_also=None, land_location=None,land_location_type=None,
                 owned_by=None, has_building=None):
        self.id = id
        self.type = "AgriFarm"
        self.name = name
        self.location_type = location_type
        self.location = convert_geojson(self.location_type, location)
        self.address_locality = address_locality
        self.address_country = address_country
        self.address_street = address_street
        self.contact_point_email = contact_point_email
        self.contact_point_telephone = contact_point_telephone
        self.has_agri_parcel = has_agri_parcel
        self.date_created = date_created or datetime.utcnow()
        self.date_modified = date_modified or datetime.utcnow()
        self.description = description
        self.related_source = related_source
        self.see_also = see_also
        self.land_location_type = land_location_type
        self.land_location = convert_geojson(self.land_location_type, land_location)
        self.owned_by = owned_by
        self.has_building = has_building
        

    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<AgriFarm {self.name}>'

    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.

        Returns:
            A dictionary representing the current Smart Data Model.
        """
        agri_farm_data = {
            "id": self.id,
            "type": self.type
        }

        if self.date_created:
            agri_farm_data["dateCreated"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.date_created
                }
            }

        if self.date_modified:
            agri_farm_data["dateModified"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.date_modified
                }
            }

        if self.name:
            agri_farm_data["name"] = {
                "type": "Property",
                "value": self.name
            }

        if self.description:
            agri_farm_data["description"] = {
                "type": "Property",
                "value": self.description
            }

        if self.related_source:
            agri_farm_data["relatedSource"] = {
                "type": "Property",
                "value": [
                    {
                        "application": self.related_source,
                        "applicationEntityId": "app:farm1"
                    }
                ]
            }

        if self.see_also:
            agri_farm_data["seeAlso"] = self.see_also

        if self.location_type and self.location:
            agri_farm_data["location"] = {
                "type": "GeoProperty",
                "value": {
                    "type": self.location_type,
                    "coordinates": self.location
                }
            }

        if self.land_location_type and self.land_location:
            agri_farm_data["landLocation"] = {
                "type": "GeoProperty",
                "value": {
                    "type": self.land_location_type,
                    "coordinates": self.land_location
                }
            }

        if self.address_locality or self.address_country or self.address_street:
            agri_farm_data["address"] = {
                "type": "Property",
                "value": {
                    "addressLocality": self.address_locality,
                    "addressCountry": self.address_country,
                    "streetAddress": self.address_street
                }
            }

        if self.contact_point_email or self.contact_point_telephone:
            agri_farm_data["contactPoint"] = {
                "type": "Property",
                "value": {
                    "email": self.contact_point_email,
                    "telephone": self.contact_point_telephone
                }
            }

        if self.owned_by:
            agri_farm_data["ownedBy"] = {
                "type": "Relationship",
                "object": self.owned_by
            }

        if self.has_building:
            agri_farm_data["hasBuilding"] = {
                "type": "Relationship",
                "object": self.has_building.split(',') if isinstance(self.has_building, str) else self.has_building
            }

        if self.has_agri_parcel:
            agri_farm_data["hasAgriParcel"] = {
                "type": "Relationship",
                "object": self.has_agri_parcel.split(',') if isinstance(self.has_agri_parcel, str) else self.has_agri_parcel
            }

        return agri_farm_data


    def validate_smart_data_model(data):
        required_fields = ['dateCreated', 'dateModified', 'name', 'location', 'address', 'contactPoint', 'hasAgriParcel']
        for field in required_fields:
            if field not in data:
                return False, f'Required "{field}" does not exist'
        return True, ''
