from pydantic_settings import BaseSettings, CliPositionalArg
from pydantic import Field


class Settings(BaseSettings, cli_parse_args=True):
    input_file: CliPositionalArg[str] = Field(..., description='Path to input XML file')
    output_dir: str = Field('generated', description='Directory to output C# code')
