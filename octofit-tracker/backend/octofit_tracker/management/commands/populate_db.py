from django.core.management.base import BaseCommand
from django.conf import settings

from django.db import connection
from pymongo import ASCENDING
from octofit_tracker.db_utils import get_db

from django.contrib.auth import get_user_model

import random

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):

        self.stdout.write(self.style.SUCCESS('Connecting to MongoDB...'))
        db = get_db()

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index([('email', ASCENDING)], unique=True)

        # Teams
        teams = [
            {'name': 'Team Marvel'},
            {'name': 'Team DC'}
        ]
        team_ids = db.teams.insert_many(teams).inserted_ids

        # Users
        users = [
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': team_ids[0]},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': team_ids[0]},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': team_ids[1]},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': team_ids[1]},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Activities
        activities = [
            {'user': user_ids[0], 'type': 'Run', 'distance': 5, 'duration': 30},
            {'user': user_ids[1], 'type': 'Swim', 'distance': 2, 'duration': 40},
            {'user': user_ids[2], 'type': 'Bike', 'distance': 10, 'duration': 50},
            {'user': user_ids[3], 'type': 'Run', 'distance': 7, 'duration': 35},
        ]
        db.activities.insert_many(activities)

        # Workouts
        workouts = [
            {'name': 'Morning Cardio', 'suggested_for': 'Team Marvel'},
            {'name': 'Strength Training', 'suggested_for': 'Team DC'}
        ]
        db.workouts.insert_many(workouts)

        # Leaderboard
        leaderboard = [
            {'team': team_ids[0], 'points': 150},
            {'team': team_ids[1], 'points': 120}
        ]
        db.leaderboard.insert_many(leaderboard)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
