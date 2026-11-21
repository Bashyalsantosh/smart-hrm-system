from enum import Enum

from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.models.user import User, UserRole


class Permission(str, Enum):
    PATIENT_VIEW = "patient:view"
    PATIENT_CREATE = "patient:create"
    PATIENT_UPDATE = "patient:update"

    EMR_VIEW = "emr:view"
    EMR_CREATE = "emr:create"
    EMR_UPDATE = "emr:update"

    APPOINTMENT_VIEW = "appointment:view"
    APPOINTMENT_CREATE = "appointment:create"

    LAB_VIEW = "lab:view"
    LAB_CREATE = "lab:create"
    LAB_RESULT_UPDATE = "lab:result_update"

    PHARMACY_VIEW = "pharmacy:view"
    PHARMACY_CREATE = "pharmacy:create"
    PHARMACY_STOCK_UPDATE = "pharmacy:stock_update"

    BILLING_VIEW = "billing:view"
    BILLING_CREATE = "billing:create"

    USER_MANAGE = "user:manage"
    SYSTEM_ADMIN = "system:admin"


ROLE_PERMISSIONS = {

    UserRole.ADMIN: {
        permission for permission in Permission
    },

    UserRole.DOCTOR: {
        Permission.PATIENT_VIEW,
        Permission.EMR_VIEW,
        Permission.EMR_CREATE,
        Permission.EMR_UPDATE,
        Permission.APPOINTMENT_VIEW,
        Permission.LAB_VIEW,
    },

    UserRole.NURSE: {
        Permission.PATIENT_VIEW,
        Permission.EMR_VIEW,
        Permission.EMR_UPDATE,
        Permission.APPOINTMENT_VIEW,
    },

    UserRole.LAB_TECH: {
        Permission.PATIENT_VIEW,
        Permission.LAB_VIEW,
        Permission.LAB_CREATE,
        Permission.LAB_RESULT_UPDATE,
    },

    UserRole.PHARMACIST: {
        Permission.PATIENT_VIEW,
        Permission.PHARMACY_VIEW,
        Permission.PHARMACY_CREATE,
        Permission.PHARMACY_STOCK_UPDATE,
    },

    UserRole.RECEPTIONIST: {
        Permission.PATIENT_VIEW,
        Permission.PATIENT_CREATE,
        Permission.PATIENT_UPDATE,
        Permission.APPOINTMENT_VIEW,
        Permission.APPOINTMENT_CREATE,
        Permission.BILLING_VIEW,
        Permission.BILLING_CREATE,
    },
}


def require_permission(permission: Permission):

    def checker(
        current_user: User = Depends(get_current_user)
    ):

        permissions = ROLE_PERMISSIONS.get(
            current_user.role,
            set()
        )

        if permission not in permissions:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action"
            )

        return current_user

    return checker