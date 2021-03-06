# %%
# for get RvId list with PdbIds
import sys
sys.path.append("/home/matias/Projects/2020/Revenant_conformationalDiversity")
from src.packages.getFasta.getFastaIteratorObjectFromMultifasta import \
    getFastaIteratorObjectFromMultifasta
from src.packages.getFastaHeader.getFastaHeaderFromFasta import \
    getFastaHeaderFromFasta
from src.packages.getFastaHeaderInfo.getFastaHeaderInfoFromFastaHeader import \
    getFastaHeaderInfoFromFastaHeader
from src.packages.getFastaHeaderInfoFilters.getIdEntryFastaWithPdbId import \
    fastaHeaderHavePdbIdEntry
# for get pdbId list from Tsv BlastpPdb table
from src.packages.getId.getPdbIdListFromBlastPdbTable import getPdbIdWithChainIdListFromBlastTsvTableOfBlastpSoft
from src.packages.getId.getPdbIdListFromRevenantCsv import getPdbIdWithChainIdListFromRvChainCsv
import os
#for get RvId list with PdbIds
mfastaPath = "/home/matias/Projects/2020/Revenant_homologuesStructures/" \
             "data/2020-06-22/multi-fasta/" \
             "revenant_sequences.fasta"
# %%
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

print(rvIdWithPdbIdList)
# %%
# for get pdbId list from Tsv BlastpPdb table
# path para filtrar las pdb ancestrales
rvChainCsvPath = "/home/matias/Projects/2020/Revenant_homologuesStructures/" \
                 "data/2020-06-22/tables/" \
                 "revenantDbChain.csv"
# %%
for rvIdWithPdbId in rvIdWithPdbIdList:
    # path infile
    blastpPdbTsvPath = "/home/matias/Projects/2020/Revenant_homologuesStructures/" \
                       "outputs/2020-06-22/tables/" \
                       "blastpPdb/rvIdsWithPdbIds/" \
                       "%s.tsv" % rvIdWithPdbId
    # path outfile
    outFolder = "/home/matias/Projects/2020/Revenant_homologuesStructures/" \
                "processed_data/2020-06-22/lists/" \
                "blastpPdb/rvIdsWithPdbId/"
    outFile = "/home/matias/Projects/2020/Revenant_homologuesStructures/" \
                "processed_data/2020-06-22/lists/" \
                "blastpPdb/rvIdsWithPdbId/" \
                "%s.list" % rvIdWithPdbId

    # %%
    try:
        os.makedirs(outFolder)
    except FileExistsError:
        ("folder exist")
    
    # %%    
    # para sacar las ancestrales 
    rvPdbIdWithChainIdList = getPdbIdWithChainIdListFromRvChainCsv(rvChainCsvPath=rvChainCsvPath,
                                                                   pdbIdColumn="pdb_id",
                                                                   chainIdColumn="chain_id",
                                                                   columnJoin="_")
    blastpPdbIdWithChainIdList = getPdbIdWithChainIdListFromBlastTsvTableOfBlastpSoft(blastpPdbTsvPath)
    # blastpPdbIdWithChainIdList = 

    # %% 
    with open(outFile, "w") as f:
        for blastpPdbIdWithChainId in blastpPdbIdWithChainIdList:
            #saco las ancestrales filtrando por las pdbId que no estan en lista de pdbIds de revenant
            if blastpPdbIdWithChainId not in rvPdbIdWithChainIdList:
                f.write("%s," % blastpPdbIdWithChainId)
