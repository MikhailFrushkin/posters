from pathlib import Path

from environs import Env

path = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()

token = env.str('token')
