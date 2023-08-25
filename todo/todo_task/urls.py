from django.urls import path
from .views import *

urlpatterns = [
    path("api/addTask", addTask),
    path("api/getTask", getAllTask),
    path("api/getActiveTask", getAllActiveTask),
    path("api/getCompleteTask", getAllcompleteTask),
    path("api/updateTaskStatusById/", updateTaskStatusById),
    path("api/taskReminder", task_reminder),
    path("api/taskrescheduler/", taskreschedulerById),
    path("api/updateTaskById/<int:id>", updateTaskById),
    path("api/deleteTaskById/<int:id>", deleteTaskById),
    path("api/searchByTitle/<str:title>", searchByTitle),
    path("api/searchByDuedate", searchByDueDate),
    path("api/searchByUpdatedate", searchByUpdatedDate),
    path("api/searchByCreatedate", searchByCreatedDate),
    
]

