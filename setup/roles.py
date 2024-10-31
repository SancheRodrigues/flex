from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    pass

class Viewer(AbstractUserRole):
    pass

class Expedition(AbstractUserRole):
    pass