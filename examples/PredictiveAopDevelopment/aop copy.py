#!/usr/bin/env python3
import os
import sys
import shutil
import pandas as pd
import requests

# Maximum terms per CTD download request
MAX_TERMS = 500


def dataframe_summary(df):
    """Prints a summary for each column in the DataFrame."""
    for col in df.columns:
        unique_count = df[col].nunique()
        missing_count = df[col].isna().sum()
        print(f"\nColumn: {col}\n  Unique values: {unique_count}\n  Missing values: {missing_count}")


def list_to_file(items, file_name):
    """Saves a list of items to a text file, one per line."""
    with open(file_name, 'w') as f:
        f.write("\n".join(str(item) for item in items))
    print(f"List saved to '{file_name}'")


def aggregate_dataframe(df, group_columns, aggregate_column):
    """Groups the DataFrame by group_columns and aggregates unique values in aggregate_column."""
    aggregated_df = df.groupby(group_columns)[aggregate_column].agg(
        lambda s: ', '.join(s.dropna().unique())
    ).reset_index()
    # Remove duplicated header row if present
    if (aggregated_df.iloc[0] == aggregated_df.columns).all():
        aggregated_df = aggregated_df.iloc[1:]
    return aggregated_df


def print_columns(df):
    """Prints column names of the DataFrame."""
    for col in df.columns:
        print(col)


def export_csv(df, output_filename):
    """Exports DataFrame to CSV without index."""
    csv_file = f"{output_filename}.csv"
    df.to_csv(csv_file, index=False)
    print(f"File saved: {csv_file}")


def filter_and_save_dataframe(df, column, value, output_filename):
    """Filters the DataFrame based on a column value and saves the result to CSV."""
    filtered_df = df[df[column] == value]
    export_csv(filtered_df, output_filename)


def extract_unique_and_save(df, column, output_filename):
    """Extracts unique values from a DataFrame column and saves them to a text file."""
    unique_values = df[column].dropna().unique()
    print(f"\nUnique {column} Count: {len(unique_values)}")
    list_to_file(unique_values, output_filename)


def read_txt_file_to_list(filename):
    """Reads a text file and returns a list of stripped, non-empty lines."""
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading '{filename}': {e}")
        return []


def ctd_download(input_type, input_terms, report, file_format, file_base_name, ontology_association=None):
    """
    Downloads data in chunks from the CTD Batch Query and combines them into a single file.
    
    Parameters:
      input_type (str): Type of input ('chem', 'disease', etc.).
      input_terms (list): List of terms.
      report (str): Report type.
      file_format (str): Output format ('csv', etc.).
      file_base_name (str): Base name for output files.
      ontology_association (str): Optional ontology association.
    """
    total_chunks = (len(input_terms) - 1) // MAX_TERMS + 1
    folder_name = f"{file_base_name}_files"
    combined_file_name = f"{file_base_name}.{file_format}"

    # Remove the existing folder, if any, then create a new one.
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)
    os.makedirs(folder_name)

    for i in range(total_chunks):
        chunk = input_terms[i * MAX_TERMS: (i + 1) * MAX_TERMS]
        input_terms_str = '|'.join(chunk)
        url = (f'https://ctdbase.org/tools/batchQuery.go?inputType={input_type}&'
               f'inputTerms={input_terms_str}&report={report}&format={file_format}&'
               f'ontology={ontology_association}&inputTermSearchType=directAssociations')
        chunk_file = os.path.join(folder_name, f"{file_base_name}_{i+1}.csv")
        print(f"Downloading chunk {i+1} of {total_chunks}...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(chunk_file, 'wb') as f:
                for data in response.iter_content(chunk_size=1024 * 1024):
                    f.write(data)
            print(f"Chunk {i+1} downloaded: {chunk_file}")
        else:
            print(f"Failed to download chunk {i+1} (status code: {response.status_code}).")
            break

    # Combine all downloaded chunks into one file.
    if os.path.exists(folder_name):
        with open(combined_file_name, 'wb') as combined_file:
            for i in range(1, total_chunks + 1):
                chunk_file = os.path.join(folder_name, f"{file_base_name}_{i}.csv")
                with open(chunk_file, 'rb') as cf:
                    combined_file.write(cf.read())
        print(f"Combined file created: {combined_file_name}")
    else:
        print("No chunks were downloaded; combined file not created.")


def find_common_elements(list1, list2):
    """Returns the common elements between two lists."""
    return list(set(list1) & set(list2))


def main(chemical_file):
    # 1. Read chemicals from file.
    chemical_list = read_txt_file_to_list("chemical.txt")
    print(f"Chemicals present for analysis: {len(chemical_list)}")

    # 2. Download chemicals associated with diseases.
    ctd_download('chem', chemical_list, 'diseases_curated', 'csv', 'raw_chemical_disease')
    df_raw_chemical_disease = pd.read_csv('raw_chemical_disease.csv')
    print(f"Unique DiseaseID Count: {df_raw_chemical_disease['DiseaseID'].nunique()}")
    print(f"Unique CasRN Count: {df_raw_chemical_disease['CasRN'].nunique()}")

    # 3. Filter for DirectEvidence == marker/mechanism.
    filter_and_save_dataframe(df_raw_chemical_disease, 'DirectEvidence', 'marker/mechanism', 'chemical_disease')
    df_chemical_disease = pd.read_csv('chemical_disease.csv')
    print(f"Shape of chemical_disease.csv: {df_chemical_disease.shape}")

    # 4. Aggregate chemical-disease associations.
    aggregated_chemical_disease = aggregate_dataframe(
        df_chemical_disease,
        ['# Input', 'ChemicalName', 'ChemicalID', 'CasRN'],
        'DiseaseID'
    )
    aggregated_chemical_disease.to_csv("aggregated_chemical_disease.csv", index=False)
    print(f"Shape of aggregated_chemical_disease.csv: {aggregated_chemical_disease.shape}")

    # 5. Extract unique diseases and chemicals.
    extract_unique_and_save(df_chemical_disease, "DiseaseID", "diseases_chemical_disease.txt")
    extract_unique_and_save(df_chemical_disease, "CasRN", "chemicals_chemical_disease.txt")
    disease_list = read_txt_file_to_list('diseases_chemical_disease.txt')
    chemical_list = read_txt_file_to_list('chemicals_chemical_disease.txt')

    # 6. Download additional datasets.
    ctd_download('chem', chemical_list, 'phenotypes_curated', 'csv', 'chemical_phenotype')
    ctd_download('chem', chemical_list, 'genes_curated', 'csv', 'chemical_gene')
    ctd_download('disease', disease_list, 'genes_curated', 'csv', 'disease_gene')

    df_chemical_phenotype = pd.read_csv('chemical_phenotype.csv', dtype=str)
    df_chemical_gene = pd.read_csv('chemical_gene.csv', dtype=str)
    df_disease_gene = pd.read_csv('disease_gene.csv', dtype=str)
    print("Loaded: df_chemical_phenotype, df_chemical_gene, df_disease_gene")
    print(f"Shapes: {df_chemical_phenotype.shape}, {df_chemical_gene.shape}, {df_disease_gene.shape}")

    # 7. Aggregate phenotype, gene, and disease gene information.
    aggregated_chemical_phenotype = aggregate_dataframe(
        df_chemical_phenotype,
        ['# Input', 'ChemicalName', 'ChemicalID', 'CasRN'],
        'PhenotypeID'
    )
    aggregated_chemical_phenotype.to_csv("aggregated_chemical_phenotype.csv", index=False)

    aggregated_chemical_gene = aggregate_dataframe(
        df_chemical_gene,
        ['# Input', 'ChemicalName', 'ChemicalId', 'CasRN'],
        'GeneSymbol'
    )
    aggregated_chemical_gene.rename(columns={'ChemicalId': 'ChemicalID'}, inplace=True)
    aggregated_chemical_gene.to_csv("aggregated_chemical_gene.csv", index=False)

    aggregated_disease_gene = aggregate_dataframe(
        df_disease_gene,
        ['# Input', 'DiseaseName', 'DiseaseID'],
        'GeneSymbol'
    )
    aggregated_disease_gene.to_csv("aggregated_disease_gene.csv", index=False)
    print("Columns after aggregations:")
    print_columns(df_chemical_disease)
    print_columns(aggregated_chemical_phenotype)
    print_columns(aggregated_disease_gene)
    print_columns(aggregated_chemical_gene)

    # 8. Merge chemical_disease with phenotype and gene data.
    merged_cd_phenotype = pd.merge(
        df_chemical_disease,
        aggregated_chemical_phenotype[['# Input', 'ChemicalName', 'ChemicalID', 'CasRN', 'PhenotypeID']],
        on=['# Input', 'ChemicalName', 'ChemicalID', 'CasRN'],
        how='left'
    )
    merged_cd_phenotype_gene = pd.merge(
        merged_cd_phenotype,
        aggregated_chemical_gene[['# Input', 'ChemicalName', 'ChemicalID', 'CasRN', 'GeneSymbol']],
        on=['# Input', 'ChemicalName', 'ChemicalID', 'CasRN'],
        how='left'
    )
    merged_cd_phenotype_gene.rename(columns={'GeneSymbol': 'ChemicalGeneSymbol'}, inplace=True)
    export_csv(merged_cd_phenotype_gene, 'chemical_phenotype_gene_disease')

    # 9. Merge with disease gene data.
    df_chemical_phenotype_gene_disease = pd.read_csv('chemical_phenotype_gene_disease.csv')
    df_aggregated_disease_gene = pd.read_csv('aggregated_disease_gene.csv')
    df_aggregated_disease_gene.rename(columns={'GeneSymbol': 'DiseaseGeneSymbol'}, inplace=True)
    merged_df = pd.merge(
        df_chemical_phenotype_gene_disease,
        df_aggregated_disease_gene[['DiseaseID', 'DiseaseGeneSymbol']],
        on='DiseaseID',
        how='left'
    )

    # 10. Find common genes between chemical and disease gene symbols.
    def find_common_genes(row):
        chem_genes = [gene.strip() for gene in str(row.get('ChemicalGeneSymbol', '')).split(',') if gene.strip()]
        dis_genes = [gene.strip() for gene in str(row.get('DiseaseGeneSymbol', '')).split(',') if gene.strip()]
        common = set(chem_genes) & set(dis_genes)
        return ', '.join(common) if common else pd.NA

    merged_df['common_gene_chemical_disease'] = merged_df.apply(find_common_genes, axis=1)
    export_csv(merged_df, 'cd_common_gene')

    # 11. Extract and process common gene list.
    df_cd_common_gene = pd.read_csv('cd_common_gene.csv')
    extract_unique_and_save(df_cd_common_gene, "common_gene_chemical_disease", "cd_common_gene_list.txt")

    # Process the unique values from the file.
    input_file_path = 'cd_common_gene_list.txt'
    output_file_path = 'set_cd_common_gene_list.txt'
    unique_values = set()
    with open(input_file_path, 'r') as infile:
        for line in infile:
            for value in line.strip().split(','):
                value = value.strip()
                if value.lower() != 'nan' and value:
                    unique_values.add(value)
    with open(output_file_path, 'w') as outfile:
        for value in sorted(unique_values):
            outfile.write(value + '\n')
    print(f"Unique values saved in {output_file_path}")

    set_cd_common_gene_list = read_txt_file_to_list('set_cd_common_gene_list.txt')
    ctd_download('gene', set_cd_common_gene_list, 'go', 'csv', 'raw_disease_gene_ontology', ontology_association='go_bp')

    # 12. Process disease gene ontology.
    df_raw_disease_gene_ontology = pd.read_csv('raw_disease_gene_ontology.csv', dtype=str)
    aggregated_disease_gene_ontology = aggregate_dataframe(
        df_raw_disease_gene_ontology,
        ['# Input', 'GeneSymbol'],
        'GoTermID'
    )
    aggregated_disease_gene_ontology.to_csv("aggregated_disease_gene.csv", index=False)
    df_aggregated_df_raw_disease_gene = pd.read_csv('aggregated_disease_gene.csv')
    print_columns(df_aggregated_df_raw_disease_gene)

    # Create a mapping from gene to GO terms.
    gene_go_dict = (df_aggregated_df_raw_disease_gene
                    .groupby('GeneSymbol')['GoTermID']
                    .apply(list)
                    .to_dict())

    # 13. Map disease gene ontology to common genes.
    df_cd_common_gene['disease_gene_ontology'] = pd.NA
    for idx, row in df_cd_common_gene.iterrows():
        if pd.notna(row['common_gene_chemical_disease']):
            genes = [g.strip() for g in row['common_gene_chemical_disease'].split(',') if g.strip()]
            go_terms = {term for gene in genes if gene in gene_go_dict for term in gene_go_dict[gene]}
            df_cd_common_gene.at[idx, 'disease_gene_ontology'] = ', '.join(go_terms) if go_terms else pd.NA

    df_cd_common_gene.to_csv("finaldf.csv", index=False)
    final_df = pd.read_csv('finaldf.csv')
    print_columns(final_df)

    # 14. Find common ontology between PhenotypeID and disease_gene_ontology.
    final_df['common_ontology'] = pd.NA
    for idx, row in final_df.iterrows():
        phenotype_ids = [p.strip() for p in str(row.get('PhenotypeID', '')).split(',') if p.strip()]
        disease_ontologies = [d.strip() for d in str(row.get('disease_gene_ontology', '')).split(',') if d.strip()]
        common = find_common_elements(phenotype_ids, disease_ontologies)
        final_df.at[idx, 'common_ontology'] = ', '.join(common) if common else pd.NA

    final_df.to_csv('complete.csv', index=False)
    print("DataFrame saved as complete.csv.")

    complete_df = pd.read_csv('complete.csv')
    dataframe_summary(complete_df)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py <chemical_file>")
        sys.exit(1)
    main(sys.argv[1])
    print("Script executed successfully.")
    print("All tasks completed successfully.")  