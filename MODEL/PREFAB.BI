''
' bu1ld0r - MODEL/PREFAB.BI
' =============================================================================
' Prefabs: models saved in prefabs/ (in folders if you like) that another
' model uses whole - a "use NAME ..." line, placed, turned and scaled like
' a part. A use stays linked: its parts come from prefabs/NAME.bld, so
' changing the prefab changes every model that uses it. The library (every
' prefab's parts) is read in at start-up and after a prefab is saved, into
' the part arrays after the model's own.
'
CONST MAX_PF = 500

DIM SHARED pfN, pfTop AS LONG ' (prefabs, and the parts they take: PF_BASE + 1 to PF_BASE + pfTop)
DIM SHARED pfName$(MAX_PF), pfFirst(MAX_PF) AS LONG, pfCnt(MAX_PF) AS LONG
DIM SHARED pfIcon&(MAX_PF) ' (its picture for the bin: 0 until it's wanted)
