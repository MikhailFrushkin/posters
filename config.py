from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from environs import Env

path = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()

token = env.str('token')


@dataclass
class FilesOnPrint:
    art: str
    count: int
    name: Optional[str] = None
    status: str = '❌'
    #'✅'

