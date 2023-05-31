# CADS_AGRISYNC
General framework for input data that flow to the Context Broker from the farmers converting to chosen smart data models.

This project uses Fiware, i4Trust, and iSHARE to create an infrastructure that enables data exchange and collaboration among different roles in an agricultural environment. The roles and the project flow are as follows:

## Roles:

- **Data Hub/Provider**: This role gathers information from farmers and stores it in a data environment. It uses Fiware components such as NGSI-LD (a standardized format for representing data), the context broker (for managing access and distribution of data), authz registry (authorization registry), i4Trust activation-service (to activate the i4Trust service), Keyrock (identity provider), and Kong (API Gateway).

- **Data Consumer**: This role is responsible for calculating the carbon footprint using the information provided by the Data Hub/Provider. It includes a context broker, the carbon footprint calculator, Kong, Keyrock, and authz registry.

- **i4Trust Marketplace**: This is a platform that allows data providers to offer their data and data consumers to subscribe to them. It facilitates the discovery and purchase of data and services.

- **Trusted Area**: This is the area under a specific data space governance. iSHARE plays the role of trust provider, ensuring trust and security in the data exchange.

## Project Flow:
### Step 1:
A contract is established between the data provider and data consumer.
#### Step 1.1:
The data provider creates an offer for the farmers' data in the i4Trust marketplace.
#### Step 1.2:
The data consumer subscribes to the offer in the marketplace, which automatically creates an entry in the data provider's authorization registry, allowing the consumer to access the data.

### Step 2:
Thanks to the contract established in Step 1, the data provider can request access to the relevant data and collect it.

## i4Trust Roles:
i4Trust roles include: Trust Authority Provider, Data Consumer, Data Provider, Data Owner, Identity Provider, Authorization Registry Provider, and Marketplace Provider. These roles ensure reliability and security in the data and services exchange in the project.

This infrastructure enables efficient and secure collaboration and data exchange, improving knowledge and decision-making in the agricultural sector, such as carbon footprint calculation.


## Configuration

Sensitive information such as API keys and database credentials are stored in a `config.py` file, located in the `app` directory. To keep these sensitive details secure, this file is not included in the version control repository.

Before running this application, you'll need to create your own `config.py` file. To do this:

1. Copy the `config_example.py` file and rename it to `config.py`. This file is also located in the `app` directory.
2. Open the `config.py` file and replace the placeholder values with your actual details.

Please ensure that you do not commit the `config.py` file to any public repository to avoid exposing your sensitive details.

## Flask App Setup

1. Create and activate a virtual environment (recommended):

    ```bash
    python -m venv venv
    ```

    - On Windows, activate the virtual environment:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS and Linux, activate the virtual environment:

        ```bash
        source venv/bin/activate
        ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask app:

    ```bash
    flask run
    ```

    This command will start the Flask development server, and you should see the app running at `http://localhost:5000`.

4. Open your web browser and visit `http://localhost:5000` to see the app in action.


