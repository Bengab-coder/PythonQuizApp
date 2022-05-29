# HERE WE IMPORT ALL MODULES
import random
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivymd.app import MDApp
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDIcon
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from akivymd.uix.piechart import AKPieChart

# ALSO, WE IMPORT THE FUNCTIONS DECLARED IN ANOTHER FILE
from view_questions import get_all_questions

# HERE WE CHANGE THE SIZE OF THE WINDOW
Window.size = 320, 650


# DECLARATION OF CUSTOM WIDGETS THAT INHERIT FROM OTHER KNOWN WIDGETS


class CategoryButton(ToggleButton):
    pass


class OptionButton(Button):
    pass


class OptionItem(BoxLayout):
    pass


class OptionLabel(MDIcon):
    pass


# THIS IS THE MAIN APP


class QuizApp(MDApp):
    # WE INITIALIZE SOME CLASS PROPERTIES

    """THE <name>PROPERTY (all classes from the properties module, StringProperty,ListProperty,etc.)
     MAKES IF POSSIBLE TO REFERENCE THE ATTRIBUTE DIRECTLY FROM THE KV FILE """

    question = StringProperty()

    option1 = StringProperty()
    option2 = StringProperty()
    option3 = StringProperty()
    option4 = StringProperty()
    answer = StringProperty()

    # Properties to hold the background_color of each option widget.

    btn_a_bg_color = ListProperty([0, 1, 0, 0.2])
    btn_b_bg_color = ListProperty([0, 1, 0, 0.2])
    btn_c_bg_color = ListProperty([0, 1, 0, 0.2])
    btn_d_bg_color = ListProperty([0, 1, 0, 0.2])

    default_font = StringProperty("Barlow-Medium.ttf")
    question_index = NumericProperty(0)
    total_questions = NumericProperty()

    tag = StringProperty("Random")

    def __init__(self, **kwargs):
        super(QuizApp, self).__init__(**kwargs)
        self.dialog = None
        self.category = "Fundamentals"
        self.total_questions_answered = 0
        self.questions = []
        self.question_index = 0
        self.total_questions = 0
        self.piechart = None
        self.back_to_back_passed = []
        self.back_to_back_failed = []

    # THIS FUNCTION RETURNS A LIST OF RANDOM QUESTIONS SELECTED FROM THE MAIN QUESTIONS FROM THE DATABASE. IT ACCEPTS
    # TWO OPTIONAL ARGUMENTS , CATEGORY, WHICH WHEN SPECIFIED TELLS THE FUNCTION THAT WE WANT IT TO RETURN ONLY THE
    # QUESTION WITH A SPECIFIC TAG OR CATEGORY. ALSO, THE LENGTH PARAMETER TELLS THE FUNCTION THE NUMBER OF RANDOM QUESTIONS TO RETURN.

    def generate_random_questions(self, category=None, length: int = 10):
        all_questions = get_all_questions()

        if category is not None:
            all_questions = [question for question in all_questions if question[-1] == category]

        questions = []
        stored_ids = []
        i = 0
        if len(all_questions) >= length:
            while i < length:
                random_number = random.randrange(1, len(all_questions))
                question = all_questions[random_number]
                if question[0] not in stored_ids:
                    questions.append(question)
                    stored_ids.append(question[0])
                    i += 1
        else:
            questions = all_questions

        return questions

    # THIS METHOD BUILDS OUR APP AND INITIALIZE ALL WIDGETS IN THE KV FILE.
    def build(self):
        return Builder.load_file("quiz.kv")

    # KIVY FIRES THIS METHOD ONCE THE APP HAS FULLY STARTED.
    # KNOW THAT WE CANNOT INITIALIZE ANY WIDGET THAT NEEDS TO BE ON SCREEN IN THE
    # __init__() CONSTRUCTOR BECAUSE BY THEN ALL WIDGETS HAS NOT FINISHED LOADING.

    def on_start(self):
        """Here we register a method to be called when the screen is pressed.
        Then we can check if the click position is inside any of the
        optoins which means that we have selected an option"""

        self.root.ids.options_list.bind(on_touch_down=self.bg_released)

    # THIS FUNCTION STARTS THE QUIZ.
    def start_quiz(self, filter=None):

        self.back_to_back_passed = []
        self.back_to_back_failed = []

        if filter:
            self.questions = self.generate_random_questions(self.category)
        else:
            self.questions = self.generate_random_questions()
        self.question_index = 0
        self.total_questions = len(self.questions)
        self.total_questions_answered = 0

        self.refresh_screen(1)

        if self.root.ids.sm.current != "quiz_screen":
            self.root.ids.sm.current = "quiz_screen"

    """THIS METHOD IS CALLED AUTOMATICALLY BY KIVY WHEN THE BACKGROUND SCREEN IS PRESSED. THEN INSIDE THE FUNCTION'S 
    SUITE, WE CHECK IF THE CLICK POSITION IS WITHIN ANY OF THE OPTION WIDGETS. IF TRUE: THEN WE ALSO CHECK IF THE TET 
    IF THAT OPTION IS EQUAL TO THE VALUE OF self.answer, WHICH MEANS THAT THE USER WAS CORRECT. THE COLOR IF THE 
    OPTION WIDGET IS CHANGED TO GREEN IF THE USER IS CORRECT OTHERWISE RED, THEN THE PROGRAM NOW SHOWS THE USER THE 
    RIGHT ANSWER BY HIGHLIGHTING IT GREEN. ALSO IN THIS METHOD  WE KEEP TRACK OF THE USERS PERFORMANCE. FOR INSTANCE 
    , IF THEY HAVE ANSWERD 3 QUESTIONS BACK-TO-BACK CORRECTLY OR NOT. """

    def bg_released(self, layout, touch):
        option_object = None
        x, y = touch.x, touch.y
        if self.root.ids.options_list.collide_point(x, y):
            if self.root.ids.opt_a.collide_point(x, y):
                option_object = self.root.ids.btn_a
            elif self.root.ids.opt_b.collide_point(x, y):
                option_object = self.root.ids.btn_b
            elif self.root.ids.opt_c.collide_point(x, y):
                option_object = self.root.ids.btn_c
            elif self.root.ids.opt_d.collide_point(x, y):
                option_object = self.root.ids.btn_d

            if option_object:
                if option_object.text == self.answer:
                    if option_object.text == self.option1:
                        self.btn_a_bg_color = (0, 1, 0, 0.2)
                    elif option_object.text == self.option2:
                        self.btn_b_bg_color = (0, 1, 0, 0.2)
                    elif option_object.text == self.option3:
                        self.btn_c_bg_color = (0, 1, 0, 0.2)
                    elif option_object.text == self.option4:
                        self.btn_d_bg_color = (0, 1, 0, 0.2)
                    self.total_questions_answered += 1

                    self.back_to_back_passed.append(1)
                    self.back_to_back_failed.clear()

                else:
                    if option_object.text == self.option1:
                        self.btn_a_bg_color = (1, 0, 0, 0.2)
                    elif option_object.text == self.option2:
                        self.btn_b_bg_color = (1, 0, 0, 0.2)
                    elif option_object.text == self.option3:
                        self.btn_c_bg_color = (1, 0, 0, 0.2)
                    elif option_object.text == self.option4:
                        self.btn_d_bg_color = (1, 0, 0, 0.2)

                    if self.root.ids.btn_a.text == self.answer:
                        self.btn_a_bg_color = (0, 1, 0, 0.2)
                    elif self.root.ids.btn_b.text == self.answer:
                        self.btn_b_bg_color = (0, 1, 0, 0.2)
                    elif self.root.ids.btn_c.text == self.answer:
                        self.btn_c_bg_color = (0, 1, 0, 0.2)
                    elif self.root.ids.btn_d.text == self.answer:
                        self.btn_d_bg_color = (0, 1, 0, 0.2)

                    self.back_to_back_failed.append(1)
                    self.back_to_back_passed.clear()

                if len(self.back_to_back_passed) == 3:
                    self.show_alert_dialog("Congratulations, you are on your way to being a python master !")

                elif len(self.back_to_back_passed) == 6:
                    self.show_alert_dialog("Hurray, You are one step away from being a python master !")

                if len(self.back_to_back_failed) == 3 or len(self.back_to_back_failed) == 6:
                    if self.question_index < len(self.questions):
                        self.show_alert_dialog("Don't give up, the game is still on !")

                Clock.schedule_once(self.refresh_screen, 0.5)  # WE WAIT FOR HALF A SECOND BEFORE WE CONTINUE WITH THE
                # NEXT QUESTION
            else:
                pass
        else:
            pass

    def option_clicked(self, option_object):
        pass

    # THIS METHOD UPDATES THE SCREEN AND MAKES ALL CHANGES
    def refresh_screen(self, dt):
        if self.question_index >= len(self.questions):
            self.end_quiz()
            return

        self.root.ids.question_count.text = f"Question {self.question_index}/{len(self.questions)}"
        question = self.questions[self.question_index]
        self.question = question[1].title()
        self.option1 = question[2]
        self.option2 = question[3]
        self.option3 = question[4]
        self.option4 = question[5]
        self.answer = question[6]
        self.tag = question[7]

        normal_color = [1, 0, 0, 0]

        self.btn_a_bg_color = normal_color
        self.btn_b_bg_color = normal_color
        self.btn_c_bg_color = normal_color
        self.btn_d_bg_color = normal_color

        self.question_index += 1

    # THE END QUIZ METHOD STOPS THE QUIZ AND CALCULATES THE USERS PERFORMANCE.

    def end_quiz(self):
        self.root.ids.sm.current = "scoreboard"
        self.category = "Fundamentals"

        self.root.ids.fundamentals_btn.state = "down"
        self.root.ids.algo_ds_btn.state = "normal"
        self.root.ids.oop_btn.state = "normal"

        passed_p, failed_p = self.get_performance_percentage(self.total_questions, self.total_questions_answered)

        # I THINK ITS NICE TO HAVE A SMALL PIE CHART TO DISPLAY THE USER'S PERFORMANCE NICELY
        self.piechart = AKPieChart(
            items=[{"Passed": passed_p, "Failed": failed_p}],
            duration=2,
        )

        self.piechart.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.piechart.size_hint = (None, None)
        self.piechart.height = 250
        self.piechart.width = 250

        self.root.ids.score_board.add_widget(self.piechart)

    def remove_piechart(self, screen):
        if self.piechart in screen.children:
            screen.remove_widget(self.piechart)

    def get_performance_percentage(self, total_questions, total_questions_answered):
        passed_marks = total_questions_answered

        passed_p = int((total_questions_answered / total_questions) * 100)

        failed_p = 100 - passed_p
        return passed_p, failed_p

    # THIS METHOD IS CALLED EACH TIME WE ARE SELECTING A CATEGORY FOR THE QUIZ FILTER.

    def on_select_category(self, category_button):
        self.category = category_button.text

    # THIS METHOD DISPLAYS A DIALOG ON THE SCREEN WITH A CONFIRM BUTTON.
    def show_alert_dialog(self, text):
        if not self.dialog:
            self.dialog = MDDialog(
                title=text,
                auto_dismiss=False,
                buttons=[
                    MDFlatButton(
                        text="Thanks",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, dialog):
        if self.dialog:
            self.dialog.dismiss()


QuizApp().run()
