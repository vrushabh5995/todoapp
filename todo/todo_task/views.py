from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse, response
from rest_framework.parsers import JSONParser
from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import pandas as pd
from django.db import connection
from datetime import date,datetime




@csrf_exempt
@api_view(["POST"]) 
def addTask(request):
    if request.method == 'POST':
        serializer =  TaskSerializer(data=request.data)
        if serializer.is_valid():
            task_title=request.data["task_title"].lower()
            serializer.save(task_title=task_title)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(["PUT"]) 
def updateTaskStatusById(request):
    task_id=request.query_params.get("id")
    cursor = connection.cursor()
    sql = "select * from todo_task_task where task_id=%s"
    df = pd.read_sql(sql, connection, params=[task_id])
    if df.empty == False:
        sql1 = "update todo_task_task set task_status=%s  where task_id=%s"
        cursor.execute(sql1, [request.data["task_status"],task_id])
        return JsonResponse({"msg":"Task status updated successfully."})
    else:
        return JsonResponse({"msg":"Task Not Found."})


@csrf_exempt
@api_view(["PUT"]) 
def taskreschedulerById(request):
    task_id=request.query_params.get("id")
    cursor = connection.cursor()
    sql = "select * from todo_task_task where task_id=%s"
    df = pd.read_sql(sql, connection, params=[task_id])
    if df.empty == False:
        sql1 = "update todo_task_task set task_due_date=%s  where task_id=%s"
        cursor.execute(sql1, [request.data["task_due_date"],task_id])
        return JsonResponse({"msg":"Task status updated successfully."})
    else:
        return JsonResponse({"msg":"Task Not Found."})
    

@csrf_exempt
@api_view(["GET"])
def task_reminder(request):
    
    sql="select * from todo_task_task where task_due_date=%s and task_status= 0 "
    df=pd.read_sql(sql,connection, params=[str(date.today())])
    if df.empty == False:
        return Response(df.to_dict("records"))
    else:
        return JsonResponse({"msg":"Task Not Found."})
    
@csrf_exempt
@api_view(['GET']) 
def getAllTask(request):
    taskData =  Task.objects.all()
    if taskData is not None:
        serializer =  TaskSerializer(taskData, many=True)
        return JsonResponse(serializer.data, safe= False)
    return JsonResponse({"msg":"Task does Not Found."})



@csrf_exempt
@api_view(['GET']) 
def getAllActiveTask(request):
    data1 =  Task.objects.filter(task_status='True').values()
    serializer =  TaskSerializer(data1, many=True)
    return JsonResponse(serializer.data, safe= False)

@csrf_exempt
@api_view(['GET']) 
def getAllcompleteTask(request):
    data1 =  Task.objects.filter(task_status='False').values()
    serializer =  TaskSerializer(data1, many=True)
    return JsonResponse(serializer.data, safe= False)


@csrf_exempt
@api_view(['GET']) 
def searchByTitle(request, title):
    title = title.lower()
    matching_task = Task.objects.filter(task_title__icontains=title)
    if matching_task is not None:
        serializer = TaskSerializer(matching_task, many=True)
        return Response(serializer.data)
    else:
        return JsonResponse({"msg":"Task Not Found."})



@csrf_exempt
@api_view(["GET"])
def searchByDueDate(request):
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    sql="select * from todo_task_task where task_due_date between %s and %s"
    df=pd.read_sql(sql,connection, params=[start_date,end_date])
    if df.empty == False:
        return Response(df.to_dict("records"))
    else:
        return JsonResponse({"msg":"Task Not Found."})

@csrf_exempt
@api_view(["GET"])
def searchByUpdatedDate(request):

    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    sql="select * from todo_task_task where DATE(updated_at) between %s and %s"
    df=pd.read_sql(sql,connection, params=[start_date,end_date])
    print(df)
    if df.empty == False: 
        return Response(df.to_dict("records"))
    else:
        return JsonResponse({"msg":"Task Not Found."})
    
@csrf_exempt
@api_view(["GET"])
def searchByCreatedDate(request):

    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    sql="select * from todo_task_task where DATE(task_created_date) between %s and %s"
    df=pd.read_sql(sql,connection, params=[start_date,end_date])
    print(df)
    if df.empty == False: 
        return Response(df.to_dict("records"))
    else:
        return JsonResponse({"msg":"Task Not Found."})


@csrf_exempt
@api_view(["PUT"]) 
def updateTaskById(request, id):
    task = Task.objects.get(task_id=id)
    serializer = TaskSerializer(task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@csrf_exempt
@api_view(["DELETE"]) 
def deleteTaskById(request, id):
    task = Task.objects.get(task_id=id)
    if task is not None:
        task.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(["DELETE"]) 
def deleteAllTask(request):
    cursor = connection.cursor()
    sql = "delete from  todo_task_task"
    cursor.execute(sql)
    return JsonResponse({"msg":"Tasks deleted successfully."})
    

