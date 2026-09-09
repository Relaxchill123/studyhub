from dataclasses import dataclass, field

@dataclass
class Task:
    id: int
    title: str
    priority: int
    is_done: bool = False
    tags: list[str] = field(
        default_factory=list,
    )

    def __post_init__(self):
        self.title = self.title.strip()

        if not self.title:
            raise ValueError("Название не может быть пустым")

        if not 1 <= self.priority <= 5:
            raise ValueError("Приоритет должен быть от 1 до 5")


    # @property
    # def id(self):
    #     return self._id

    # @property
    # def title(self):
    #     return self._title

    # @title.setter
    # def title(self, value):
    #     cleaned = value.strip()
    #     if not cleaned:
    #         raise ValueError("Название не может быть пустым")
    #     self._title = cleaned

    # @property
    # def priority(self):
    #     return self._priority

    # @priority.setter
    # def priority(self, value):
    #     try:
    #         self._priority = int(value)
    #     except ValueError as e:
    #         raise ValueError("Приоритет должен быть целым числом")

    #     if not 1 <= self._priority <= 5:
    #         raise ValueError("Приоритет должен быть от 1 до 5")

    #     self._priority = value

    # @property
    # def is_done(self):
    #     return self._is_done

    # @property
    # def tags(self):
    #     return self._tags

    def task_to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'priority': self.priority,
            'is_done': self.is_done,
            'tags': self.tags,
        }

    def task_from_dict(self, task):
        return Task(
            task['id'],
            task['title'],
            task['priority'],
            task['is_done'],
            task['tags']
        )

    def mark_done(self):
        self.is_done = True

    def is_high_priority(self):
        return self.priority >= 4

    def __str__(self):
        mark = "x" if self.is_done else " "
        tags = f"| Тэги: {', '.join(self.tags)}" if self.tags else ''
        return f"[{mark}] {self.id}. {self.title} {tags}" 