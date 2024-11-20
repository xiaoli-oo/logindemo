import math
import random
import json
import redis
import threading
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import HttpResponseRedirect, Http404, HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.cache import never_cache, cache_page, cache_control
from django.core.cache import caches
from django.contrib.sitemaps import Sitemap
from django.db.models import F, Q
from django.urls import reverse
from django.core import validators
from logindemo.settings import REDIS_POOL

# Create your views here.
cache_token = caches['token']
cache_api = caches['api']

rr = redis.Redis(connection_pool=REDIS_POOL)
