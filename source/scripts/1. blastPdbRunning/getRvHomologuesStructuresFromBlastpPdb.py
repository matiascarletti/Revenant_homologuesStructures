# %% 
import os
import sys
import glob
sys.path.append("/home/matias/Projects/2020/Revenant_conformationalDiversity")
import Bio
from Bio import SeqIO
from src.packages.getFasta.getFastaIteratorObjectFromMultifasta import \
    getFastaIteratorObjectFromMultifasta
from src.packages.getFastaHeaderInfoFilters.getIdEntryFastaWithPdbId import \
    fastaHeaderHavePdbIdEntry
from src.packages.getFastaHeader.getFastaHeaderFromFasta import \
    getFastaHeaderFromFasta
from src.packages.getFastaHeaderInfo.getFastaHeaderInfoFromFastaHeader import \
    getFastaHeaderInfoFromFastaHeader
from src.packages.getIoFilePath.getOutFilePath import \
    getTouchOutFilePath
from src.packages.runBlast.runBlastp import \
    runBlastpDefectTsvFormat
from src.packages.getIoFilePathList.getFilePathList import \
    getFilePathListFromDirectoryPath

# %%
rvFastasWithPdbIdInFolder = "/home/matias/Projects/2020/Revenant_homologuesStructures/" \
                            "processed_data/2020-06-22/fastas/" \
                            "rvIdsWithPdbIds/"
blastpPdbDbPath          = "/home/matias/blastDbs/pdbaa/pdbaa"
blastpPdbOutFolder      = "/home/matias/Projects/2020/Revenant_homologuesStructures/" \
                        "outputs/2020-06-22/" \
                        "/tables/blastpPdb/"

# %%
# get Fasta file path list
fileExtension = "fasta"
'''TODO: check this function
getFilePathListFromDirectoryPath(dirPath=str, fileExtension=str)
'''
rvFastaFileWithPdbIdPathList = glob.glob(rvFastasWithPdbIdInFolder + "*.fasta")
print(rvFastaFileWithPdbIdPathList)
for rvFastaFileWithPdbIdPath in rvFastaFileWithPdbIdPathList:
    # print(rvFastaFileWithPdbIdPath[-10:])
    rvFastaIterable     = Bio.SeqIO.read(rvFastaFileWithPdbIdPath, "fasta")
    rvFastaHeader       = getFastaHeaderFromFasta(fasta=rvFastaIterable)
    rvFastaHeaderRvId   = getFastaHeaderInfoFromFastaHeader(fastaHeader=rvFastaHeader,
                                                            headerSep="|", headerPos=0)
    # TODO hacer que la la creación del directorio sea aparte de del seteo del directorio \
    # para que en loop no siga intentando crear indefinidamente los directorios
    blastpPdbOutFile    = getTouchOutFilePath(outPath=blastpPdbOutFolder,
                                            outDirName="rvIdsWithPdbIds",
                                            outFileName=rvFastaHeaderRvId,
                                            fileExtension="tsv")
    runBlastpDefectTsvFormat(blastDbPath=blastpPdbDbPath, 
                            query=rvFastaFileWithPdbIdPath,
                            evalue=1E-10,
                            outFilePath=blastpPdbOutFile,
                            outFileFormat=6, numAlignements=1000,
                            queryCoverage=70, sortHitsByParam=3,
                            sortHspsByParam=3)