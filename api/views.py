import re
import timeit
from rest_framework import viewsets
from .serializers import TermSerializer, DocumentSerializer, DocTermSerializer, NeighborhoodSerializer, EntitySerializer, QuerySerializer
from .models import Term, Document, DocTerm, Termsim, Entity
from django.db.models import Prefetch
from math import log2
from functools import cmp_to_key

def sort_tfidf(docA, docB):
    totA = 0.0
    totB = 0.0
    tfA = 1
    tfB = 1
    for doc_term in docA.doc_terms.all():
        tfA = log2(doc_term.tf + 1)
        idfA = log2(100_000) - log2(doc_term.term.term_df)
        totA += tfA * idfA
    for doc_term in docB.doc_terms.all():
        tfB = log2(doc_term.tf + 1)
        idfB = log2(100_000) - log2(doc_term.term.term_df)
        totB += tfB * idfB   
    if totA > totB:
        return -1
    elif totA < totB:
        return 1
    else:
        return 0


class TermViewSet(viewsets.ModelViewSet):
    serializer_class = TermSerializer
    queryset = Term.objects.all()
    lookup_field = 'term_term'

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    lookup_field = 'doc_id'
    def get_queryset(self):
        version = "1"
        if "v" in self.request.GET:
            version = self.request.GET["v"]
        database = "nor_fam_2" if version == "2" else "nor_fam_1"
        queryset = Document.objects.all().using(database)
        print(queryset.query)
        return queryset

class TermsimViewSet(viewsets.ModelViewSet):
    serializer_class = NeighborhoodSerializer
    def get_queryset(self):
        version = "1"
        if "v" in self.request.GET:
            version = self.request.GET["v"]
        database = "nor_fam_2" if version == "2" else "nor_fam_1"
        q = [str(term).lower() for term in re.split(r"\s+", self.request.GET["q"])]
        queryset = Term.objects.distinct().prefetch_related(
            Prefetch('neighbors', queryset=Termsim.objects.order_by('-similarity'))
        ).select_related().filter(neighbors__target__term_term__in=q).all().using(database)
        return queryset


class EntityViewSet(viewsets.ModelViewSet):
    serializer_class = EntitySerializer
    def get_queryset(self):
        version = "1"
        if "v" in self.request.GET:
            version = self.request.GET["v"]
        database = "nor_fam_2" if version == "2" else "nor_fam_1"
        q = int(self.request.GET["q"])
        queryset = Entity.objects.distinct().select_related().filter(doc_id=q).all().using(database)
        return queryset

class QueryViewSet(viewsets.ModelViewSet):
    serializer_class = QuerySerializer
    def get_queryset(self):
        version = 1
        search_mode = "w"
        if "v" in self.request.GET:
            version = self.request.GET["v"]
        if "m" in self.request.GET:
            search_mode = self.request.GET["m"]
        database = "nor_fam_2" if version == "2" else "nor_fam_1"
        q = [str(term).lower() for term in re.split(r"\s+", self.request.GET["q"])]
        if search_mode == "t":
            tic = timeit.default_timer()
            queryset = Document.objects.distinct().prefetch_related(
                Prefetch('doc_terms', queryset = DocTerm.objects.filter(term__term_term__in=q))
            ).select_related().filter(doc_terms__term__term_term__in=q).all().using(database)
            print(queryset.query)
            toc = timeit.default_timer()
            print(toc-tic)
            return sorted(queryset, key=cmp_to_key(sort_tfidf))
        else:
            queryset = Document.objects.distinct().prefetch_related(
                Prefetch('doc_terms', queryset = DocTerm.objects.filter(term__term_term__in=q))
            ).filter(doc_keyword__in=q).all().using(database).order_by('doc_keyword', 'doc_suppl')
            print(queryset.query)
            return queryset
