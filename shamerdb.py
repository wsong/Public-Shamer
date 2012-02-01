#!/usr/bin/python

import sqlite3

DATABASE_NAME = "shamer.db"
conn = None

def database_init():
    conn = sqlite3.connect(DATABASE_NAME)
    with conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("create table if not exists Users(Id integer primary key, Facebook_Id text, Full_Name text, First_Name text, Last_Name text, Access_Token text)")
        conn.commit()

def get_user_by_row_id(user_id):
    conn = sqlite3.connect(DATABASE_NAME)
    with conn:
        cur = conn.cursor()
        cur.execute("select * from Users where Id=?", (user_id,))
        row = cur.fetchone()
        return row

def get_user_by_fb_id(fb_id):
    conn = sqlite3.connect(DATABASE_NAME)
    with conn:
        cur = conn.cursor()
        cur.execute("select * from Users where Facebook_Id=?", (fb_id,))
        row = cur.fetchone()
        return row

def create_user(fb_id, full_name, first_name, last_name, access_token):
    conn = sqlite3.connect(DATABASE_NAME)
    with conn:
        cur = conn.cursor()
        values = (fb_id, full_name, first_name, last_name, access_token)
        cur.execute("insert into Users(Facebook_Id, Full_Name, First_Name, Last_Name, Access_Token) values (?, ?, ?, ?, ?)", values)
        conn.commit()
