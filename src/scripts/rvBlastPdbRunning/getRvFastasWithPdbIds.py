import os
import sys
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

def getRvFastasWithPdbId(mfastaInFile, rvFastasWithPdbIdOutFolder):
    """
    Save each rvFasta of de rvMfasta in individual fasta if the Revenant have PDB structure
    """
    # creating multifasta iteractor
    rvFastaIterator = getFastaIteratorObjectFromMultifasta(mfastaPath=mfastaInFile)
    
    #try:
    #    os.makedirs(rvFastasWithPdbIdOutFolder)
    #except FileExistsError:
    #    print("Folder exist error")
    
    
    for rvFasta in rvFastaIterator:
        #ount = 1
        # check the if the Revenant have PDB structure
        if fastaHeaderHavePdbIdEntry(fasta=rvFasta, headerSep="|",
                                    pdbIdEntryHeaderPos=1,
                                    pdbIdNoExistParam=""):
            rvFastaHeader = getFastaHeaderFromFasta(fasta=rvFasta)
            rvFastaHeaderRvId = getFastaHeaderInfoFromFastaHeader(fastaHeader=rvFastaHeader,
                                                                headerSep="|", headerPos=0)
            # save the rvFasta in individual fasta
            # TODO if exist rvFasta file exist in the processed_data dir no run the line
            Bio.SeqIO.write(rvFasta, rvFastasWithPdbIdOutFolder + "/" + "%s.fasta" % rvFastaHeaderRvId, "fasta")
            #count += 1
            print("The %s Revenant fasta with structure generated" % rvFastaHeaderRvId)
