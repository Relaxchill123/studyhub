from dataclasses import dataclass, field

@dataclass
class Task:
    _id: int
    _title: str
    _priority: int
    _is_done: bool = False
    _tags: list[str] = field(
        default_factory=list,
    )

    def __post_init__(self):
        self.title = self.title.strip()

        if not self.title:
            raise ValueError("Название не может быть пустым")

        if not 1 <= self.priority <= 5:
            raise ValueError("Приоритет должен быть от 1 до 5")

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Название не может быть пустым")
        self._title = cleaned

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        # if not isinstance(value, int):
        #     raise ValueError("Приоритет должен быть int")

        if not 1 <= value <= 5:
            raise ValueError("Приоритет должен быть от 1 до 5")

        self._priority = value

    @property
    def is_done(self):
        return self._is_done

    @property
    def tags(self):
        return self._tags

    def task_to_dict(self):
        return {
            'id': self._id,
            'title': self._title,
            'priority': self._priority,
            'is_done': self._is_done,
            'tags': self._tags,
        }

    def mark_done(self):
        self._is_done = True

    def is_high_priority(self):
        return self._priority >= 4

    def __str__(self):
        mark = "x" if self._is_done else " "
        tags = f"Тэги: {', '.join(self._tags)}" if self._tags else ''
        return f"[{mark}] {self._id}. {self._title} {tags}" # добавить отображение для пользователя