from abc import ABC, abstractmethod


class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return dict(self.__dict__.items())


class Reporter(BaseEntity):
    def __init__(self, id, name, email, team):
        self.id = id
        self.name = name
        self.email = email
        self.team = team

    def validate(self):
        if not self.name:
            raise ValueError('Name cannot be empty')
        if '@' not in self.email:
            raise ValueError('Invalid email')


class Issue(BaseEntity):
    STATUSES = ['open', 'in_progress', 'resolved', 'closed']
    PRIORITIES = ['low', 'medium', 'high', 'critical']

    def __init__(self, id, title, description, status, priority, reporter_id):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = reporter_id

    def validate(self):
        if not self.title:
            raise ValueError('Title cannot be empty')
        if self.status not in self.STATUSES:
            raise ValueError('Invalid status')
        if self.priority not in self.PRIORITIES:
            raise ValueError('Invalid priority')

    def describe(self):
        return f"{self.title} [{self.priority}]"


class CriticalIssue(Issue):
    def describe(self):
        return f"[URGENT] {self.title} — needs immediate attention"


class LowPriorityIssue(Issue):
    def describe(self):
        return f"{self.title} — low priority, handle when free"