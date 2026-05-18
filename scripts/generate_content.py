#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Moments Content Generator
Automatically generate content for WeChat Moments
"""

import random
from datetime import datetime

TEMPLATES = {
    "morning": [
        "Good morning ☀️ A new day, a new beginning",
        "Another energetic day 💪",
        "Morning sunshine is the best gift 🌅",
        "Good morning, have a great day!",
        "Every morning brings new hope ✨",
    ],
    "noon": [
        "Good noon ☀️ Remember to eat well",
        "Morning work done, lunch time 🍽️",
        "Afternoon coffee break ☕",
        "Take a break, keep going this afternoon 💪",
    ],
    "evening": [
        "Evening sunset is always beautiful 🌅",
        "Off work! A fulfilling day",
        "Sunset is beautiful 🌇",
        "Evening breeze, relaxing after a busy day",
    ],
    "night": [
        "Good night, sweet dreams 🌙",
        "Day done, time to rest 💤",
        "Late night, time for sleep",
        "Great day, good night world 🌙",
    ],
    "motivation": [
        "Life rewards those who work hard 💪",
        "Perseverance prevails, keep going!",
        "Every effort builds your future ✨",
        "Believe in yourself, you are stronger than you think",
        "Dreams are worth chasing 🌟",
    ],
    "life": [
        "Life needs rituals ✨",
        "Simple happiness is the best life",
        "Enjoy every moment",
        "Life is more than just work",
        "Little joys in everyday life 🌸",
    ],
    "work": [
        "Work makes me happy (not really) 😂",
        "Working hard, one day at a time 💪",
        "Another day at the office",
        "Work hard, live well",
        "Take breaks and stay hydrated ☕",
    ],
}

FESTIVALS = {
    "01-01": "Happy New Year! 🎆",
    "02-14": "Happy Valentine's Day 💕",
    "05-01": "Happy Labor Day! 💪",
    "10-01": "Happy National Day! 🇨🇳",
}


def get_time_category():
    """Get time category based on current time"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 14:
        return "noon"
    elif 14 <= hour < 18:
        return "evening"
    else:
        return "night"


def check_festival():
    """Check if today is a festival"""
    today = datetime.now().strftime("%m-%d")
    return FESTIVALS.get(today)


def generate_content():
    """
    Generate moments content

    Returns:
        str: Generated content
    """
    festival_content = check_festival()
    if festival_content:
        return festival_content

    time_category = get_time_category()

    themes = [time_category, "motivation", "life", "work"]
    selected_theme = random.choice(themes)

    if selected_theme in TEMPLATES:
        content = random.choice(TEMPLATES[selected_theme])
    else:
        content = random.choice(TEMPLATES["life"])

    return content


def main():
    content = generate_content()
    print(content)
    return content


if __name__ == "__main__":
    main()