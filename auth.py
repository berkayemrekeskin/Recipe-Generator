from flask import Blueprint, render_template, request, redirect, url_for
from db import init_db

auth = Blueprint('auth', __name__)

