from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    input_file: str = Field(..., description="Path to input XML file")
    output_dir: str = Field("generated", description="Directory to output C# code")
