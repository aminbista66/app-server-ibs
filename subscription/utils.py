def permission_filter(user_permissions, admin_permissions):
    user_permissions = set(user_permissions)
    admin_permissions = set(admin_permissions)

    common_permissions = admin_permissions.intersection(user_permissions)
    return list(common_permissions)