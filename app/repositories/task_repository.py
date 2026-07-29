tasks = []


def get_all():
    return tasks


def get_by_id(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def create(task: dict):
    tasks.append(task)
    return task


def update(task_id: int, data: dict):
    task = get_by_id(task_id)

    if task is None:
        return None

    task["title"] = data["title"]
    task["description"] = data["description"]

    return task


def delete(task_id: int):
    task = get_by_id(task_id)

    if task is None:
        return False

    tasks.remove(task)
    return True