"""This module contain the CodePipelineClient class to interact with AWS Python SDK"""

import sys

import boto3
import botocore
from tabulate import tabulate


class CodePipelineClient:
  """This class defines methods to interact with required AWS Codepipe resource"""

  def __init__(self, region_name):
    self.client = boto3.Session(region_name=region_name).client("codepipeline")

  def list_pipelines(self, name=""):
    """
      List pipelines status filtering by name

      Parameter: 
        - name (string): Name to filter pipelines

      Output: Print pipelines status filtered by name to stout with table format.
    """

    try:
      pipeline_names = self.get_pipeline_names(name=name)
      pipeline_details = self.get_pipeline_details(pipeline_names=pipeline_names)
      CodePipelineClient.display_pipelines(pipeline_details)
    except:
      print("Something went wrong. Please try again.")
      sys.exit(2)

  def execute_pipeline(self, name):
    """
      Execute pipeline with specified name

      Parameter: 
        - name (string): Name of the pipeline

      Output: Print message to stout.
    """

    try:
      pipeline_execution = self.client.start_pipeline_execution(name=name)
      print("Execute successfully. Execution ID: {}".format(pipeline_execution['pipelineExecutionId']))
      sys.exit(0)
    except self.client.exceptions.PipelineNotFoundException:
      print("Pipeline not found.")
      sys.exit(2)
    except Exception:
      print("Something went wrong. Please try again.")
      sys.exit(2)

  def get_pipeline_names(self, name=""):
    """
      Find pipelines filter by name.

      Parameter: 
        - name (string): Name to filter pipelines

      Output: list of pipeline names ([:string])
    """

    name = name.lower()
    pipeline_names = []
    
    next_token = None

    while True:
      if next_token is None:
        pipelines_raw = self.client.list_pipelines()
      else:
        pipelines_raw = self.client.list_pipelines(nextToken=next_token)

      for pipeline in pipelines_raw['pipelines']:
        if name in pipeline['name'].lower():
          pipeline_names.append(pipeline['name'])

      next_token = pipelines_raw.get('nextToken')

      if next_token is None:
        break

    return pipeline_names

  def get_pipeline_details(self, pipeline_names):
    """
      Get pipelines details with a given list of pipeline names

      Parameter: 
        - pipeline_names ([:string]): List of pipeline names.

      Output: ([[<pipeline_name:string>, <lastest_status:string>, <last_resource_revision:string>, <last_executed:string>]])
    """

    pipeline_details = []

    for pipeline_name in pipeline_names:
      pipeline_detail_raw = self.client.list_pipeline_executions(pipelineName=pipeline_name, maxResults=1)
      
      if len(pipeline_detail_raw.get('pipelineExecutionSummaries')) != 0:
        pipeline_detail = [
          pipeline_name,
          pipeline_detail_raw['pipelineExecutionSummaries'][0]['status'],
          pipeline_detail_raw['pipelineExecutionSummaries'][0]['sourceRevisions'][0]['revisionSummary'][:50],
          str(pipeline_detail_raw['pipelineExecutionSummaries'][0]['startTime'])]
      else:
        pipeline_detail = [pipeline_name, None, None, None]

      pipeline_details.append(pipeline_detail)

    return pipeline_details    

  @staticmethod
  def display_pipelines(pipeline_details):
    header = ['Name', 'Latest Status', 'Latest source revisions', 'Last executed']
    print(tabulate(pipeline_details, headers=header, tablefmt='orgtbl'))
