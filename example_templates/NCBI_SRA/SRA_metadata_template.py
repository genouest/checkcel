from checkcel import Checkplate
from checkcel.validators import SetValidator, NoValidator, LinkedSetValidator
from collections import OrderedDict


class MyTemplate(Checkplate):
    validators = OrderedDict([
        ("sample_name", NoValidator()),
        ("library_ID", NoValidator()),
        ("title", NoValidator()),
        ("library_strategy", SetValidator(valid_values=["WGA", "WGS", "WXS", "RNA-Seq", "miRNA-Seq", "WCS", "CLONE", "POOLCLONE", "AMPLICON", "CLONEEND", "FINISHING", "ChIP-Seq", "MNase-Seq", "DNase-Hypersensitivity", "Bisulfite-Seq", "Tn-Seq", "EST", "FL-cDNA", "CTS", "MRE-Seq", "MeDIP-Seq", "MBD-Seq", "Synthetic-Long-Read", "ATAC-seq", "ChIA-PET", "FAIRE-seq", "Hi-C", "ncRNA-Seq", "RAD-Seq", "RIP-Seq", "SELEX", "ssRNA-seq", "Targeted-Capture", "Tethered Chromatin Conformation Capture", "OTHER"])),
        ("library_source", SetValidator(valid_values=["GENOMIC", "TRANSCRIPTOMIC", "METAGENOMIC", "METATRANSCRIPTOMIC", "SYNTHETIC", "VIRAL RNA", "GENOMIC SINGLE CELL", "TRANSCRIPTOMIC SINGLE CELL", "OTHER"])),
        ("library_selection", SetValidator(valid_values=["RANDOM", "PCR", "RANDOM PCR", "RT-PCR", "HMPR", "MF", "CF-S", "CF-M", "CF-H", "CF-T", "MDA", "MSLL", "cDNA", "ChIP", "MNase", "DNAse", "Hybrid Selection", "Reduced Representation", "Restriction Digest", "5-methylcytidine antibody", "MBD2 protein methyl-CpG binding domain", "CAGE", "RACE", "size fractionation", "Padlock probes capture method", "other", "unspecified", "cDNA_oligo_dT", "cDNA_randomPriming", "Inverse rRNA", "Oligo-dT", "PolyA", "repeat fractionation"])),
        ("library_layout", SetValidator(valid_values=["single", "paired"])),
        ("platform", SetValidator(valid_values=["_LS454", "ABI_SOLID", "BGISEQ", "CAPILLARY", "COMPLETE_GENOMICS", "HELICOS", "ILLUMINA", "ION_TORRENT", "OXFORD_NANOPORE", "PACBIO_SMRT"])),
        ("instrument_model", LinkedSetValidator("platform", {"_LS454": ["454 GS", "454 GS 20", "454 GS FLX", "454 GS FLX+", "454 GS FLX Titanium", "454 GS Junior"], "ABI_SOLID": ["AB 5500 Genetic Analyzer", "AB 5500xl Genetic Analyzer", "AB 5500x-Wl Genetic Analyzer", "AB SOLiD 3 Plus System", "AB SOLiD 4 System", "AB SOLiD 4hq System", "AB SOLiD PI System", "AB SOLiD System", "AB SOLiD System 2.0", "AB SOLiD System 3.0"], "BGISEQ": ["BGISEQ-500", "None", "None", "None"], "CAPILLARY": ["AB 310 Genetic Analyzer", "AB 3130 Genetic Analyzer", "AB 3130xL Genetic Analyzer", "AB 3500 Genetic Analyzer", "AB 3500xL Genetic Analyzer", "AB 3730 Genetic Analyzer", "AB 3730xL Genetic Analyzer"], "COMPLETE_GENOMICS": ["Complete Genomics"], "HELICOS": ["Helicos HeliScope", "None"], "ILLUMINA": ["HiSeq X Five", "HiSeq X Ten", "Illumina Genome Analyzer", "Illumina Genome Analyzer II", "Illumina Genome Analyzer IIx", "Illumina HiScanSQ", "Illumina HiSeq 1000", "Illumina HiSeq 1500", "Illumina HiSeq 2000", "Illumina HiSeq 2500", "Illumina HiSeq 3000", "Illumina HiSeq 4000", "Illumina iSeq 100", "Illumina NovaSeq 6000", "Illumina MiniSeq", "Illumina MiSeq", "NextSeq 500", "NextSeq 550"], "ION_TORRENT": ["Ion Torrent PGM", "Ion Torrent Proton", "Ion Torrent S5 XL", "Ion Torrent S5"], "OXFORD_NANOPORE": ["GridION", "MinION", "PromethION"], "PACBIO_SMRT": ["PacBio RS", "PacBio RS II", "PacBio Sequel", "PacBio Sequel II"]})),
        ("design_description", NoValidator()),
        ("filetype", SetValidator(valid_values=["bam", "srf", "sff", "fastq", "454_native", "Helicos_native", "SOLiD_native", "PacBio_HDF5", "CompleteGenomics_native", "OxfordNanopore_native"])),
        ("filename", NoValidator()),
        ("filename2", NoValidator()),
        ("filename3", NoValidator()),
        ("filename4", NoValidator()),
        ("filename5", NoValidator()),
        ("filename6", NoValidator()),
        ("filename7", NoValidator()),
        ("filename8", NoValidator()),
        ("assembly", NoValidator()),
        ("fasta_file", NoValidator())
    ])
