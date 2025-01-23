class Youtuber:
    def __init__(self, name, group_id, pl_id=None):
        self.name = name  # имя ютубера после @
        self.group_id = group_id  # ID группы ВК
        self.pl_id = pl_id  # номер плейлиста в группе ВК

    def __str__(self):
        return self.name

# Пример правильного определения youtubers_list, без ограничений количества
youtubers_list = [
    Youtuber(name="NULL", group_id="NULL", pl_id=NULL),
    Youtuber(name="NULL", group_id="NULL", pl_id=NULL)
]
