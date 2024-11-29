from app.processor import process_data


def test_process_data():
    """Test that the process_data function works correctly."""
    input_message = '{"symbol": "AAPL", "prices": [{"price": 1}, {"price": 2}, {"price": 3}, {"price": 4}, {"price": 5}]}'
    result = process_data(input_message)
    
    assert "symbol" in result
    assert result["symbol"] == "AAPL"
    assert "analysis" in result
    assert len(result["analysis"]) == 5
