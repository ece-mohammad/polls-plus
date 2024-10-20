#!/usr/bin/env python


# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones intact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# manage.py dumpscript polls
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script
import os, sys
from django.db import transaction

class BasicImportHelper:

    def pre_import(self):
        pass

    @transaction.atomic
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(self, original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = { pk_name: pk_value }
        the_obj = the_class.objects.get(**search_data)
        #print(the_obj)
        return the_obj


    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper
    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper ) , {} )()
except ImportError as e:
    # From Python 3.3 we can check e.name - string match is for backward compatibility.
    if 'import_helper' in str(e):
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
    from dateutil.tz import tzoffset
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)

def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()

def import_data():
    # Initial Imports

    # Processing model: polls.models.Question

    from polls.models import Question

    polls_question_1 = Question()
    polls_question_1.question_text = 'Answer to the Ultimate Question'
    polls_question_1.pub_date = dateutil.parser.parse("2024-10-20T11:23:04+00:00")
    polls_question_1.exp_date = dateutil.parser.parse("2025-10-20T11:23:16+00:00")
    polls_question_1 = importer.save_or_locate(polls_question_1)

    polls_question_2 = Question()
    polls_question_2.question_text = 'In python, which of the following data types is mutable?'
    polls_question_2.pub_date = dateutil.parser.parse("2024-09-23T01:35:00.639000+00:00")
    polls_question_2.exp_date = dateutil.parser.parse("2024-11-07T08:47:42.965195+00:00")
    polls_question_2 = importer.save_or_locate(polls_question_2)

    polls_question_3 = Question()
    polls_question_3.question_text = 'Which programming language do you prefer?'
    polls_question_3.pub_date = dateutil.parser.parse("2024-09-23T01:34:33.179000+00:00")
    polls_question_3.exp_date = dateutil.parser.parse("2024-11-07T08:47:42.965195+00:00")
    polls_question_3 = importer.save_or_locate(polls_question_3)

    polls_question_4 = Question()
    polls_question_4.question_text = 'Which band do you like the most?'
    polls_question_4.pub_date = dateutil.parser.parse("2024-09-23T00:14:19.074000+00:00")
    polls_question_4.exp_date = dateutil.parser.parse("2024-11-07T08:47:42.965195+00:00")
    polls_question_4 = importer.save_or_locate(polls_question_4)

    polls_question_5 = Question()
    polls_question_5.question_text = 'Which series do you like the most?'
    polls_question_5.pub_date = dateutil.parser.parse("2024-09-23T00:14:07.100000+00:00")
    polls_question_5.exp_date = dateutil.parser.parse("2024-11-07T08:47:42.965195+00:00")
    polls_question_5 = importer.save_or_locate(polls_question_5)

    polls_question_6 = Question()
    polls_question_6.question_text = 'Which movie do you like the most?'
    polls_question_6.pub_date = dateutil.parser.parse("2024-09-23T00:13:58.021000+00:00")
    polls_question_6.exp_date = dateutil.parser.parse("2024-11-07T08:47:42.965195+00:00")
    polls_question_6 = importer.save_or_locate(polls_question_6)

    polls_question_7 = Question()
    polls_question_7.question_text = 'Which food do you like the most?'
    polls_question_7.pub_date = dateutil.parser.parse("2024-09-23T00:13:46.627000+00:00")
    polls_question_7.exp_date = dateutil.parser.parse("2024-11-07T08:47:42.965195+00:00")
    polls_question_7 = importer.save_or_locate(polls_question_7)

    polls_question_8 = Question()
    polls_question_8.question_text = 'Which color do you like the most?'
    polls_question_8.pub_date = dateutil.parser.parse("2024-09-23T00:07:49.300000+00:00")
    polls_question_8.exp_date = dateutil.parser.parse("2024-11-07T08:47:42.965195+00:00")
    polls_question_8 = importer.save_or_locate(polls_question_8)

    # Processing model: polls.models.Choice

    from polls.models import Choice

    polls_choice_1 = Choice()
    polls_choice_1.question = polls_question_4
    polls_choice_1.choice_text = 'Linkin Park'
    polls_choice_1.votes = 0
    polls_choice_1 = importer.save_or_locate(polls_choice_1)

    polls_choice_2 = Choice()
    polls_choice_2.question = polls_question_4
    polls_choice_2.choice_text = 'Evanescence'
    polls_choice_2.votes = 0
    polls_choice_2 = importer.save_or_locate(polls_choice_2)

    polls_choice_3 = Choice()
    polls_choice_3.question = polls_question_4
    polls_choice_3.choice_text = 'Disturbed'
    polls_choice_3.votes = 0
    polls_choice_3 = importer.save_or_locate(polls_choice_3)

    polls_choice_4 = Choice()
    polls_choice_4.question = polls_question_4
    polls_choice_4.choice_text = 'Nightwish'
    polls_choice_4.votes = 0
    polls_choice_4 = importer.save_or_locate(polls_choice_4)

    polls_choice_5 = Choice()
    polls_choice_5.question = polls_question_5
    polls_choice_5.choice_text = 'Supernatural'
    polls_choice_5.votes = 0
    polls_choice_5 = importer.save_or_locate(polls_choice_5)

    polls_choice_6 = Choice()
    polls_choice_6.question = polls_question_2
    polls_choice_6.choice_text = 'string'
    polls_choice_6.votes = 0
    polls_choice_6 = importer.save_or_locate(polls_choice_6)

    polls_choice_7 = Choice()
    polls_choice_7.question = polls_question_2
    polls_choice_7.choice_text = 'int'
    polls_choice_7.votes = 0
    polls_choice_7 = importer.save_or_locate(polls_choice_7)

    polls_choice_8 = Choice()
    polls_choice_8.question = polls_question_2
    polls_choice_8.choice_text = 'float'
    polls_choice_8.votes = 0
    polls_choice_8 = importer.save_or_locate(polls_choice_8)

    polls_choice_9 = Choice()
    polls_choice_9.question = polls_question_2
    polls_choice_9.choice_text = 'list'
    polls_choice_9.votes = 2
    polls_choice_9 = importer.save_or_locate(polls_choice_9)

    polls_choice_10 = Choice()
    polls_choice_10.question = polls_question_2
    polls_choice_10.choice_text = 'tuple'
    polls_choice_10.votes = 0
    polls_choice_10 = importer.save_or_locate(polls_choice_10)

    polls_choice_11 = Choice()
    polls_choice_11.question = polls_question_3
    polls_choice_11.choice_text = 'C'
    polls_choice_11.votes = 0
    polls_choice_11 = importer.save_or_locate(polls_choice_11)

    polls_choice_12 = Choice()
    polls_choice_12.question = polls_question_3
    polls_choice_12.choice_text = 'C++'
    polls_choice_12.votes = 0
    polls_choice_12 = importer.save_or_locate(polls_choice_12)

    polls_choice_13 = Choice()
    polls_choice_13.question = polls_question_3
    polls_choice_13.choice_text = 'python'
    polls_choice_13.votes = 0
    polls_choice_13 = importer.save_or_locate(polls_choice_13)

    polls_choice_14 = Choice()
    polls_choice_14.question = polls_question_3
    polls_choice_14.choice_text = 'Rust'
    polls_choice_14.votes = 0
    polls_choice_14 = importer.save_or_locate(polls_choice_14)

    polls_choice_15 = Choice()
    polls_choice_15.question = polls_question_5
    polls_choice_15.choice_text = 'Suits'
    polls_choice_15.votes = 0
    polls_choice_15 = importer.save_or_locate(polls_choice_15)

    polls_choice_16 = Choice()
    polls_choice_16.question = polls_question_5
    polls_choice_16.choice_text = 'Hannibal'
    polls_choice_16.votes = 0
    polls_choice_16 = importer.save_or_locate(polls_choice_16)

    polls_choice_17 = Choice()
    polls_choice_17.question = polls_question_5
    polls_choice_17.choice_text = 'F.R.I.E.N.D.S'
    polls_choice_17.votes = 0
    polls_choice_17 = importer.save_or_locate(polls_choice_17)

    polls_choice_18 = Choice()
    polls_choice_18.question = polls_question_6
    polls_choice_18.choice_text = 'Green Mile'
    polls_choice_18.votes = 0
    polls_choice_18 = importer.save_or_locate(polls_choice_18)

    polls_choice_19 = Choice()
    polls_choice_19.question = polls_question_6
    polls_choice_19.choice_text = 'Forrest Gump'
    polls_choice_19.votes = 0
    polls_choice_19 = importer.save_or_locate(polls_choice_19)

    polls_choice_20 = Choice()
    polls_choice_20.question = polls_question_6
    polls_choice_20.choice_text = 'Sully'
    polls_choice_20.votes = 0
    polls_choice_20 = importer.save_or_locate(polls_choice_20)

    polls_choice_21 = Choice()
    polls_choice_21.question = polls_question_6
    polls_choice_21.choice_text = 'Django unchained'
    polls_choice_21.votes = 0
    polls_choice_21 = importer.save_or_locate(polls_choice_21)

    polls_choice_22 = Choice()
    polls_choice_22.question = polls_question_6
    polls_choice_22.choice_text = 'The Dark Knight'
    polls_choice_22.votes = 0
    polls_choice_22 = importer.save_or_locate(polls_choice_22)

    polls_choice_23 = Choice()
    polls_choice_23.question = polls_question_7
    polls_choice_23.choice_text = 'Pizza'
    polls_choice_23.votes = 0
    polls_choice_23 = importer.save_or_locate(polls_choice_23)

    polls_choice_24 = Choice()
    polls_choice_24.question = polls_question_7
    polls_choice_24.choice_text = 'Burger'
    polls_choice_24.votes = 0
    polls_choice_24 = importer.save_or_locate(polls_choice_24)

    polls_choice_25 = Choice()
    polls_choice_25.question = polls_question_7
    polls_choice_25.choice_text = 'Grilled Chicken'
    polls_choice_25.votes = 0
    polls_choice_25 = importer.save_or_locate(polls_choice_25)

    polls_choice_26 = Choice()
    polls_choice_26.question = polls_question_8
    polls_choice_26.choice_text = 'Black'
    polls_choice_26.votes = 6
    polls_choice_26 = importer.save_or_locate(polls_choice_26)

    polls_choice_27 = Choice()
    polls_choice_27.question = polls_question_8
    polls_choice_27.choice_text = 'blue'
    polls_choice_27.votes = 0
    polls_choice_27 = importer.save_or_locate(polls_choice_27)

    polls_choice_28 = Choice()
    polls_choice_28.question = polls_question_8
    polls_choice_28.choice_text = 'red'
    polls_choice_28.votes = 0
    polls_choice_28 = importer.save_or_locate(polls_choice_28)

    polls_choice_29 = Choice()
    polls_choice_29.question = polls_question_8
    polls_choice_29.choice_text = 'green'
    polls_choice_29.votes = 0
    polls_choice_29 = importer.save_or_locate(polls_choice_29)

    polls_choice_30 = Choice()
    polls_choice_30.question = polls_question_1
    polls_choice_30.choice_text = '42'
    polls_choice_30.votes = 0
    polls_choice_30 = importer.save_or_locate(polls_choice_30)

    polls_choice_31 = Choice()
    polls_choice_31.question = polls_question_1
    polls_choice_31.choice_text = 'foobar'
    polls_choice_31.votes = 0
    polls_choice_31 = importer.save_or_locate(polls_choice_31)

