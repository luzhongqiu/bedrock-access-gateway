import json
import os
from typing import Annotated

import boto3
from botocore.exceptions import ClientError
from fastapi import Depends, HTTPException, status

from api.setting import DEFAULT_API_KEYS

# 移除所有认证相关的代码
