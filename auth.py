#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools

PERMISSIONS = {}
OWNER_IDS = tuple()

def sender_requires(_func=None, *, permission=None, on_violation=None):
    def decorator_permission(func):
        @functools.wraps(func)
        def wrapper_permission(message):
            try:
                user_id = message.from_user.id
                has_access = user_id in OWNER_IDS
                if not has_access:
                    has_access = user_id in PERMISSIONS.get(permission,[])
                if not has_access and callable(on_violation):
                    has_access = on_violation(message, func, permission)
                return func(message) if has_access else None
            except Exception:
                return None
        return wrapper_permission

    if _func is None:
        return decorator_permission
    else:
        return decorator_permission(_func)

def chat_requires(_func=None, *, permission=None, on_violation=None):
    def decorator_permission(func):
        @functools.wraps(func)
        def wrapper_permission(message):
            try:
                chat_id = message.chat.id
                has_access = chat_id in PERMISSIONS.get(permission,[])
                if not has_access and callable(on_violation):
                    has_access = on_violation(message, func, permission)
                return func(message) if has_access else None
            except Exception:
                return None
        return wrapper_permission

    if _func is None:
        return decorator_permission
    else:
        return decorator_permission(_func)
