# encoding: utf-8
from python_elasticsearch.coreFunction.coreDatabase import CoreDatabase
from python_elasticsearch.functions.exportToExcel import exportToExcel as ExportToExcel

clsCoreDatabase = CoreDatabase()
clsExportToExcel = ExportToExcel()
listDoc = list()
page = 0

while True:
  resp = clsCoreDatabase.getAllDocument(page, index="project", type="news")
  if resp["res"]==True:
    listDoc = listDoc + resp["data"]
    page += 1
  else: break

clsExportToExcel.exportToExcel(listDoc)