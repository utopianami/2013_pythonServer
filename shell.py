#!/usr/bin/env python
import os
import readline
from pprint import pprint

from flask import *
from app import *
from app.users.models import User, UserInfo
from app.missions.models import Mission, MissionState
from app.energy.models import EnergyData

os.environ['PYTHONINSPECT'] = 'True'

