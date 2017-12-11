# -*- coding: utf-8 -*-
import sys


def filter_ohnologuous_genes(input_file, output_file, min_window_size):
    """
    Filter ohnologuous pair from synmap output
    Args :
       - input_file : the path to the input file which is the dagchainer output of synmap (see doc)
       - output_file : the path to the output file
       - min_window_size : minimum synteny window size (on whichever chromosome) in which the ohnologuous genes will be retained
    """
    min_window_size = int(min_window_size)
    window_dict = build_window_dict(input_file)
    filtered_window_dict = filter_window_dict(window_dict, min_window_size)
    ohnologuous_genes = get_ohnologuous_genes(filtered_window_dict)
    write_results(ohnologuous_genes, output_file)


def write_results(ohnologuous_genes, output_file):
    """
    Write results in the output file
    """
    output_handler = open(output_file, "w")

    for ohnologuous_pair in ohnologuous_genes:
        ohnologuous_pair = list(ohnologuous_pair)
        to_write = [ohnologuous_pair[0], ohnologuous_pair[1]]
        output_handler.write("\t".join(to_write) + "\n")


def get_ohnologuous_genes(filtered_window_dict):
    """
    Get unique pairs of ohnologuous genes from the filtered windows dictionnary and return a list of pairs of ohnologuous_genes
    """
    ohnologuous_genes = []

    genes_context_dict = {}

    for window in filtered_window_dict:
        window_effective_size = max(filtered_window_dict[window]["chrA_window_size"], filtered_window_dict[window]["chrB_window_size"])

        for gene_pair in filtered_window_dict[window]["gene_pairs"]:
            gene_pair_list = list(gene_pair)
            check_list = []

            for gene in gene_pair_list:
                if gene not in genes_context_dict:
                    genes_context_dict[gene] = 0
                if window_effective_size > genes_context_dict[gene]:
                    check_list.append("o")
                else:
                    check_list.append("x")

            if "x" not in check_list:
                for ohnologuous_pair in ohnologuous_genes:
                    if (gene_pair_list[0] in ohnologuous_pair) or (gene_pair_list[1] in ohnologuous_pair):
                        ohnologuous_genes.remove(ohnologuous_pair)

                for gene in gene_pair_list:
                    genes_context_dict[gene] = window_effective_size
                ohnologuous_genes.append(gene_pair)

    return ohnologuous_genes


def filter_window_dict(window_dict, min_window_size):
    """
    Filter small windows out of the window dictionnary and return a filtered window dictionnary
    """
    filtered_window_dict = {}

    for window in window_dict:


        window_dict[window]["chrA_window_size"] = max(window_dict[window]["chrA_window_coords"]) - min(window_dict[window]["chrA_window_coords"])
        window_dict[window]["chrB_window_size"] = max(window_dict[window]["chrB_window_coords"]) - min(window_dict[window]["chrB_window_coords"])


        window_effective_size = max(window_dict[window]["chrA_window_size"], window_dict[window]["chrB_window_size"])

        if window_effective_size >= min_window_size:
            filtered_window_dict[window] = window_dict[window]

    return filtered_window_dict


# Parse the input file to retrieve all the necessary data and store them in a window_dict
def build_window_dict(input_file):

    window_dict = {}
    window_count = 0

    for line in open(input_file, "r"):

        # Hash is the infile separator for synteny windows. The window id in the dict will change (window_count) each time a hash is encountered
        if line[0] == "#":
            window_count += 1

        else:
            sl = line.split("\t")
            window_name = str(window_count)

            if window_name not in window_dict:
                window_dict[window_name] = {"chrA_window_size": 0, "chrB_window_size": 0, "chrA_window_coords" : [],  "chrB_window_coords" : [], "gene_pairs": [], "chromosome_pair": ""}

            gene_pair = (sl[1].split("||")[3].split(":")[1].split(".")[0], sl[5].split("||")[3].split(":")[1].split(".")[0])
            gene_pair = set(gene_pair)

            if len(list(gene_pair)) > 1:
                window_dict[window_name]["gene_pairs"].append(gene_pair)

            chrA = sl[0]
            chrA_cds_start = int(sl[1].split("||")[1])

            chrB = sl[4]
            chrB_cds_start = int(sl[5].split("||")[1])

            if window_dict[window_name]["chromosome_pair"] == "":
                window_dict[window_name]["chromosome_pair"] = set((chrA, chrB))

            window_dict[window_name]["chrA_window_coords"].append(chrA_cds_start)
            window_dict[window_name]["chrB_window_coords"].append(chrB_cds_start)

    return window_dict


filter_ohnologuous_genes(sys.argv[1], sys.argv[2], sys.argv[3])
