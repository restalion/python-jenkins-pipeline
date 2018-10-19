from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):
    def on_start(self):
        print("Start performance test")

    @task(10)
    def index(self):
        self.client.get("/auth/hello")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 50
    max_wait = 150
