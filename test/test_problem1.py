import unittest
from src import problem1

class TestCleanNames(unittest.TestCase):
    '''
        Checking code returning whether appropriate output.
    '''
    def setUp(self):
        self.raw_names = [
        'SPV Inc., DBA: Super Company',
        'Michael Forsky LLC d.b.a F/B Burgers .',
        '*** Youthful You Aesthetics ***',
        'Aruna Indika (dba. NGXess)',
        'Diot SA, - D. B. A. *Diot-Technologies*',
        'PERFECT PRIVACY, LLC, d-b-a Perfection,',
        'PostgreSQL DB Analytics',
        '/JAYE INC/',
        ' ETABLISSEMENTS SCHEPENS /D.B.A./ ETS_SCHEPENS',
        'DUIKERSTRAINING OOSTENDE | D.B.A.: D.T.O. '
        ]

        self.cleaned_name_pairs = [
        ('SPV Inc', 'Super Company'),
        ('Michael Forsky LLC', 'F/B Burgers'),
        ('Youthful You Aesthetics', None),
        ('Aruna Indika', 'NGXess'),
        ('Diot SA', 'Diot-Technologies'),
        ('PERFECT PRIVACY, LLC', 'Perfection'),
        ('PostgreSQL DB Analytics', None),
        ('JAYE INC', None),
        ('ETABLISSEMENTS SCHEPENS', 'ETS SCHEPENS'),
        ('DUIKERSTRAINING OOSTENDE', 'D.T.O'),
        ]
    
    def tearDown(self):
        pass

    def test_clean_names(self):
        return_clean_names = problem1.clean_names(self.raw_names)
        self.assertEqual(return_clean_names, self.cleaned_name_pairs)

if __name__ == '__main__':
    unittest.main()