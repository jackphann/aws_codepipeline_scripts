import datetime

import configargparse

from commands.utility import env_to_region
from CodePipelineClient import CodePipelineClient
from commands.BaseCommand import BaseCommand

class ExecutePipelineCommand(BaseCommand):
    """Execute Code Pipelines Command"""

    def __init__(self):        
        # Get args from command line or environment variables.
        parser = configargparse.ArgParser(description="Execute an AWS Code Pipelines.")
        parser.add_argument("-e", "--environment", help="Environment: dev/staging/prod. Default: dev", choices=['dev', 'staging', 'prod'], required=False, default="dev")
        parser.add_argument("-n", "--name", help="Pipeline name.", required=True)

        self.parse_args, unkown = parser.parse_known_args()

    def execute(self):
      region = env_to_region[self.parse_args.environment]
      client = CodePipelineClient(region_name=region)
      client.execute_pipeline(self.parse_args.name)
