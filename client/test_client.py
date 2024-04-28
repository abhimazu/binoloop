import pytest
from modelclient import send_request, process_dataset_loop
import pandas as pd

def test_send_request(mocker):
    """Test sending a request to the server."""
    sample_data = {
        "prompt_id": 0,
        "essay_output": "Abc def ghj",
        "student_id": "test321"
    }
    mocker.patch('requests.post', return_value=mocker.Mock(status_code=200, json=lambda: {"criticism": "Good job", "student_id": "test321", "prompt_id": 0}))
    response = send_request(sample_data)
    assert response is not None
    assert response['criticism'] == "Good job"
    assert response['student_id'] == "test321"

def test_process_dataset_loop(mocker):
    """Test the processing loop with a dataset."""
    mocker.patch('modelclient.send_request', return_value={"criticism": "Well done", "student_id": "test321", "prompt_id": 0})
    df = pd.DataFrame({
        "prompt_id": [0],
        "AI_Essay": ["Abc def ghj"],
        "student_id": ["test321"]
    })
    results = process_dataset_loop(df, 0)
    assert len(results) == 1
    assert results[0]["criticism"] == "Well done"
    assert results[0]["student_id"] == "test321"

