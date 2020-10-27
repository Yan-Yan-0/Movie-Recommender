"""CSC108 A3 recommender starter code."""

from typing import TextIO, List, Dict

from recommender_constants import (MovieDict, Rating, UserRatingDict, 
                                   MovieUserDict)
from recommender_constants import (MOVIE_FILE_STR, RATING_FILE_STR,
                                   MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL,
                                   MOVIE_USER_DICT_SMALL)

############## HELPER FUNCTIONS

def get_similarity(user1: Rating, user2: Rating) -> float:
    """Return the a similarity score between user1 and user2 based on their
    movie ratings. The returned similarity score is a number between 0 and 1
    inclusive. The higher the number, the more similar user1 and user2 are.

    For those who are curious, this type of similarity measure is called the
    "cosine similarity".

    >>> r1 = {1: 4.5, 2: 3.0, 3: 1.0}
    >>> r2 = {2: 4.5, 3: 3.5, 4: 1.5, 5: 5.0}
    >>> s1 = get_similarity(r1, r1)
    >>> abs(s1 - 1.0) < 0.0001 # s1 is close to 1.0
    True
    >>> s2 = get_similarity(r1, {6: 4.5})
    >>> abs(s2 - 0.0) < 0.0001 # s2 is close to 0.0
    True
    >>> round(get_similarity(r1, r2), 2)
    0.16
    """
    shared = 0.0
    for m_id in user1:
        if m_id in user2:
            shared += user1[m_id] * user2[m_id]
    norm1 = 0.0
    for m_id in user1:
        norm1 = norm1 + user1[m_id] ** 2
    norm2 = 0.0
    for m_id in user2:
        norm2 = norm2 + user2[m_id] ** 2
    return (shared * shared) / (norm1 * norm2)


############## STUDENT CONSTANTS




############## STUDENT HELPER FUNCTIONS

def get_num_user_movies(target_rating: Rating,  
                        user_ratings: UserRatingDict,
                        user: int) -> int:
    """Return the number of movies for user in user_ratings rated that is above 
    or equal to 3.5 and not in target_rating.
    
    >>> get_num_user_movies({12345: 3.3} ,USER_RATING_DICT_SMALL, 1)
    2
    >>> get_num_user_movies({12345: 3.3} ,USER_RATING_DICT_SMALL, 2)
    1
    """
    num = 0 
    for mov in user_ratings[user]:
        if user_ratings[user][mov] >= 3.5 and mov not in target_rating:
            num = num + 1
    return num 


def get_same_index(mov_list: list) -> list:
    """Return a list of the first index of two repeated items in mov_list, 
    return empty list if there is no two co-occured identical item.
    
    >>> get_same_index([1, 2, 3])
    []
    >>> get_same_index([2, 2, 7, 7])
    [0, 2]
    """
    
    index_list = []
    for i in range(len(mov_list)-1):
        if mov_list[i] == mov_list[i + 1]:
            index_list.append(i)
    return index_list


def index_sorted_list(ori_list: list, index_list: list) -> list:
    """Sort the ori_list at index in index_list.
    
    >>> index_sorted_list([1, 3, 2, 4, 5, 7, 6], [1, 2, 3])
    [1, 2, 3, 4, 5, 7, 6]
    """
    
    if index_list != []:
        for i in index_list:
            if ori_list[i] > ori_list[i + 1]:
                ori_list[i], ori_list[i + 1] = ori_list[i + 1], ori_list[i]
    return ori_list
        
    

def get_candidate_mov_info(similar_users_dict: Dict[int, float], 
                           target_rating: Rating, user_ratings: UserRatingDict,
                           movie_users: MovieUserDict) -> Rating:
    """get the score of movies using user_ratings and movie_users from users 
    similar to target_rating's user
    
    >>> get_candidate_mov_info({1: 0.5663716814159292}, {302156: 4.5}, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL)
    {68375: 0.2831858407079646}
    """
    
    candidate_mov_info = {}
    for user in similar_users_dict:
        rated_infom = user_ratings[user]
        user_similarity_score = similar_users_dict[user]
        num_user_movie = get_num_user_movies(target_rating, user_ratings, user)
        for mov in rated_infom:
            movie_pouplarity = len(movie_users[mov])
            criteria = rated_infom[mov] >= 3.5 and mov not in target_rating
            score = user_similarity_score / (num_user_movie * movie_pouplarity)
            if criteria and mov not in candidate_mov_info:
                candidate_mov_info[mov] = score 
            elif criteria and mov in candidate_mov_info:
                candidate_mov_info[mov] = candidate_mov_info[mov] + score 
    return candidate_mov_info
    

############## STUDENT FUNCTIONS

def read_movies(movie_file: TextIO) -> MovieDict:
    """Return a dictionary containing movie id to (movie name, movie genres)
    in the movie_file.

    >>> movfile = open('movies_tiny.csv')
    >>> movies = read_movies(movfile)
    >>> movfile.close()
    >>> 68735 in movies
    True
    >>> movies[124057]
    ('Kids of the Round Table', [])
    >>> len(movies)
    4
    >>> movies == MOVIE_DICT_SMALL
    True
    """
    
    movie_dict = {}
    movie_file_list = movie_file.readlines()
    movie_file_list = movie_file_list[1:]
    for i in range(len(movie_file_list)):
        movie_file_list[i] = movie_file_list[i].strip()
    for movinfo in movie_file_list:
        movinfo_list = movinfo.split(',')
        genres = movinfo_list[4:]
        movie_dict[int(movinfo_list[0])] = (movinfo_list[1], genres)
    return movie_dict


def read_ratings(rating_file: TextIO) -> UserRatingDict:
    """Return a dictionary containing user id to {movie id: ratings} for the
    collection of user movie ratings in rating_file.

    >>> rating_file = open('ratings_tiny.csv')
    >>> ratings = read_ratings(rating_file)
    >>> rating_file.close()
    >>> len(ratings)
    2
    >>> ratings[1]
    {2968: 1.0, 3671: 3.0}
    >>> ratings[2]
    {10: 4.0, 17: 5.0}
    """

    rating_dict = {}
    
    rating_file_list = rating_file.readlines()
    rating_file_list = rating_file_list[1:]
    for ratinfo in rating_file_list:
        ratinfo_list = ratinfo.split(',')
        movid = int(ratinfo_list[1])
        rating = float(ratinfo_list[2])
        userid = int(ratinfo_list[0])
        if userid not in rating_dict:
            rating_dict[userid] = {movid: rating}
        else:
            rating_dict[userid][movid] = rating
    return rating_dict


def remove_unknown_movies(user_ratings: UserRatingDict, 
                          movies: MovieDict) -> None:
    """Modify the user_ratings dictionary so that only movie ids that are in the
    movies dictionary is remaining. Remove any users in user_ratings that have
    no movies rated.

    >>> small_ratings = {1001: {68735: 5.0, 302156: 3.5, 10: 4.5}, 1002: {11: 3.0}}
    >>> remove_unknown_movies(small_ratings, MOVIE_DICT_SMALL)
    >>> len(small_ratings)
    1
    >>> small_ratings[1001]
    {68735: 5.0, 302156: 3.5}
    >>> 1002 in small_ratings
    False
    """

    unknown_mov = []
    empty_user = []
    for user in user_ratings:
        rated_info = user_ratings[user]
        for rated_mov in rated_info:
            if rated_mov not in movies:
                unknown_mov.append(rated_mov)
        for mov in unknown_mov:
            if mov in rated_info:
                del user_ratings[user][mov]
        if user_ratings[user] == {}:
            empty_user.append(user)
    for users in empty_user:
        del user_ratings[users]
   

def movies_to_users(user_ratings: UserRatingDict) -> MovieUserDict:
    """Return a dictionary of movie ids to list of users who rated the movie,
    using information from the user_ratings dictionary of users to movie
    ratings dictionaries.

    >>> result = movies_to_users(USER_RATING_DICT_SMALL)
    >>> result == MOVIE_USER_DICT_SMALL
    True
    """

    mov_user_dic = {}
    for user in user_ratings:
        for rated_mov in user_ratings[user]:
            if rated_mov not in mov_user_dic:
                mov_user_dic[int(rated_mov)] = [int(user)]
            else:
                mov_user_dic[int(rated_mov)].append(int(user))
    for mov_id in mov_user_dic:
        mov_user_dic[mov_id].sort()
    return mov_user_dic



def get_users_who_watched(movie_ids: List[int],
                          movie_users: MovieUserDict) -> List[int]:
    """Return the list of user ids in moive_users who watched at least one
    movie in moive_ids.

    >>> get_users_who_watched([293660], MOVIE_USER_DICT_SMALL)
    [2]
    >>> lst = get_users_who_watched([68735, 302156], MOVIE_USER_DICT_SMALL)
    >>> len(lst)
    2
    """
    rated_lst = []
    watched_lst = []
    for mov in movie_users: 
        if mov in movie_ids:
            rated_lst = rated_lst + movie_users[mov]
    for userid in rated_lst:
        if userid not in watched_lst:
            watched_lst.append(userid)
    watched_lst.sort()
    return watched_lst
    


def get_similar_users(target_rating: Rating,
                      user_ratings: UserRatingDict,
                      movie_users: MovieUserDict) -> Dict[int, float]:
    """Return a dictionary of similar user ids to similarity scores between the
    similar user's movie rating in user_ratings dictionary and the
    target_rating. Only return similarites for similar users who has at least
    one rating in movie_users dictionary that appears in target_Ratings.

    >>> sim = get_similar_users({293660: 4.5}, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL)
    >>> len(sim)
    1
    >>> round(sim[2], 2)
    0.86
    """
    
    similar_user_dic = {}
    target_mov = []
    for mov in target_rating:
        target_mov.append(mov)
    candidate = get_users_who_watched(target_mov, movie_users) #a list 
    for can in candidate:
        can_rating = user_ratings[can]
        similar_score = get_similarity(target_rating, can_rating)
        similar_user_dic[can] = similar_score
    return  similar_user_dic
    
    
def recommend_movies(target_rating: Rating,
                     movies: MovieDict, 
                     user_ratings: UserRatingDict,
                     movie_users: MovieUserDict,
                     num_movies: int) -> List[int]:
    """Return a list of num_movies movie id recommendations for a target user 
    with target_rating of previous movies. The recommendations come from movies
    dictionary, and are based on movies that "similar users" data in
    user_ratings / movie_users dictionaries.

    >>> recommend_movies({302156: 4.5}, MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL, 2)
    [68735]
    >>> recommend_movies({68735: 4.5}, MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL, 2)
    [302156, 293660]
    """

    candidate_mov_info = {}
    mov_recommend = []
    similar_users = get_similar_users(target_rating, user_ratings, movie_users)
    candidate_mov_info = get_candidate_mov_info(similar_users, target_rating, 
                                                user_ratings, movie_users)    
    candidate_mov_score = sorted(candidate_mov_info.values(), reverse=True)
    for sco in candidate_mov_score:
        for movie in candidate_mov_info:
            if sco == candidate_mov_info[movie]:
                mov_recommend.append(movie)
    same_score_index = get_same_index(candidate_mov_score)
    mov_recommend = index_sorted_list(mov_recommend, same_score_index)
    if len(mov_recommend) > num_movies:
        mov_recommend = mov_recommend[:num_movies + 1]
    return mov_recommend
             
                


if __name__ == '__main__':
    """Uncomment to run doctest"""
    #import doctest
    #doctest.testmod()
