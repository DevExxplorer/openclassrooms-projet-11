from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 5)

    @task
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "admin@irontemple.com"})

    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces", data={
            'competition': 'Spring Festival',
            'club': 'She Lifts',
            'places': 15
        })