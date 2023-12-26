BOT_TOKEN = "6437988250:AAGJRvRVjLseX9WSOTcwxAISyI7fYCMamI8"
id_admin = 6044110141
email_address = "dramaturg2021igor@yandex.ru"
email_password = "Vfnhtif1"
host = "smtp.yandex.com" # если yandex
# host = "smtp.mail.ru" # если mail и так далее
BASE_PROVIDERS = []
for i in open("providers", "r"):
    if i == "\n":
        continue
    else:
        BASE_PROVIDERS.append(i.replace("\n", ""))
