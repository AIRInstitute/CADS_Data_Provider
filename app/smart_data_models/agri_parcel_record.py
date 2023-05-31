from datetime import datetime

from app.utils import convert_geojson, generate_urn


ModelBase = object

class AgriParcelRecord(ModelBase):
    """
    AgriParcelRecord class represents an agricultural parcel record.
        
    Attributes:
        - has_agri_parcel (str): Represents the relationship with the agricultural parcel.
        - location (str): The location of the agricultural parcel.
        - type_location (str): The type of location data provided (e.g., Polygon).
        - soil_temperature (float): The soil temperature at the location.
        - soil_temperature_unit (str): The unit of the soil temperature (e.g., 'C' for Celsius).
        - air_temperature (float): The air temperature at the location.
        - air_temperature_unit (str): The unit of the air temperature.
        - air_temperature_timestamp (str): The timestamp when the air temperature was recorded.
        - relative_humidity (float): The relative humidity at the location.
        - relative_humidity_unit (str): The unit of the relative humidity.
        - relative_humidity_timestamp (str): The timestamp when the relative humidity was recorded.
        - date_created (datetime, optional): The date when the record was created. If not provided, it's set to the current UTC time.
        - date_modified (datetime, optional): The date when the record was last modified. If not provided, it's set to the current UTC time.
        - related_source (str, optional): The source related to this agricultural parcel record.
        - see_also (str, optional): An optional field that could be used to provide additional related information.
        - soil_moisture_vwc (float, optional): The soil moisture content (in volume water content).
        - soil_moisture_vwc_unit (str, optional): The unit of soil moisture content.
        - soil_moisture_vwc_timestamp (str, optional): The timestamp when the soil moisture content was recorded.
        - depth (float, optional): The depth of the measurement.
        - depth_unit (str, optional): The unit of the depth measurement.
        - soil_moisture_ec (float, optional): The soil moisture (in electrical conductivity).    
        - soil_moisture_ec_unit (str, optional): The unit of soil moisture (in electrical conductivity).
        - soil_moisture_ec_timestamp (str, optional): The timestamp when the soil moisture (in electrical conductivity) was recorded.
        - soil_salinity (float, optional): The soil salinity measurement.
        - soil_salinity_unit (str, optional): The unit of the soil salinity measurement.
        - soil_salinity_timestamp (str, optional): The timestamp when the soil salinity was recorded.
        - leaf_wetness (float, optional): The leaf wetness measurement.
        - leaf_wetness_unit (str, optional): The unit of the leaf wetness measurement.
        - leaf_wetness_timestamp (str, optional): The timestamp when the leaf wetness was recorded.
        - leaf_relative_humidity (float, optional): The leaf relative humidity measurement.
        - leaf_relative_humidity_unit (str, optional): The unit of the leaf relative humidity measurement.
        - leaf_relative_humidity_timestamp (str, optional): The timestamp when the leaf relative humidity was recorded.
        - leaf_temperature (float, optional): The leaf temperature measurement.
        - leaf_temperature_unit (str, optional): The unit of the leaf temperature measurement.
        - leaf_temperature_timestamp (str, optional): The timestamp when the leaf temperature was recorded.
        - solar_radiation (float, optional): The solar radiation measurement.
        - solar_radiation_unit (str, optional): The unit of the solar radiation measurement.
        - solar_radiation_timestamp (str, optional): The timestamp when the solar radiation was recorded.
        - atmospheric_pressure (float, optional): The atmospheric pressure measurement.
        - atmospheric_pressure_unit (str, optional): The unit of the atmospheric pressure measurement.
        - atmospheric_pressure_timestamp (str, optional): The timestamp when the atmospheric pressure was recorded.
        - description (str, optional): A description of the record.
        - has_device (str, optional): Represents the relationship with the device that recorded these measurements.
        - observed_at (datetime, optional): The timestamp when the measurements were observed.
        - timestamp (datetime, optional): The timestamp for the record.
    """


    def __init__(self, has_agri_parcel, location, type_location, soil_temperature, soil_temperature_unit, air_temperature, air_temperature_unit, air_temperature_timestamp, relative_humidity, relative_humidity_unit, relative_humidity_timestamp, 
                 date_created=None, date_modified=None, related_source=None, see_also=None, soil_moisture_vwc=None,
                 soil_moisture_vwc_unit=None, soil_moisture_vwc_timestamp=None, depth=None, depth_unit=None,
                 soil_moisture_ec=None, soil_moisture_ec_unit=None, soil_moisture_ec_timestamp=None, 
                 soil_salinity=None, soil_salinity_unit=None, soil_salinity_timestamp=None, leaf_wetness=None, leaf_wetness_unit=None, leaf_wetness_timestamp=None, leaf_relative_humidity=None, leaf_relative_humidity_unit=None, leaf_relative_humidity_timestamp=None,
                 leaf_temperature=None, leaf_temperature_unit=None, leaf_temperature_timestamp=None,
                 solar_radiation=None, solar_radiation_unit=None, solar_radiation_timestamp=None,
                 atmospheric_pressure=None, atmospheric_pressure_unit=None, atmospheric_pressure_timestamp=None,
                 description=None, has_device=None, observed_at=None, timestamp=None):


       
        self.id = generate_urn("AgriParcelRecord")
        self.type = "AgriParcelRecord"           
        self.date_created = date_created or datetime.utcnow()
        self.date_modified = date_modified or datetime.utcnow()
        self.has_agri_parcel = has_agri_parcel
        self.type_location = type_location
        self.location = convert_geojson(type_location=type_location, location=location)
        self.soil_temperature = soil_temperature
        self.soil_temperature_unit = soil_temperature_unit
        self.air_temperature = air_temperature
        self.air_temperature_unit = air_temperature_unit
        self.air_temperature_timestamp = air_temperature_timestamp
        self.relative_humidity = relative_humidity
        self.relative_humidity_unit = relative_humidity_unit
        self.relative_humidity_timestamp = relative_humidity_timestamp
        self.related_source = related_source
        self.see_also = see_also
        self.soil_moisture_vwc = soil_moisture_vwc
        self.soil_moisture_ec = soil_moisture_ec
        self.soil_salinity = soil_salinity
        self.soil_salinity_unit = soil_salinity_unit
        self.soil_salinity_timestamp = soil_salinity_timestamp
        self.leaf_wetness = leaf_wetness
        self.leaf_wetness_unit = leaf_wetness_unit
        self.leaf_wetness_timestamp = leaf_wetness_timestamp
        self.leaf_relative_humidity = leaf_relative_humidity
        self.leaf_relative_humidity_unit = leaf_relative_humidity_unit
        self.leaf_relative_humidity_timestamp = leaf_relative_humidity_timestamp
        self.leaf_temperature = leaf_temperature
        self.leaf_temperature_unit = leaf_temperature_unit
        self.leaf_temperature_timestamp = leaf_temperature_timestamp
        self.solar_radiation = solar_radiation
        self.solar_radiation_unit = solar_radiation_unit
        self.solar_radiation_timestamp = solar_radiation_timestamp
        self.atmospheric_pressure = atmospheric_pressure
        self.atmospheric_pressure_unit = atmospheric_pressure_unit
        self.atmospheric_pressure_timestamp = atmospheric_pressure_timestamp
        self.description = description
        self.has_device = has_device
        self.observed_at = observed_at
        self.depth = depth
        self.depth_unit = depth_unit
        self.timestamp = timestamp
        self.soil_moisture_vwc_unit = soil_moisture_vwc_unit
        self.soil_moisture_vwc_timestamp = soil_moisture_vwc_timestamp
        self.soil_moisture_ec_unit = soil_moisture_ec_unit
        self.soil_moisture_ec_timestamp = soil_moisture_ec_timestamp
   



    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<AgriParcelRecord {self.id}>'

    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.

        Returns:
            A dictionary representing the current Smart Data Model.
        """
        agri_parcel_record_data = {
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
            "relatedSource": {
                "value": [
                    {
                        "application": self.related_source.split(',') if isinstance(self.related_source, str) else self.related_source,
                        "applicationEntityId": "app:record1"
                    }
                ]
            },
            "seeAlso": {
                "value": self.see_also.split(',') if isinstance(self.see_also, str) else self.see_also
            },
            "hasAgriParcel": {
                "type": "Relationship",
                "object": self.has_agri_parcel
            },
            "location": {
                "type": "GeoProperty",
                "value": {
                    "type": self.type_location,
                    "coordinates": self.location
                }
            },
            "soilTemperature": {
                "type": "Property",
                "value": self.soil_temperature,
                "unitCode":  self.soil_temperature_unit
            },
            "timestamp": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.timestamp
                }
            },
            "depth": {
                "type": "Property",
                "value": self.depth,
                "unitCode":  self.depth_unit
            },
            "soilMoistureVWC": {
                "type": "Property",
                "value": self.soil_moisture_vwc,
                "unitCode":  self.soil_moisture_vwc_unit
            },
            "soilMoistureEC": {
                "type": "Property",
                "value": self.soil_moisture_ec,
                "unitCode":  self.soil_moisture_ec_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                        "@value": self.soil_moisture_ec_timestamp
                    }
                }
            },
            "soilSalinity": {
                "type": "Property",
                "value": self.soil_salinity,
                "unitCode":  self.soil_salinity_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                        "@value": self.soil_salinity_timestamp
                    }
                }
            },
            "leafWetness": {
                "type": "Property",
                "value": self.leaf_wetness,
                "unitCode":  self.leaf_wetness_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                    "@value": self.leaf_wetness_timestamp
                    }
                }
            },
            "leafRelativeHumidity": {
                "type": "Property",
                "value": self.leaf_relative_humidity,
                "unitCode": self.leaf_relative_humidity_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                        "@value": self.leaf_relative_humidity_timestamp
                    }
                }
            },
            "leafTemperature": {
                "type": "Property",
                "value": self.leaf_temperature,
                "unitCode": self.leaf_temperature_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                        "@value": self.leaf_temperature_timestamp
                    }
                }
            },
            "airTemperature": {
                "type": "Property",
                "value": self.air_temperature,
                "unitCode": self.air_temperature_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                        "@value": self.air_temperature_timestamp
                    }
                }
            },
            "solarRadiation": {
                "type": "Property",
                "value": self.solar_radiation,
                "unitCode":  self.solar_radiation_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                        "@value": self.solar_radiation_timestamp
                    }
                }
            },
            "relativeHumidity": {
                "type": "Property",
                "value": self.relative_humidity,
                "unitCode":  self.relative_humidity_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                        "@value": self.relative_humidity_timestamp
                    }
                }
            },
            "atmosphericPressure": {
                "type": "Property",
                "value": self.atmospheric_pressure,
                "unitCode":  self.atmospheric_pressure_unit,
                "timestamp": {
                    "type": "Property",
                    "value": {
                        "@type": "DateTime",
                        "@value": self.atmospheric_pressure_timestamp
                    }
                }
            },
            "description": {
                "type": "Property",
                "value": self.description
            },
            "hasDevice": {
                "type": "Relationship",
                "object": self.has_device.split(',') if isinstance(self.has_device, str) else self.has_device
            },
            "observedAt":  self.observed_at
                
        }

        return agri_parcel_record_data
