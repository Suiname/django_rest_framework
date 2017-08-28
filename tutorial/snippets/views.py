# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from snippets.models import Snippet, Feeding, Discharge
from snippets.serializers import SnippetSerializer, UserSerializer, FeedingSerializer, DischargeSerializer
from rest_framework import generics, permissions, renderers, viewsets
from django.contrib.auth.models import User
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.views import generic
from django.views.generic.edit import CreateView
from itertools import chain
from operator import attrgetter

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'snippets/index.html'
    context_object_name = 'tracker_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        result_list = sorted(
            chain(Discharge.objects.all(), Feeding.objects.all()),
            key=attrgetter('created'))
        return result_list[-5:]

class FeedingFormView(CreateView):
    template_name = 'snippets/feeding.html'
    success_url = '/'
    model = Feeding
    fields = ['created', 'left', 'right', 'pumped', 'formula']

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FeedingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Feeding.objects.all()
    serializer_class = FeedingSerializer

class DischargeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Discharge.objects.all()
    serializer_class = DischargeSerializer