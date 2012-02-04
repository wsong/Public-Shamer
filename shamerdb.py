#!/usr/bin/python

import constants
import sqlite3

conn = None

def database_init():
    conn = sqlite3.connect(constants.DATABASE_NAME)
    with conn:
        cur = conn.cursor()
        cur.execute("create table if not exists Users(Id integer primary key, Facebook_Id text, Full_Name text, First_Name text, Last_Name text, LastFm boolean, LastFm_Username text, Reminder_Time_Day_Of_Week int, Reminder_Time_Hour int, Access_Token text)")
        conn.commit()

def get_user_by_fb_id(fb_id):
    conn = sqlite3.connect(constants.DATABASE_NAME)
    with conn:
        conn.row_factory = sqlite3.Row        
        cur = conn.cursor()
        cur.execute("select * from Users where Facebook_Id=?", (fb_id,))
        row = cur.fetchone()
        return row

def create_user(fb_id, full_name, first_name, last_name, access_token):
    conn = sqlite3.connect(constants.DATABASE_NAME)
    with conn:
        cur = conn.cursor()
        values = (fb_id, full_name, first_name, last_name, access_token)
        cur.execute("insert into Users(Facebook_Id, Full_Name, First_Name, Last_Name, Access_Token) values (?, ?, ?, ?, ?)", values)
        conn.commit()

def set_user_reminder_time(fb_id, day_of_week, hour):
    conn = sqlite3.connect(constants.DATABASE_NAME)
    with conn:
        cur = conn.cursor()
        cur.execute("update Users set Reminder_Time_Day_Of_Week=?, Reminder_Time_Hour=? where Facebook_Id=?", (day_of_week, hour, fb_id))
        conn.commit()

def set_user_last_fm_pref(fb_id, last_fm_pref, lastfm_username):
    conn = sqlite3.connect(constants.DATABASE_NAME)
    with conn:
        cur = conn.cursor()
        cur.execute("update Users set LastFm=?, LastFm_Username=? where Facebook_Id=?", (last_fm_pref, lastfm_username, fb_id))
        conn.commit()
        
def delete_user_by_fb_id(fb_id):
    conn = sqlite3.connect(constants.DATABASE_NAME)
    with conn:
        cur = conn.cursor()
        cur.execute("delete from Users where Facebook_Id=?", (fb_id,))
        conn.commit()
        
