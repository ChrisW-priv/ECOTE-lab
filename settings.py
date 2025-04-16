from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    input_file: str = Field(..., description="Path to input XML file")
    output_dir: str = Field(..., description="Directory to output C# code")
