# Clinic Application

This is a Django application that uses MySQL as its database. It is simply used as a demo.
- It has different levels of user, the admin/doctor, the assistant and patient
- The doctor and the assistant can both see info about the patient 
- Only the doctor can see privileged info 
- Only the doctor can create staff and patients
- Only the doctor can record an appointment (to do so, click the name of the patient)
- The patient can see their records at http://0.0.0.0:8000/patient-info/ with their id


## Running the Application

To run the application:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-github-username/clinic.git
```

2. Navigate to the project dir:
```bash 
cd clinic
```
3. Run the docker compose bundle

```bash 
docker compose up
```
The application should now be running at http://localhost:8000.


## Creating a Superuser
To login you need to create a superuser, you can use the following command:
```bash 
docker exec -it clinic-app python manage.py createsuperuser
```

Admin/staff panel: http://0.0.0.0:8000/
