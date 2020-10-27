"""Unit test for recommender_functions.movies_to_users"""
import unittest

from recommender_functions import movies_to_users

class TestMoviesToUsers(unittest.TestCase):
    

    def test_movies_to_users(self):
        actual = movies_to_users({1: {10: 3.0}, 2: {10: 3.5}})
        expected = {10: [1, 2]}
        self.assertEqual(actual, expected) #2 people rate same 1 mov 
        
    def test_movies_to_users_2(self):
        """ testing movies_to_users under the condition that there is only one 
        user watch one movie in user_ratings
        """
        actual = movies_to_users({1: {10: 3.0}})
        expected = {10: [1]}
        self.assertEqual(actual, expected) #1 people rate 1 mov
        
    def test_movies_to_users_3(self):
        """ testing movies_to_users under the condition that there is two users 
        watch one different movie in user_ratings
        """        
        actual = movies_to_users({1: {10: 3.0}, 2: {20: 3.5}})
        expected = {10: [1], 20: [2]} 
        self.assertEqual(actual, expected) #2 people rate different mov
        
    def test_movies_to_users_4(self):
        """ testing movies_to_users under the condition that there is more than 
        two users watch same and different movie in user_ratings
        """        
        actual = movies_to_users({1: {10: 3.0}, 2: {20: 3.5}, 3: {10: 2.5}})
        expected = {10: [1, 3], 20: [2]}
        self.assertEqual(actual, expected) #2+ people watch same & different mov
    
    def test_movies_to_users_5(self):
        """ testing movies_to_users under the condition that there is two users 
        watch more than one movies in user_ratings
        """        
        actual = movies_to_users({1: {10: 3.0, 20: 2.0}, 2: {20: 3.5}})
        expected = {10: [1], 20: [1, 2]}
        self.assertEqual(actual, expected) #2 people watch 1+ mov
        
    def test_movies_to_users_6(self):
        """ testing movies_to_users under the condition that user_ratings is 
        empty
        """        
        actual = movies_to_users({})
        expected = {}
        self.assertEqual(actual, expected) #empty dict
        

    # Add tests below to create a complete set of tests without redundant tests
    # Redundant tests are tests that would only catch bugs that another test
    # would also catch.

if __name__ == '__main__':
    unittest.main(exit=False)
