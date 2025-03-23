def generate_example_files():
    """
    Generate example files in different formats for testing.
    """
    df = pd.DataFrame({
        "ID": range(1, 101),
        "Name": [f"Sample_{i}" for i in range(1, 101)],
        "Score": [round(x, 2) for x in (pd.np.random.rand(100) * 100)]
    })
    
    # Save in different formats
    df.to_csv("dummy_data.csv", index=False)
    df.to_json("dummy_data.json", orient="records")
    df.to_excel("dummy_data.xlsx", index=False, sheet_name="Sheet1")
    with open("dummy_data.pkl", "wb") as f:
        pickle.dump(df, f)
    conn = sqlite3.connect("dummy_database.db")
    df.to_sql("dummy_table", conn, if_exists="replace", index=False)
    conn.close()
    df.to_hdf("dummy_data.h5", key="df", mode="w")
    df.to_csv("dummy_data.txt", sep="\t", index=False)
    
    print("✅ Example files generated in CSV, JSON, Excel, Pickle, SQLite, HDF5, and TXT formats.")

# Call function to generate example files
generate_example_files()