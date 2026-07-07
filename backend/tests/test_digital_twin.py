import pytest
from app.services.digital_twin import DigitalTwinService

class TestDigitalTwin:
    def test_predict_crowd_movement(self):
        service = DigitalTwinService()
        predictions = await service.predict_crowd_movement(15)
        assert "predictions" in predictions
        assert "summary" in predictions
    
    def test_heatmap_data(self):
        service = DigitalTwinService()
        heatmap = await service.get_heatmap_data()
        assert "data" in heatmap
        assert "legend" in heatmap
    
    def test_section_update(self):
        service = DigitalTwinService()
        result = await service.update_section_density("A1", 0.8)
        assert result["status"] == "updated"