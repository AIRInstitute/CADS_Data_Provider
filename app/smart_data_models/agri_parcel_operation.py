from datetime import datetime

from app.utils import generate_urn


ModelBase = object

class AgriParcelOperation(ModelBase):
    """
        AgriParcelOperation class represents an operation on an agricultural parcel.
        
        Attributes:
            date_created (datetime): The creation date of this instance, defaults to current datetime.
            date_modified (datetime): The last modification date of this instance, defaults to current datetime.
            has_agri_parcel (str): The associated agricultural parcel of the operation.
            operation_type (str): The type of the operation.
            description (str): The description of the operation.
            result (str): The result of the operation.
            planned_start_at (datetime): The planned start time of the operation.
            planned_end_at (datetime): The planned end time of the operation.
            status (str): The status of the operation.
            started_at (datetime, optional): The actual start time of the operation.
            ended_at (datetime, optional): The actual end time of the operation.
            reported_at (datetime, optional): The reported time of the operation.
            related_source (str, optional): A source related to the operation.
            see_also (str, optional): Other related links.
            has_operator (str, optional): The operator of the operation.
            has_agri_product_type (str, optional): The associated product type of the operation.
            quantity (float, optional): The quantity involved in the operation.
            water_source (str, optional): The water source used in the operation.
            work_order (str, optional): The work order associated with the operation.
            work_record (str, optional): The work record associated with the operation.
            irrigation_record (str, optional): The irrigation record associated with the operation.
            diesel_fuel_consumption (float, optional): The diesel fuel consumption in the operation.
            gasoline_fuel_consumption (float, optional): The gasoline fuel consumption in the operation.
            diesel_fuel_consumption_max_value (float, optional): The maximum diesel fuel consumption in the operation.
            diesel_fuel_consumption_min_value (float, optional): The minimum diesel fuel consumption in the operation.
            diesel_fuel_consumption_unit_text (str, optional): The unit of diesel fuel consumption measurement.
            gasoline_fuel_consumption_max_value (float, optional): The maximum gasoline fuel consumption in the operation.
            gasoline_fuel_consumption_min_value (float, optional): The minimum gasoline fuel consumption in the operation.
            gasoline_fuel_consumption_unit_text (str, optional): The unit of gasoline fuel consumption measurement.
    """

    def __init__(self, has_agri_parcel, operation_type, description, result, planned_start_at, planned_end_at,
                 status, started_at, ended_at, reported_at, quantity, diesel_fuel_consumption,
                 diesel_fuel_consumption_max_value, diesel_fuel_consumption_min_value, diesel_fuel_consumption_unit_text,
                 gasoline_fuel_consumption,gasoline_fuel_consumption_max_value, gasoline_fuel_consumption_min_value, 
                 gasoline_fuel_consumption_unit_text, date_created=None, date_modified=None,
                 related_source=None, see_also=None, has_operator=None, has_agri_product_type=None, water_source=None,
                 work_order=None, work_record=None, irrigation_record=None):
        self.id = generate_urn("AgriParcelOperation")
        self.type = "AgriParcelOperation"
        self.date_created = date_created or datetime.utcnow()
        self.date_modified = date_modified or datetime.utcnow()
        self.has_agri_parcel = has_agri_parcel
        self.operation_type = operation_type
        self.description = description
        self.result = result
        self.planned_start_at = planned_start_at
        self.planned_end_at = planned_end_at
        self.status = status
        self.started_at = started_at
        self.ended_at = ended_at
        self.reported_at = reported_at
        self.related_source = related_source
        self.see_also = see_also
        self.has_operator = has_operator
        self.has_agri_product_type = has_agri_product_type
        self.quantity = quantity
        self.water_source = water_source
        self.work_order = work_order
        self.work_record = work_record
        self.irrigation_record = irrigation_record
        self.diesel_fuel_consumption = diesel_fuel_consumption
        self.gasoline_fuel_consumption = gasoline_fuel_consumption
        self.diesel_fuel_consumption_max_value = diesel_fuel_consumption_max_value
        self.diesel_fuel_consumption_min_value = diesel_fuel_consumption_min_value
        self.diesel_fuel_consumption_unit_text = diesel_fuel_consumption_unit_text
        self.gasoline_fuel_consumption_max_value = gasoline_fuel_consumption_max_value
        self.gasoline_fuel_consumption_min_value = gasoline_fuel_consumption_min_value
        self.gasoline_fuel_consumption_unit_text = gasoline_fuel_consumption_unit_text
        

    def __repr__(self):
        """
        This method returns a machine-readable string representation of the current object.
        """
        return f'<AgriParcelOperation {self.id}>'
    

    def to_smart_data_model(self):
        """
        This method converts the current object into a dictionary that adheres to the Smart Data Model standard.
        
        Returns:
            A dictionary representing the current Smart Data Model.
        """
        agri_parcel_operation_data = {
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
                        "applicationEntityId": "app:operation1"
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
            "operationType": {
                "value":self.operation_type
            },
            "description": {
                "value": self.description
            },
            "result": {
                "value":self.result
            },
            "plannedStartAt": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.planned_start_at
                }
            },
            "plannedEndAt": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.planned_end_at
                }
            },
            "status": {
                "value":self.status
            },
            "hasOperator": {
                "type": "Relationship",
                "object": self.has_operator
            },
            "startedAt": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.started_at
                }
            },
            "endedAt": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.ended_at
                }
            },
            "reportedAt": {
                "type": "Property",
                "value": {
                    "@type": "DateTime",
                    "@value": self.reported_at
                }
            },
            "hasAgriProductType": {
                "type": "Relationship",
                "object": self.has_agri_product_type
            },
            "quantity": {
                "value":self.quantity
            },
             "waterSource": {
                "value":self.water_source
            },
            "workOrder": {
                "type": "Property",
                "value": {
                    "@type": "URL",
                    "@value": self.work_order
                }
            },
            "workRecord": {
                "type": "Property",
                "value": {
                    "@type": "URL",
                    "@value": self.work_record
                }
            },
            "irrigationRecord": {
                "type": "Property",
                "value": {
                    "@type": "URL",
                    "@value": self.irrigation_record
                }
            },
            "dieselFuelConsumption": {
                "type": "Property",
                "value": {
                    "value": self.diesel_fuel_consumption,
                    "maxValue": self.diesel_fuel_consumption_max_value,
                    "minValue": self.diesel_fuel_consumption_min_value,
                    "unitText": self.diesel_fuel_consumption_unit_text
                }
            },
            "gasolineFuelConsumption": {
                "type": "Property",
                "value": {
                    "value": self.gasoline_fuel_consumption,
                    "maxValue": self.gasoline_fuel_consumption_max_value,
                    "minValue": self.gasoline_fuel_consumption_min_value,
                    "unitText": self.gasoline_fuel_consumption_unit_text
                }
            }
            
        }

        return agri_parcel_operation_data


    def validate_smart_data_model(data):
        required_fields = ['dateCreated', 'dateModified', 'hasAgriParcel', 'operationType', 'description', 'result', 'plannedStartAt',  'plannedEndAt' , 'status', 'startedAt', 'endedAt', 'reportedAt', 'quantity', 'dieselFuelConsumption', 'gasolineFuelConsumption']
        for field in required_fields:
            print(field)
            if field not in data:
                return False, f'Required "{field}" does not exist'
        return True, ''