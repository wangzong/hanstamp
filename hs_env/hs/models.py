from django.db import models

# Create your models here. 

# class Hanzi(models.Model):
#     """定义汉字类"""
#     zi = models.CharField(max_length=100)
#
#     # pagenum = models.integer
#
#     class Meta:
#         verbose_name_plural = 'Hanzis'
#
#     def __str__(self):
#         """返回汉字"""
#         return self.zi
class Wzz(models.Model):
    pagenum = models.IntegerField(blank=True, null=True)
    col = models.IntegerField(blank=True, null=True)
    character = models.TextField(blank=True, null=True)
    index_code = models.TextField(blank=True, null=True)
    drawnum = models.IntegerField(blank=True, null=True)
    simplified = models.TextField(blank=True, null=True)
    component = models.TextField(blank=True, null=True)
    stampnum_in_col = models.IntegerField(blank=True, null=True)
    stampcode1 = models.TextField(blank=True, null=True)
    stampcode2 = models.TextField(blank=True, null=True)
    stampcode3 = models.TextField(blank=True, null=True)
    stampcode4 = models.TextField(blank=True, null=True)
    stampcode5 = models.TextField(blank=True, null=True)
    stampcode6 = models.TextField(blank=True, null=True)
    stampcode7 = models.TextField(blank=True, null=True)
    stampcode8 = models.TextField(blank=True, null=True)
    stampcode9 = models.TextField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'wzz'

    def __str__(self):
        # a = ''
        s = str(self.pagenum) +" - " + str(self.col)+" - " + self.character +" - " + str(self.drawnum)
        return (s)




