from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from .models import Projects, CustomUsers, Issues, Comments, Contributors
from .serializers import (ProjectSerializer,
                          CustomUserSerializer,
                          IssueSerializer,
                          CommentSerializer,
                          ContributorSerializer,
                          ProjectWithIdSerializer)

from .permissions import (HasProjectPermission,
                          HasContributorPermission,
                          HasHomePermission,
                          HasIssuePermission,
                          HasCommentPermission)

from django.shortcuts import get_object_or_404




class UserRegistrationView(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CustomUsers.objects.all()
    serializer_class = CustomUserSerializer

    '''creates a new user'''
    def create(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create_user(email=request.data['email'],
                                   last_name=request.data['last_name'],
                                   password=request.data['password'],
                                   first_name=request.data['first_name'])
            userEmail = serializer.data.get('email')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# /projects/
class HomeView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Projects.objects.all()
    serializer_class = ProjectWithIdSerializer
    serializer_create = ProjectSerializer
    '''
    gets list of Projects where the connected user is involved
    '''
    def list(self, request, *args, **kwargs):
        qs = Projects.objects.filter(contributors__user=request.user)
        serializer = ProjectWithIdSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # from post method, creates a new project
    def create(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(author_user=request.user)
            contributor = Contributors.objects.create(project=project, user=request.user, role='Author')
            contributor.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /projects/{id}/
class ProjectsView (ModelViewSet):
    model = Projects
    permission_classes = [IsAuthenticated, HasProjectPermission]
    serializer_class = ProjectWithIdSerializer
    lookup_field = 'project_id'
    queryset = Projects.objects.all()


    def retrieve(self, request, *args, **kwargs):
        instance = Projects.objects.get(id=kwargs['project_id'])
        if Projects.objects.get(id=kwargs['project_id']):
            raw = Projects.objects.get(id=kwargs['project_id'])
            project = ProjectWithIdSerializer(raw, many=False)
            return Response(project.data, status=status.HTTP_200_OK)

    '''
    update project via its id follows a put method
    '''
    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Projects, id=kwargs['project_id'])
        self.check_object_permissions(self.request, obj)
        instance = Projects.objects.get(id=kwargs['project_id'])
        serializer = ProjectWithIdSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    '''
    deletes project via its id thanks to delete method
    '''
    def destroy(self, request, *args, **kwargs):
        obj = get_object_or_404(Projects, id=kwargs['project_id'])
        self.check_object_permissions(self.request, obj)
        instance = kwargs['project_id']
        waste = Projects.objects.filter(id=instance)
        self.perform_destroy(waste)
        message = 'You deleted the project' + str(instance)
        return Response({'message': message}, status=status.HTTP_202_ACCEPTED)
        # delete le project, et en cascade ca va delete les issues liéés, les contributors, les comments


# /project/id/users/ et /projects/id/users/id
class ContributorsView (ModelViewSet):
    permission_classes = [IsAuthenticated, HasContributorPermission]
    queryset = Contributors.objects.all()
    serializer_class = ContributorSerializer

    '''gets the list of contributors for a specific project id'''
    def list(self, request, *args, **kwargs):
        #  project_instance = Projects.objects.get(id=kwargs['project_id'])
        instances = Contributors.objects.filter(project=kwargs['project_id'])
        serializer = ContributorSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    '''creates a new contributor object '''
    def create(self, request, *args, **kwargs):
        serializer = ContributorSerializer(data=request.data)
        instance_project = Projects.objects.get(id=kwargs['project_id'])
        perso = CustomUsers.objects.get(id=request.data['user'])
        '''Vérifie que le user qui fait la request est l'author du project'''
        if serializer.is_valid():
            serializer.save(project=instance_project, user=perso, role='Contributor')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)




class ContributorsDeletionView(ModelViewSet):
    permission_classes = [IsAuthenticated, HasContributorPermission]
    queryset = Contributors.objects.all()
    serializer_class = ContributorSerializer
    '''deletes a contributor object related to a specific project'''
    def destroy(self, request, *args, **kwargs):
        project_instance = Projects.objects.get(id=kwargs['project_id'])
        user_instance = CustomUsers.objects.get(id=kwargs['user_id'])
        obj = Contributors.objects.filter(project=project_instance).filter(user=user_instance)
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)
        message ='The contributor was successfully deleted '
        return Response({'message':message}, status=status.HTTP_202_ACCEPTED)


# /projects/id/issues/ and /projects/id/issues/id
class IssuesView(ModelViewSet):
    permission_classes = [IsAuthenticated, HasIssuePermission]
    serializer_class = IssueSerializer
    queryset = Issues.objects.all()

    '''list of issues in a specific project, get method'''
    def list(self, request, *args, **kwargs):
        instance = Projects.objects.get(id=kwargs['project_id'])
        qs = []
        for elem in Issues.objects.all():
            if elem.project == instance:
                qs.append(elem)
        serializer = IssueSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    '''creates an issue in a specific project, post method'''
    def create(self, request, *args, **kwargs):
        project = Projects.objects.get(id=kwargs['project_id'])
        serializer = IssueSerializer(data=request.data)
        assignee = CustomUsers.objects.get(id=request.data['assignee_user'])
        if Contributors.objects.filter(user=assignee).filter(project=project).exists():
            if serializer.is_valid():
                serializer.save(author_user=request.user, project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            message = 'The assignee user is not yet a contributor to this project'
            return Response({'message': message}, status=status.HTTP_200_OK)


    '''updates a specific issue, put method'''
    def update(self, request, *args, **kwargs):
        obj = Issues.objects.get(id=kwargs['issue_id'])
        self.check_object_permissions(request, obj)
        project = Projects.objects.get(id=kwargs['project_id'])
        serializer = IssueSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)



    '''deletes an issue from specific project, delete method'''
    def destroy(self, request, *args, **kwargs):
        if Issues.objects.filter(id=kwargs['issue_id']).exists():
            obj = Issues.objects.get(id=kwargs['issue_id'])
            self.check_object_permissions(request, obj)
            self.perform_destroy(obj)
            message = 'The issue was successfully deleted'
            return Response({'message': message}, status=status.HTTP_204_NO_CONTENT)
        else:
            message = 'This issue doesnt exists'
            return Response({'message': message}, status=status.HTTP_204_NO_CONTENT)


# /projects/id/issues/id/comments/ and /projects/id/issues/id/comments/id/
class CommentsView(ModelViewSet):
    permission_classes = [IsAuthenticated, HasCommentPermission]
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()

    '''get list of comments linked to a specific issue'''
    def list(self, request, *args, **kwargs):
        instance = Issues.objects.get(id=kwargs['issue_id'])
        qs = []
        for elem in Comments.objects.all():
            if elem.issue == instance:
                qs.append(elem)
        serializer = CommentSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    '''creates a new comment on a specific issue'''
    def create(self, request, *args, **kwargs):
        issue_obj = Issues.objects.get(id=kwargs['issue_id'])
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(issue=issue_obj, author_user_id=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SoloCommentView(ModelViewSet):
    permission_classes = [IsAuthenticated, HasCommentPermission]
    serializer_class = CommentSerializer
    queryset = Comments.objects.all()

    """allows to retrieve ONE comment object"""
    def retrieve(self, request, *args, **kwargs):
        if Comments.objects.get(id=kwargs['comment_id']):
            comm = Comments.objects.get(id=kwargs['comment_id'])
            serializer = CommentSerializer(comm, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

    '''Updates comment via its id'''
    def update(self, request, *args, **kwargs):
        obj = Comments.objects.get(id=kwargs['comment_id'])
        self.check_object_permissions(request, obj)
        serializer = CommentSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    """deletes comments via its id"""
    def destroy(self, request, *args, **kwargs):
        instance = kwargs['comment_id']
        obj = Comments.objects.get(id=instance)
        self.check_object_permissions(request, obj)
        self.perform_destroy(obj)
        message = 'The comment was successfully deleted'
        return Response({'message': message}, status=status.HTTP_200_OK)
