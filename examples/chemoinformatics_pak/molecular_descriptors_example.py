# examples/compute_descriptors.py

from toxichempy.chemoinformatics import DescriptorCalculator
import ace_tools as tools  # If you want to display tables in Jupyter Notebook

# Sample molecules (SMILES format)
smiles_list = [
    "CCO",  # Ethanol
    "CC(=O)O",  # Acetate
    "CCN(CC)CC",  # Tetraethylamine
    "CC(C)CCO",  # Pentanol
    "O=C(C)Oc1ccccc1C(=O)O"  # Aspirin
]

# Initialize descriptor calculator
calculator = DescriptorCalculator(smiles_list)

# Compute descriptors
descriptor_df = calculator.calculate_descriptors()

# Display the table (for Jupyter Notebook)
tools.display_dataframe_to_user("Molecular Descriptors", descriptor_df)

# Save as CSV (optional)
descriptor_df.to_csv("molecular_descriptors.csv", index=False)

# Print descriptors
print(descriptor_df)
