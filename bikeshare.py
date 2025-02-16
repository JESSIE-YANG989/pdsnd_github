import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_user_input(prompt, valid_choices):
    """
    获取用户输入的有效值 / Helper function to get valid user input.

    Args:
        prompt (str): 要显示给用户的提示 / The prompt to display to the user.
        valid_choices (list): 有效选择的列表 / List of valid input choices.

    Returns:
        str: 有效的用户输入 / Valid user input.
    """
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_choices:
            return user_input
        print(f"无效输入！请选择：{', '.join(valid_choices)}\n / Invalid input. Please choose from: {', '.join(valid_choices)}\n")

def get_filters():
    """
    获取用户指定的城市、月份和星期几来分析数据 / Asks the user to specify a city, month, and day to analyze.

    Returns:
        city (str): 要分析的城市名称 / Name of the city to analyze.
        month (str): 过滤的月份名称，或"all"表示不过滤 / Name of the month to filter by, or "all" for no filter.
        day (str): 要过滤的星期几名称，或"all"表示不过滤 / Name of the day of week to filter by, or "all" for no filter.
    """
    print("你好！让我们一起探索美国的共享单车数据吧！ / Hello! Let's explore some US bikeshare data!")
    
    valid_cities = ['chicago', 'new york city', 'washington']
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    valid_days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

    city = get_user_input('你想查看哪个城市的数据？（Chicago, New York City 或 Washington）/ Would you like to see data for Chicago, New York City or Washington?\n', valid_cities)
    month = get_user_input("你想过滤哪一个月份？如果不想过滤，请输入'all' / Which month would you like to filter by? Type 'all' if you don't want to filter by month.\n", valid_months)
    day = get_user_input("你想查看哪一天的数据？如果不想过滤，请输入'all' / Which day would you like to see data for? Type 'all' if you don't want to filter by day.\n", valid_days)
    
    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    加载指定城市的数据，并根据月份和星期几进行过滤（如果适用） / Loads data for the specified city and filters by month and day if applicable.

    Returns:
        df (DataFrame): 过滤后的城市数据的Pandas DataFrame / Pandas DataFrame containing city data filtered by month and day.
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df
