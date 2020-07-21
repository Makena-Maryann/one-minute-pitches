import unittest
from app import db
from app.models import User,Pitch

class PitchModelTest(unittest.TestCase):
    def setup(self):
        self.user_Makena = User(username = 'Maryann',password = 'tomato', email = 'maks@gmail.com')
        
        self.new_pitch = Pitch(title='Interviews',pitch='I am qualified',user = self.user_Makena)

    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.title,'Interviews')
        self.assertEquals(self.new_pitch.pitch,'I am qualified')
        self.assertEquals(self.new_pitch.user,self.user_Makena)

    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)    

    def test_get_pitch_by_id(self):
        self.new_pitch.save_pitch()
        got_pitch = Pitch.get_pitches(2)
        self.assertTrue(len(got_pitch) == 1)