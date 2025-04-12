#  Shantanu Raut - DataX.ai

This project brings together a real-world backend solution using Django and Django REST Framework, along with a handy Python CLI tool. It covers everything from building and securing APIs to handling files and processing images—all in one place!

- **Project & Task Management API**
- **User Activity Logging System**
- **Command-Line Image Processor** for URLs and CSVs


## 1. Project & Task Management API

### API Endpoints

GET    /projects/                      → List projects
POST   /projects/                      → Create new project
PATCH  /projects/<id>/                → Update a project
POST   /projects/<id>/upload_image/   → Upload project image
GET    /projects/<id>/download_csv/   → Export project to CSV
POST   /projects/bulk_delete/         → Soft-delete multiple projects

GET    /projects/<id>/tasks/          → List tasks for a project
POST   /projects/<id>/tasks/          → Create task under a project
PUT    /projects/<pid>/tasks/<tid>/   → Update task
DELETE /projects/<pid>/tasks/<tid>/   → Delete task


## 2. User Activity Logging

Every important action in the project—like creating a new project—is automatically logged with a timestamp in the UserActivity model. You can easily expand this to keep track of things like user logins, updates or deletions, and any actions performed by logged-in users.


##  3. Image Downloader & Processor (CLI Tool)

python3 main.py "(URL)"
python3 main.py machine.csv
