from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *

subscription_id = '<subscription_id>'
resource_group_name = '<resource_group_name>'
datafactory_name = '<datafactory_name>'

credential = DefaultAzureCredential()

client = DataFactoryManagementClient(credential, subscription_id)

def create_pipeline(pipeline_name, pipeline_json):
 pipeline = PipelineResource(
 description="Pipeline to fetch and save country data",
 activities=pipeline_json['activities']
 )
 client.pipelines.create_or_update(resource_group_name, datafactory_name, pipeline_name, pipeline)

def create_trigger(trigger_name, trigger_json):
 trigger = ScheduleTriggerRecurrence(frequency=trigger_json['frequency'], interval=trigger_json['interval'], start_time=trigger_json['start_time'], minutes=trigger_json['minutes'])
 trigger = TriggerResource(
 description="Trigger for fetch country data pipeline",
 recurrence=trigger
 )
 client.triggers.create_or_update(resource_group_name, datafactory_name, trigger_name, trigger)

def create_pipeline_run(pipeline_name, reference_time):
 run_response = client.pipeline_runs.create(resource_group_name, datafactory_name, pipeline_name, parameters={}, reference_time=reference_time)

fetch_country_data_pipeline = {
 "activities": [
 {
 "name": "FetchCountryData",
 "type": "WebActivity",
 "linkedServiceName": {
 "referenceName": "RestAPILinkedService",
 "type": "LinkedServiceReference"
 },
 "typeProperties": {
 "url": "https://restcountries.com/v3.1/name/@{item().CountryName}",
 "method": "GET"
 },
 "foreach": "@activity('LookupCountryNames').output.value",
 "foreachItem": "CountryName"
 },
 {
 "name": "SaveCountryData",
 "type": "CopyActivity",
 "inputs": [],
 "outputs": [],
 "typeProperties": {
 "source": {
 "type": "RestSource"
 },
 "sink": {
 "type": "BlobSink",
 "writeBatchSize": 0,
 "writeBatchTimeout": "00:00:00"
 }
 }
 }
 ]
}

fetch_country_data_trigger = {
 "frequency": "Day",
 "interval": 1,
 "start_time": "2022-01-01T12:00:00Z",
 "minutes": [0]
}

create_pipeline("FetchCountryDataPipeline", fetch_country_data_pipeline)
create_trigger("FetchCountryDataTrigger", fetch_country_data_trigger)
