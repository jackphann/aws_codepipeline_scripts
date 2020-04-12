"""This module contains utility variables/methods"""

from commands.ListPipelinesCommand import ListPipelinesCommand
from commands.ExecutePipelineCommand import ExecutePipelineCommand


commands = {
  "list": ListPipelinesCommand,
  "execute": ExecutePipelineCommand
}