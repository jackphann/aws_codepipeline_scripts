import datetime

import configargparse

from commands.utility import env_to_region
from CodePipelineClient import CodePipelineClient
from commands.BaseCommand import BaseCommand


class ListPipelinesCommand(BaseCommand):
    """List Code Pipelines Command"""

    def __init__(self):        
        # Get args from command line or environment variables.
        parser = configargparse.ArgParser(description="List AWS Code Pipelines in a specific environment.")
        parser.add_argument("-e", "--environment", help="Environment: dev/staging/prod. Default: dev", choices=['dev', 'staging', 'prod'], required=False, default="dev")
        parser.add_argument("-n", "--name", help="Pipeline name. Default: \"\"", required=False, default="")

        self.parse_args, unkown = parser.parse_known_args()

    def execute(self):
      region = env_to_region[self.parse_args.environment]
      client = CodePipelineClient(region_name=region)
      client.list_pipelines(self.parse_args.name)
