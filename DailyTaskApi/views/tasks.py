"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from DailyTaskApi.models import Task, TaskUser
from rest_framework.decorators import action
from datetime import date


class Tasks(ViewSet):
    """Tasks"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Task instance
        """

        # Uses the token passed in the `Authorization` header
        user = TaskUser.objects.get(user=request.auth.user)

        # Create a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.
        task = Task()
        task.user = user
        task.title = request.data["title"]
        task.task_date = date.today()
        task.content = request.data["content"]
        task.complete = False

        # Try to save the new Post to the database, then
        # serialize the Post instance as JSON, and send the
        # JSON as a response to the client request
        try:
            task.save()
            serializer = TaskSerializer(task, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Post
        Returns:
            Response -- JSON serialized Post instance
        """


        


        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/Posts/2
            #
            # The `2` at the end of the route becomes `pk`
            task = Task.objects.get(pk=pk)

            user = TaskUser.objects.get(user=request.auth.user)

        
            serializer = TaskSerializer(post, context={'request': request})
            
            single_post={}
            single_post['post']=serializer.data
            if user == task.user:
                single_post['myPosts']=True 

            return Response(single_post)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def patch(self, request, pk=None):
        """Handle PATCH requests for a Post
        Returns:
            Response -- Empty body with 204 status code
        """
        task = Task.objects.get(pk=pk)
        task.approved = request.data['complete']
        task.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        """Handle PUT requests for a Post
        Returns:
            Response -- Empty body with 204 status code
        """
        user = TaskUser.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Post, get the Post record
        # from the database whose primary key is `pk`
        task = Task.objects.get(pk=pk)
        task.user = user
        task.title = request.data["title"]
        task.task_date = request.data["taskDate"]
        task.content = request.data["content"]
        task.complete = request.data["complete"]


        task.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Post
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            task = Task.objects.get(pk=pk)
            task.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Task.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to Posts resource
        Returns:
            Response -- JSON serialized list of Posts
        """
        # Get all Post records from the database
        tasks = Task.objects.all()
        #geting the current user
        user = TaskUser.objects.get(user=request.auth.user)
        #filter all the tasks by the signed in user
        myTasks=tasks.filter(user=user)
            

            

        serializer = TaskSerializer(
            myTasks, many=True, context={'request': request})

        return Response(serializer.data)
class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users
    Arguments:
        serializer type
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')
class TaskUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUsers
    Arguments:
        serializer type
    """
    user = UserSerializer(many=False)

    class Meta:
        model = TaskUser
        fields = ('id', 'user')
        depth = 1
class TaskSerializer(serializers.ModelSerializer):
    user = TaskUserSerializer(many=False)
    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'task_date', 'content', 'complete')
        depth = 1
