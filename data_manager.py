import json
import os
from datetime import datetime, timedelta

DATA_FILE = 'data/exercise_data.json'
TIMEZONE_OFFSET = -8  # PST (UTC-8)

EXERCISES = ['pushups', 'pullups', 'squats', 'crunches']
EXERCISE_ALIASES = {
    'pushup': 'pushups',
    'pullup': 'pullups',
    'squat': 'squats',
    'crunch': 'crunches',
}

# State variables
users = {}
last_reset = None
daily_totals = {ex: 0 for ex in EXERCISES}

def load_data():
    global users, last_reset, daily_totals
    try:
        if not os.path.exists(DATA_FILE):
            return {}, None, {ex: 0 for ex in EXERCISES}
            
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            
            users = data.get('users', {})
            last_reset = data.get('last_reset', None)
            daily_totals = data.get('daily_totals', {ex: 0 for ex in EXERCISES})
            return users, last_reset, daily_totals
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, None, {ex: 0 for ex in EXERCISES}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump({
            'users': users,
            'last_reset': last_reset,
            'daily_totals': daily_totals
        }, f)

def get_pst_date():
    utc_now = datetime.utcnow()
    pst_now = utc_now + timedelta(hours=TIMEZONE_OFFSET)
    return pst_now.date()

def parse_exercise(text):
    text = text.lower()
    if text in EXERCISES:
        return text
    return EXERCISE_ALIASES.get(text)

def maybe_reset_daily():
    global users, last_reset, daily_totals
    today = str(get_pst_date())
    if last_reset != today:
        for user, stats in users.items():
            # If user did pushups yesterday (or any exercise)
            # The original code checked stats['current'] which is confusing if it was migrated
            # Let's check if they did any exercise yesterday
            did_anything = False
            for ex in EXERCISES:
                if stats['exercises'][ex]['current'] > 0:
                    did_anything = True
                    break
            
            if did_anything:
                try:
                    last_active_date = datetime.strptime(stats['last_active'], "%Y-%m-%d") if stats.get('last_active') else None
                    last_reset_date = datetime.strptime(last_reset, "%Y-%m-%d") if last_reset else None
                except (ValueError, TypeError):
                    last_active_date = last_reset_date = None
                
                if last_active_date and last_reset_date:
                    day_diff = (last_reset_date - last_active_date).days
                    if day_diff == 1:
                        stats['streak'] += 1
                    else:
                        stats['streak'] = 1
                else:
                    stats['streak'] = 1
                
                stats['days_tracked'] += 1
                stats['last_active'] = last_reset
            else:
                stats['streak'] = 0
            
            # Reset current for all exercises
            for ex_stats in stats['exercises'].values():
                ex_stats['current'] = 0
                
        daily_totals = {ex: 0 for ex in EXERCISES}
        last_reset = today
        save_data()

# Initial load
load_data()
