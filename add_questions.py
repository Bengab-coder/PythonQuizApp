"""
THIS FILE IS USED TO ADD DATA TO THE DATABASE.
"""

from kivymd.app import MDApp
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder

import sqlite3

KV = """
<Label>:
    size_hint_x:0.5
    halign:'center'
    color:0,0,0,1
    font_size:"18sp"

<CategoryButton>:
    on_press:app.on_select_category(self)
    size_hint: None, None
    size:170,50

Screen:
    GridLayout:
        rows:10
        cols:1
        padding:10
        spacing:10

        Label:
            text:"Add questions to the app"
                
        
        GridLayout:
            cols:2
            rows:1
            Label:
                text:"Question"
            TextInput:
                id:question
                
                
        
        GridLayout:
            cols:2
            rows:1
            Label:
                text:"Option1"
            TextInput:
                id:opt1
                
        
        GridLayout:
            cols:2
            rows:1
            Label:
                text:"Option2"
            TextInput:
                id:opt2
                
        
        GridLayout:
            cols:2
            rows:1
            Label:
                text:"Option3"
            TextInput:
                id:opt3
                
        
        GridLayout:
            cols:2
            rows:1
            MDLabel:
                text:"Option4"
            TextInput:
                id:opt4
                

        GridLayout:
            cols:2
            rows:1
            Label:
                text:"Answer"
            TextInput:
                id:answer
                
        
        GridLayout:
            cols:2
            rows:1
            Label:
                text:"Category"

            GridLayout:
                cols:3
                rows:1
                pos_hint: {'center_x': 0.5}

                CategoryButton:
                    text:"Fundamentals"
                    group:'cat-btn'
                    state:'down'

                CategoryButton:
                    text:"OOP"
                    group:'cat-btn'

                CategoryButton:
                    text:"Algorithms and DS"
                    group:'cat-btn'
                
        
        GridLayout:
            cols:2
            orientation: 'rl-tb'
            MDRectangleFlatButton:
                text:"Add Question"
                on_release:app.add_question(question,opt1,opt2,opt3,opt4,answer)
"""


class CategoryButton(ToggleButton):
    pass


class AddQuestionsApp(MDApp):
    
    def __init__(self,**kwargs):
        super(AddQuestionsApp,self).__init__(**kwargs)
        with sqlite3.connect("questions_database.sqlite") as db:
            database = db.cursor()
            SQL = """CREATE TABLE IF NOT EXISTS questions (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        question text NOT NULL,
                        opt1 text NOT NULL,
                        opt2 text NOT NULL,
                        opt3 text NOT NULL,
                        opt4 text NOT NULL,
                        answer text NOT NULL,
                        category text NOT NULL
                );"""
            database.execute(SQL)
            
            self.category = "Fundamentals"
        
    def build(self):
        return Builder.load_string(KV)
    
    def on_select_category(self,category):
        self.category = category.text
        
    def add_question(self,question,opt1,opt2,opt3,opt4,answer):
        with sqlite3.connect("questions_database.sqlite") as db:
            database = db.cursor()
            SQL = "INSERT INTO questions (question,opt1,opt2,opt3,opt4,answer,category) VALUES (?,?,?,?,?,?,?);"
            database.execute(SQL,(
                question.text,
                opt1.text,
                opt2.text,
                opt3.text,
                opt4.text,
                answer.text,
                self.category
            ))
            db.commit()
            
        question.text = ""
        opt1.text = ""
        opt2.text = ""
        opt3.text = ""
        opt4.text = ""
        answer.text = ""
    
    
if __name__ == "__main__":
    AddQuestionsApp().run()