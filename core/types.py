"""
Custom type aliases for Django Financial API.

This module defines custom type aliases used throughout the application
for better type safety and code documentation.
"""

from typing import Any, Dict, List, Optional, TypeVar, Union

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest

from rest_framework.request import Request as DRFRequest

# Django type aliases
DjangoRequest = HttpRequest
RequestUser = User

# DRF type aliases
APIRequest = DRFRequest

# Generic type aliases
JSONDict = dict[str, Any]
JSONList = list[JSONDict]
StrList = list[str]
IntList = list[int]

# Optional types
OptionalStr = Optional[str]
OptionalInt = Optional[int]
OptionalDict = Optional[dict[str, Any]]

# Generic QuerySet type variable
_ModelT = TypeVar("_ModelT")
QuerySetType = QuerySet[_ModelT, _ModelT]

# Serializer data types
SerializerData = dict[str, Any]
ValidationErrors = dict[str, list[str]]

# HTTP Response types
ResponseData = Union[JSONDict, JSONList, str, None]
StatusCode = int

# Authentication types
Token = str
TokenPayload = dict[str, Any]

# Category choices type
CategoryChoice = str

# Transaction types
TransactionAmount = float
TransactionDescription = str
