import numpy as np

class SimpleModel:
    def __init__(self):
        self.classes = ['person', 'car', 'bicycle', 'dog', 'cat']
    
    def predict(self, image_data):
        """
        Mock inference function
        In real implementation, you would load your trained model here
        """
        # Simulate processing
        confidence = np.random.uniform(0.7, 0.99)
        predicted_class = np.random.choice(self.classes)
        
        return {
            'prediction': predicted_class,
            'confidence': float(confidence),
            'all_predictions': {
                cls: float(np.random.uniform(0.1, 0.9)) 
                for cls in self.classes
            }
        }