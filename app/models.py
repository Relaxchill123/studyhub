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
            raise ValueError("Некоректное название. Название не может быть пустым", self.id)

        if not 1 <= self.priority <= 5:
            raise ValueError("Некоректный приоритет. Приоритет должен быть от 1 до 5", self.id)

    def mark_done(self):
        self.is_done = True

    def add_tag_to_task(self, tag):
        self.tags.append(tag)

    def task_to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'priority': self.priority,
            'is_done': self.is_done,
            'tags': list(self.tags),
        }

    @classmethod
    def task_from_dict(cls, task):
        return cls(
            id=task['id'],
            title=task['title'],
            priority=task['priority'],
            is_done=task['is_done'],
            tags=list(task['tags'])
        )

    def is_high_priority(self):
        return self.priority >= 4

    def __str__(self):
        mark = "x" if self.is_done else " "
        tags = f"| Тэги: {', '.join(self.tags)}" if self.tags else ''
        return f"[{mark}] {self.id}. {self.title} {tags}" 