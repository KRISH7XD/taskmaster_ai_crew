import time

class FeedbackLoop:
    def __init__(self):
        self.task_times = {}
        self.task_success = {}

    def start_task(self, task_id):
        self.task_times[task_id] = time.time()

    def end_task(self, task_id, success=True):
        duration = time.time() - self.task_times[task_id]
        self.task_success[task_id] = {"duration": duration, "success": success}
        return duration

    def get_performance(self, task_id):
        return self.task_success.get(task_id, {"duration": None, "success": False})

feedback = FeedbackLoop()