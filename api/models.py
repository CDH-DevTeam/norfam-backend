# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Term(models.Model):
    term_id = models.AutoField(primary_key=True)
    term_term = models.CharField(unique=True, max_length=100)
    term_stem = models.CharField(max_length=100, blank=True, null=True)
    term_df = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'term'

class DocTerm(models.Model):
    doc_term_id = models.AutoField(primary_key=True)
    doc_id = models.ForeignKey('Document', on_delete=models.PROTECT, db_column='doc_id', related_name='doc_terms')
    term = models.ForeignKey('Term', on_delete=models.PROTECT, db_column='term_id')
    tf = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doc_term'

class Document(models.Model):
    doc_id = models.AutoField(primary_key=True)
    doc_keyword = models.CharField(max_length=100)
    doc_text = models.TextField()
    doc_abstr = models.CharField(max_length=2048)
    doc_suppl = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'document'

class Termsim(models.Model):
    termsim_id = models.AutoField(primary_key=True)
    target = models.ForeignKey('Term', on_delete=models.PROTECT, db_column='term1_id', related_name='neighbors')
    term = models.ForeignKey('Term', on_delete=models.PROTECT, db_column='term2_id')
    similarity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'termsim'

class Entity(models.Model):
    ent_id = models.AutoField(primary_key=True)
    doc_id = models.IntegerField(blank=True, null=True)
    ent_type = models.TextField()
    ent_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'entity'
