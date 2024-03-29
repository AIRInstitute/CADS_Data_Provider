from datetime import datetime
import json

from app.utils import convert_geojson, generate_urn


ModelBase = object

class AgriParcel(ModelBase):
    """
        AgriParcel class represents an agricultural parcel record.
        
        Attributes:
            - location (str): The location of the agricultural parcel.
            - type_location (str): The type of location data provided (e.g., Polygon).
            - area (str): The area of the agricultural parcel.
            - description (str): A description of the parcel.
            - category (str): The category of the agricultural parcel.
            - belongs_to (str): The entity that the parcel belongs to.
            - has_agri_soil (str): Represents the relationship with the soil on the agricultural parcel.
            - date_created (datetime, optional): The date the record was created.
            - date_modified (datetime, optional): The date the record was last modified.
            - related_source (str, optional): Any related sources of information for the parcel.
            - see_also (str, optional): Additional resources related to the parcel.
            - owned_by (str, optional): The entity that owns the agricultural parcel.
            - has_agri_parcel_parent (str, optional): Represents the relationship with the parent agricultural parcel.
            - has_agri_parcel_children (str, optional): Represents the relationship with the child agricultural parcels.
            - has_agri_crop (str, optional): Represents the relationship with the crops on the agricultural parcel.
            - has_air_quality_observed (str, optional): Represents the relationship with the air quality observed on the parcel.
            - crop_status (str, optional): The status of the crop on the parcel.
            - last_planted_at (datetime, optional): The date when the parcel was last planted.
            - has_device (str, optional): Represents the relationship with the device that recorded these measurements.
            - soil_texture_type (str, optional): The type of soil texture on the parcel.
            - irrigation_system_type (str, optional): The type of irrigation system on the parcel.
    """

    def __init__(self, id, location, type_location, area, description, category, belongs_to, has_agri_soil, date_created=None,
                 date_modified=None, related_source=None, see_also=None, owned_by=None, has_agri_parcel_parent=None,
                 has_agri_parcel_children=None, has_agri_crop=None, has_air_quality_observed=None, crop_status=None,
                 last_planted_at=None, has_device=None, soil_texture_type=None, irrigation_system_type=None):
        
        self.id = id
        self.type = "AgriParcel"       
        self.date_created = date_created or datetime.utcnow()
        self.date_modified = date_modified or datetime.utcnow()
        self.type_location = type_location
        self.location = convert_geojson(type_location, location)
        self.area = area
        self.description = description
        self.category = category
        self.belongs_to = belongs_to
        self.related_source = related_source
        self.see_also = see_also
        self.owned_by = owned_by
        self.has_agri_parcel_parent = has_agri_parcel_parent
        self.has_agri_parcel_children = has_agri_parcel_children
        self.has_agri_crop = has_agri_crop
        self.has_air_quality_observed = has_air_quality_observed
        self.crop_status = crop_status
        self.last_planted_at = last_planted_at
        self.has_agri_soil = has_agri_soil
        self.has_device = has_device
        self.soil_texture_type = soil_texture_type
        self.irrigation_system_type = irrigation_system_type

    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<AgriParcel {self.id}>'
    
    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.
        
        Returns:
            A dictionary representing the current Smart Data Model.
        """
        agri_parcel_data = {
            "id": self.id,
            "type": self.type
        }

        # A continuación, se verifica cada atributo antes de añadirlo al diccionario:
        if self.date_created:
            agri_parcel_data["dateCreated"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.date_created
                }
            }

        if self.date_modified:
            agri_parcel_data["dateModified"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.date_modified
                }
            }

        if self.type_location and self.location:
            agri_parcel_data["location"] = {
                "type": "GeoProperty",
                "value": {
                    "type": self.type_location,
                    "coordinates": self.location
                }
            }

        if self.area:
            agri_parcel_data["area"] = {"value": self.area}

        if self.description:
            agri_parcel_data["description"] = {"value": self.description}

        if self.category:
            agri_parcel_data["category"] = {"value": self.category}

        if self.related_source:
            agri_parcel_data["relatedSource"] = {
                "value": [
                    {
                        "application": self.related_source.split(',') if isinstance(self.related_source, str) else self.related_source,
                        "applicationEntityId": "app:parcel1"
                    }
                ]
            }

        if self.see_also:
            agri_parcel_data["seeAlso"] = {
                "value": self.see_also.split(',') if isinstance(self.see_also, str) else self.see_also
            }

        # Similar checks for the remaining attributes:
        for attr, key in [
            (self.belongs_to, "belongsTo"),
            (self.owned_by, "ownedBy"),
            (self.has_agri_parcel_parent, "hasAgriParcelParent"),
            (self.has_agri_crop, "hasAgriCrop"),
            (self.has_air_quality_observed, "hasAirQualityObserved"),
            (self.crop_status, "cropStatus"),
            (self.has_agri_soil, "hasAgriSoil"),
            (self.soil_texture_type, "soilTextureType"),
            (self.irrigation_system_type, "irrigationSystemType")
        ]:
            if attr:
                agri_parcel_data[key] = {
                    "type": "Relationship" if "has" in key or "belongsTo" in key or "ownedBy" in key else "Property",
                    "object": attr if "has" in key or "belongsTo" in key or "ownedBy" in key else {"value": attr}
                }

        if self.has_agri_parcel_children:
            agri_parcel_data["hasAgriParcelChildren"] = {
                "type": "Relationship",
                "object": self.has_agri_parcel_children.split(',') if isinstance(self.has_agri_parcel_children, str) else self.has_agri_parcel_children
            }

        if self.last_planted_at:
            agri_parcel_data["lastPlantedAt"] = {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.last_planted_at
                }
            }

        if self.has_device:
            agri_parcel_data["hasDevice"] = {
                "type": "Relationship",
                "object": self.has_device.split(',') if isinstance(self.has_device, str) else self.has_device
            }

        return agri_parcel_data



    def validate_smart_data_model(data):
        required_fields = ['dateCreated', 'dateModified',  'location','area','description', 'category', 'belongsTo' ,'hasAgriSoil']
        for field in required_fields:
            if field not in data:
                return False, f'Required "{field}" does not exist'
        return True, ''