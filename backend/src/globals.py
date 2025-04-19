import os

dois = {
    "_dPCR_SOP_for_Quantification_of_Antibiotic_Resistance_Genes_121916.txt" : "10.17504/protocols.io.5qpvo96wzv4o/v1",
    "After-LCM_(Laser-Capture_Microdissection)_procedure_123238.txt" :  "10.17504/protocols.io.e6nvwb3wwvmk/v1",
    "Aβ_ELISA_119915.txt" : "10.17504/protocols.io.n2bvj9e6plk5/v1",
    "BD_FACSDiscover_S8_-_Bi-weekly_Maintenance_and_Cleaning_Protocol_123580.txt" : "",
    "Calcium_phosphate_transfection_of_Oxyrrhis_marina_with_an_Alexa488-labelled_DNA_fragment_5180.txt" : "10.17504/protocols.io.ha4b2gw",
    "Confocal_Microscopy_of_DFP-Treated_Cells_120015.txt" : "10.17504/protocols.io.n2bvj9e9blk5/v1",
    "Creation_of_pooled_CRISPR_KO_cell_lines_using_Synthego_sgRNA_123248.txt" : "10.17504/protocols.io.bp2l6dqodvqe/v1",
    "CRISPR-Cas9_gene_editing_in_hiPSC_123201.txt" : "10.17504/protocols.io.j8nlk9xxdv5r/v1",
    "CRISPR_Detect_for_Evercode™_WT_v2_123399.txt" : "10.17504/protocols.io.14egn952yl5d/v1",
    "CTAB-Based_RNA_Extraction_with_Qiagen_RNeasy_Cleanup_120178.txt" : "10.17504/protocols.io.261gerk8wl47/v1",
    "DNA_extraction_and_qPCR_protocol_for_sensitive_detection_of_Trypanosoma_cruzi_in_blood_119293.txt" : "10.17504/protocols.io.ewov1dm87vr2/v1",
    "Euplotes_crassus_transfection_using_FuGene_HD_Transfection_Reagent_as_vehicle_(provisional)_5445.txt" : "10.17504/protocols.io.hjdb4i6",
    "High_Efficiency_Transformation_Protocol_(C2987H)_33939.txt" : "10.17504/protocols.io.bddti26n",
    "High_Efficiency_Transformation_Protocol_(C2987I)_33940.txt" : "10.17504/protocols.io.bddui26w",
    "High_Efficiency_Transformation_Protocol_using_NEB_10-beta_Competent_E._coli_(C3019)_33941.txt" : "10.17504/protocols.io.zewov12ogr24/v6",
    "High-throughput_96-well_plate-based_porcine_antibody_isolation_protocol_101284.txt" : "10.17504/protocols.io.yxmvmee6ng3p/v1",
    "Measuring_ROS_production_by_neutrophils_using_DCFH-DA_probe_and_flow_Cytometry_118815.txt" : "10.17504/protocols.io.n2bvj9j3blk5/v1",
    "Monkeypox_virus_multiplexed_PCR_amplicon_sequencing_(PrimalSeq) _126391.txt" : "10.17504/protocols.io.5qpvob1nbl4o/v5",
    "Protocol_to_isolate_and_fix_nuclei_from_flash_frozen_mouse_brain_for_IGVF_SHARE-seq__119404.txt" : "10.17504/protocols.io.5jyl8dq29g2w/v1",
    "Singleplex_Assay_for_Function_Measurements_119208.txt" : "10.17504/protocols.io.dm6gpzwx8lzp/v3",
    "SOI_-_BDAria_Fusion_Cell_Sorter_-_Instrument_Startup_113750.txt" : "",
    "Whole_genome_amplification_of_human_parechovirus_type_3_(PEV-A3)_utilizing_tiling-PCR_126707.txt" : "10.17504/protocols.io.q26g758q3lwz/v1"
}

keyword_list = []

def load_keywords():
    global keyword_list
    keyword_set = set()
    for filename in os.listdir("../data"):
        file_path = os.path.join("../data", filename)
        with open(file_path, 'r') as file:
            content = file.read()
            start = content.find("Keywords: ")
            end = content[start+10:].find("~")
            keywords_str = content[start+10:start+end+10]
            keywords_str = keywords_str.replace("\n", "")
            keywords = keywords_str.split(", ")
            # keyword_subset = set(keywords)
            keyword_set.update(keywords)
    keyword_set.remove("")
    keyword_list = sorted(keyword_set)