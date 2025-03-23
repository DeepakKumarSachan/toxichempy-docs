import pandas as pd
import pytest

from toxichempy.utils.data_io_utils import convert_file, read_file, write_file


@pytest.fixture
def sample_dataframe():
    """Fixture that provides a sample DataFrame for testing."""
    return pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})


def test_write_read_csv(sample_dataframe, tmp_path):
    """Test writing and reading a CSV file."""
    file_path = tmp_path / "test.csv"
    write_file(sample_dataframe, file_path)
    df = read_file(file_path)
    pd.testing.assert_frame_equal(df, sample_dataframe)


def test_write_read_excel(sample_dataframe, tmp_path):
    """Test writing and reading an Excel file."""
    file_path = tmp_path / "test.xlsx"
    write_file(sample_dataframe, file_path)
    df = read_file(file_path)
    pd.testing.assert_frame_equal(df, sample_dataframe)


def test_write_read_json(sample_dataframe, tmp_path):
    """Test writing and reading a JSON file."""
    file_path = tmp_path / "test.json"
    write_file(sample_dataframe, file_path)
    df = read_file(file_path)
    pd.testing.assert_frame_equal(df, sample_dataframe, check_like=True)


def test_write_read_pickle(sample_dataframe, tmp_path):
    """Test writing and reading a Pickle file."""
    file_path = tmp_path / "test.pkl"
    write_file(sample_dataframe, file_path)
    df = read_file(file_path)
    pd.testing.assert_frame_equal(df, sample_dataframe)


def test_write_read_txt(sample_dataframe, tmp_path):
    """Test writing and reading a structured TXT file (tab-separated)."""
    file_path = tmp_path / "test.txt"
    write_file(sample_dataframe, file_path, sep="\t")
    # Read the TXT file using a specified delimiter
    df = read_file(file_path, delimiter="\t")
    pd.testing.assert_frame_equal(df, sample_dataframe)


def test_convert_txt_to_csv_without_kwargs(sample_dataframe, tmp_path):
    """Test converting a structured TXT file to a CSV file without extra source kwargs."""
    txt_path = tmp_path / "test.txt"
    csv_path = tmp_path / "test.csv"
    write_file(sample_dataframe, txt_path, sep="\t")
    convert_file(txt_path, csv_path)
    df = read_file(csv_path)
    pd.testing.assert_frame_equal(df, sample_dataframe)


def test_convert_txt_to_csv_with_source_kwargs(sample_dataframe, tmp_path):
    """Test converting a structured TXT file to a CSV file with source kwargs provided."""
    txt_path = tmp_path / "test.txt"
    csv_path = tmp_path / "test.csv"
    write_file(sample_dataframe, txt_path, sep="\t")
    # Pass the delimiter via source_kwargs so read_file gets it explicitly
    convert_file(txt_path, csv_path, source_kwargs={"delimiter": "\t"})
    df = read_file(csv_path)
    pd.testing.assert_frame_equal(df, sample_dataframe)


def test_convert_json_to_csv(sample_dataframe, tmp_path):
    """Test converting a JSON file to a CSV file."""
    json_path = tmp_path / "test.json"
    csv_path = tmp_path / "test.csv"
    write_file(sample_dataframe, json_path)
    convert_file(json_path, csv_path)
    df = read_file(csv_path)
    pd.testing.assert_frame_equal(df, sample_dataframe)


def test_file_not_found():
    """Test that FileNotFoundError is raised for missing files."""
    with pytest.raises(FileNotFoundError):
        read_file("non_existent_file.csv")


def test_unsupported_file_format(sample_dataframe, tmp_path):
    """Test that ValueError is raised for unsupported file formats."""
    file_path = tmp_path / "test.unsupported"
    # Write the file first so it exists
    file_path.write_text("Unsupported file content")
    with pytest.raises(ValueError):
        write_file(sample_dataframe, file_path)
    with pytest.raises(ValueError):
        read_file(file_path)
