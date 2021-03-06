# for get RvId list with PdbIds
from src.packages.getFasta.getFastaIteratorObjectFromMultifasta import \
    getFastaIteratorObjectFromMultifasta
from src.packages.getFastaHeader.getFastaHeaderFromFasta import \
    getFastaHeaderFromFasta
from src.packages.getFastaHeaderInfo.getFastaHeaderInfoFromFastaHeader import \
    getFastaHeaderInfoFromFastaHeader
from src.packages.getFastaHeaderInfoFilters.getIdEntryFastaWithPdbId import \
    fastaHeaderHavePdbIdEntry
import os
import shutil
#for get RvId list with PdbIds
mfastaPath = "/home/matias/Projects/2020/Revenant_DC/" \
             "data/2020-06-22/" \
             "multi-fasta/revenant_sequences.fasta"
rvIdWithPdbIdList = list()
rvFastaIterator = getFastaIteratorObjectFromMultifasta(mfastaPath=mfastaPath)
for rvFasta in rvFastaIterator:
    if fastaHeaderHavePdbIdEntry(fasta=rvFasta, headerSep="|",
                                 pdbIdEntryHeaderPos=1,
                                 pdbIdNoExistParam=""):
        rvFastaHeader = getFastaHeaderFromFasta(fasta=rvFasta)
        rvFastaHeaderRvId = getFastaHeaderInfoFromFastaHeader(fastaHeader=rvFastaHeader,
                                                              headerSep="|", headerPos=0)
        rvIdWithPdbIdList.append(rvFastaHeaderRvId)


# ¿What is the conformational diversity cluster of codnas that fall a pdbId of revenant blastPdb?
# Find each pdb(Ids in a file list in the file cluster list of codnas update
outFolderPath = "/home/matias/Projects/2020/Revenant_conformationalDiversity/" \
                "processed_data/2020-06-22/lists/" \
                "clustersCodnas"
codnasListFolderPath = "/home/matias/Projects/2020/codnasUpdate/" \
                       "processed_data/lists/" \
                       "2020-10-10/cd-hit"

for rvIdWithPdbId in rvIdWithPdbIdList:
    outRvIdFolderPath = outFolderPath + "/" + rvIdWithPdbId
    try:
        os.makedirs(outRvIdFolderPath)
    except FileExistsError:
        print("file exist")
    count = 1
    for count in range(len(rvIdWithPdbIdList)):
        codnasList = os.listdir(codnasListFolderPath)
        for clusterName in codnasList:
            pdbIdsByRvIdListFilePath = "/home/matias/Projects/2020/Revenant_conformationalDiversity/" \
                                       "processed_data/2020-06-22/" \
                                       "lists/blastpPdb/rvIdsWithPdbId/" \
                                       "%s.list" % rvIdWithPdbId
            codnasListFilePath = codnasListFolderPath + "/" + \
                                   "%s" % clusterName

            inFileObj1 = open(pdbIdsByRvIdListFilePath)
            inFileList1 = inFileObj1.readlines()
            pdbIdList = list()
            for pdbIdWithChainId in inFileList1:
                pdbIdWithChainId = pdbIdWithChainId.strip("\n").upper()
                # la linea de abajo no me daría bien los match con codnas por que se pierde info de la cadena?
                #pdbIdWithChainId = pdbIdWithChainId[0:4].lower() + pdbIdWithChainId.strip()[-2:]
                pdbIdList.append(pdbIdWithChainId)

            inFileObj2 = open(codnasListFilePath)
            inFileList2 = inFileObj2.readlines()
            codnasPdbIdList = list()
            for pdbIdWithChainId in inFileList2:
                pdbIdWithChainId = pdbIdWithChainId.strip("\n").upper()
                # la linea de abajo no me daría bien los match con codnas por que se pierde info de la cadena?
                #pdbIdWithChainId = pdbIdWithChainId[0:4].lower() + pdbIdWithChainId.strip()[-2:]
                codnasPdbIdList.append(pdbIdWithChainId)

            for pdbId in pdbIdList:
                if pdbId in codnasPdbIdList:
                    print(rvId, "True iteration:", count, "of", len(pdbIdList), "\n",
                          pdbId, "found in cluster with Cd:", clusterName, "\n",
                          codnasPdbIdList)
                    count += 1
                    shutil.copy(codnasListFilePath, outRvIdFolderPath)
        break

