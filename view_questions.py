from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable

import sqlite3


def get_all_questions():
    with sqlite3.connect("questions_database.sqlite") as db:
        database = db.cursor()
        all = database.execute("SELECT * FROM questions").fetchall()
        return all


class ViewQuestionsApp(MDApp):
    def build(self):
        data_table = MDDataTable(
            check=False,
            use_pagination=True,
            column_data=[
                ("ID.", dp(30)),
                ("Question", dp(50)),
                ("Option 1", dp(30)),
                ("Option 2", dp(30)),
                ("Option 3", dp(30)),
                ("Option 4", dp(30)),
                ("Answer", dp(30)),
                ("Category", dp(30)),
            ],
            row_data=get_all_questions(),

        )
        return data_table


if __name__ == "__main__":
    ViewQuestionsApp().run()
