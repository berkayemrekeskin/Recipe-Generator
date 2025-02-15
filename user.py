from flask import Blueprint, render_template, request, redirect, url_for
from db import init_db

user = Blueprint('user', __name__)



