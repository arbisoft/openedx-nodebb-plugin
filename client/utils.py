"""
Contains some common functions of the related app
to store and retrieve data from database.
"""
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from openedx.features.openedx_nodebb_discussion.models import EdxNodeBBUser, EdxNodeBBCategory


def save_user_relation_into_db(username, nodebb_uid):
    """
    Saves edx_userid and nodebb_uid in EdxNodeBBUser table.
    """
    relation = EdxNodeBBUser()
    relation.edx_uid = get_object_or_404(User, username=username)
    relation.nodebb_uid = nodebb_uid
    relation.save()


def get_nodebb_uid_from_username(username):
    """
    Returns nodebb_uid using edx username.
    """
    edx_user = get_object_or_404(User, username=username)
    user_relation = get_object_or_404(EdxNodeBBUser, edx_uid=edx_user)
    return user_relation.nodebb_uid


def save_category_relation_into_db(course_id, category_id):
    """
    Saves edx course key and nodebb category id in EdxNodeBBCategory table.
    """
    category_relation = EdxNodeBBCategory()
    category_relation.course_key = course_id
    category_relation.nodebb_cid = category_id
    category_relation.save()


def save_group_relation_into_db(course_id, group_slug, group_name):
    """
    Saves nodebb group slug against the course it is created.
    """
    group_relation = get_object_or_404(EdxNodeBBCategory, course_key=course_id)
    group_relation.nodebb_group_slug = group_slug
    group_relation.nodebb_group_name = group_name
    group_relation.save()


def get_category_id_from_course_id(course_id):
    """
    Returns category id using edx course id
    """
    category_relation = get_object_or_404(EdxNodeBBCategory, course_key=course_id)
    return category_relation.nodebb_cid


def get_group_slug_from_course_id(course_id):
    """
    Returns group slug using edx course id.
    """
    category_relation = get_object_or_404(EdxNodeBBCategory, course_key=course_id)
    return category_relation.nodebb_group_slug


def get_group_slug_from_category_id(category_id):
    """
    Returns nodebb group slug using nodebb  category id.
    """
    category_relation = get_object_or_404(EdxNodeBBCategory, nodebb_cid=category_id)
    return category_relation.nodebb_group_slug


def get_group_name_from_course_id(course_id):
    """
    Returns nodebb group name using edx course id.
    """
    category_relation = get_object_or_404(EdxNodeBBCategory, course_key=course_id)
    return category_relation.nodebb_group_name
