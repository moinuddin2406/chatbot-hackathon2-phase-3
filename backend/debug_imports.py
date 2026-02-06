"""Debug script to identify import issues"""
import sys
import traceback
import os

# Add the current directory to the path for relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Starting import debugging...")

modules_to_test = [
    ('datetime', ''),
    ('timedelta', 'from datetime import datetime, timedelta'),
    ('typing', 'from typing import Optional'),
    ('fastapi', 'from fastapi import FastAPI, Depends, HTTPException, status'),
    ('security', 'from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials'),
    ('jwt', 'import jwt'),
    ('jwt_exceptions', 'from jwt.exceptions import InvalidTokenError, ExpiredSignatureError'),
    ('config', 'import config'),
    ('logging', 'import logging'),
    ('sqlmodel', 'from sqlmodel import Session, select'),
    ('db', 'import db'),
    ('models', 'import models'),
    ('auth', 'import auth'),
    ('security_module', 'import security'),
    ('utils', 'import utils'),
    ('task_service', 'from services import task_service'),
    ('tasks_route', 'from routes import tasks')
]

for module_name, import_statement in modules_to_test:
    try:
        if import_statement:
            exec(import_statement)
        else:
            __import__(module_name)
        print(f"✓ Successfully imported: {module_name}")
    except Exception as e:
        print(f"❌ Failed to import {module_name}: {str(e)}")
        traceback.print_exc()

print("Import debugging complete.")