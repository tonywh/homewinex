from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from datetime import datetime

from .models import Ingredient, Recipe, IngredientUse, Brew, LogEntry, Image

def index(request):
    return "HomeWineX says Hello!"
