from locust import HttpUser, TaskSet, task, between
import random


class MyTaskSet(TaskSet):
    @task
    def my_task(self):
        phone_number = "09" + "".join(str(random.randint(0, 9)) for _ in range(8))

        payload = {"code": "test_code", "phone": phone_number}
        headers = {"Content-Type": "application/json", "accept": "application/json"}

        response = self.client.post(
            "/charge-code/submit/", json=payload, headers=headers
        )

        print(response.status_code)


class MyUser(HttpUser):
    tasks = [MyTaskSet]
    wait_time = between(1, 3)  # Define a random wait time between requests
