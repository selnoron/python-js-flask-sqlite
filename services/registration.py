from flask import session
from services.database.database import User, DB


class CheckEmail:
    """Check validation of email"""

    @staticmethod
    def check_email(em) -> bool:
        if not isinstance(em, str):
            return 1
        email_elements: list[str] = em.split("@")
        if "" in email_elements:
            return 1
        if len(email_elements) != 2:
            return 1
        if email_elements[0] != email_elements[0].lower():
            return 1
        upg_ems = email_elements[1].split('.')
        if len(upg_ems) != 2:
            return 1
        if "" in upg_ems:
            return 1
        if (
            upg_ems[0] != upg_ems[0].lower()
        ) or (
            upg_ems[1] != upg_ems[1].lower()
        ):
            return 1
        return 0


# функция регистрации пользователя
# вернет:
# 0 - ОК
# 1 - все плохо
def registrate(data: dict) -> int:
    user = User(
        login=data.get("login"),
        email=data.get("email"),
        password=data.get("password"),
        os_version="Windows"
    )

    if not isinstance(user.login, str):
        return 1
    
    if not isinstance(user.password, str):
        return 1
    
    if user.password != data.get("rpassword"):
        return 1

    if CheckEmail.check_email(user.email):
        return 1

    db : DB = DB()
    result_of_registration = db.registrate_user(data=user)

    print(result_of_registration)

    if isinstance(result_of_registration, int):
        if result_of_registration == 0:
            session['logged_in'] = True
            session["login"] = user.login
            return 0
        return 1
    return 1