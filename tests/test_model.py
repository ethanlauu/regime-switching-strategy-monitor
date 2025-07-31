import pytest
import numpy as np
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from app.model import RegimeHMM

class TestRegimeHMM:
    """Test cases for RegimeHMM class."""
    
    def setup_method(self):
        """Setup test environment."""
        self.test_model_path = '/tmp/test_model.pkl'
        self.sample_df = pd.DataFrame({
            'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
        }, index=pd.date_range('2023-01-01', periods=10))
        self.hmm = RegimeHMM(n_states=3)
    
    def teardown_method(self):
        """Cleanup test environment."""
        if os.path.exists(self.test_model_path):
            os.remove(self.test_model_path)
    
    def test_init(self):
        """Test RegimeHMM initialization."""
        assert self.hmm.n_states == 3
        assert self.hmm.model is None
    
    def test_fit(self):
        """Test model fitting."""
        self.hmm.fit(self.sample_df)
        
        assert self.hmm.model is not None
        assert hasattr(self.hmm.model, 'n_components')
        assert self.hmm.model.n_components == 3
    
    def test_fit_custom_states(self):
        """Test model fitting with custom number of states."""
        self.hmm.fit(self.sample_df, n_states=2)
        
        assert self.hmm.model is not None
        assert self.hmm.model.n_components == 2
    
    def test_predict_proba_fitted(self):
        """Test probability prediction with fitted model."""
        self.hmm.fit(self.sample_df)
        tail_df = self.sample_df.tail(3)
        probs = self.hmm.predict_proba(tail_df)
        
        assert isinstance(probs, np.ndarray)
        assert len(probs) == 3
        assert np.allclose(probs.sum(), 1.0, atol=1e-6)
        assert np.all(probs >= 0)
    
    def test_predict_proba_unfitted(self):
        """Test probability prediction without fitting."""
        tail_df = self.sample_df.tail(3)
        
        with pytest.raises(ValueError, match="Model not fitted"):
            self.hmm.predict_proba(tail_df)
    
    def test_save_fitted(self):
        """Test model saving when fitted."""
        self.hmm.fit(self.sample_df)
        self.hmm.save(self.test_model_path)
        
        assert os.path.exists(self.test_model_path)
    
    def test_save_unfitted(self):
        """Test model saving without fitting."""
        with pytest.raises(ValueError, match="Model not fitted"):
            self.hmm.save(self.test_model_path)
    
    def test_load(self):
        """Test model loading."""
        # First fit and save a model
        self.hmm.fit(self.sample_df)
        self.hmm.save(self.test_model_path)
        
        # Create new instance and load
        new_hmm = RegimeHMM(n_states=3)
        new_hmm.load(self.test_model_path)
        
        assert new_hmm.model is not None
        assert new_hmm.model.n_components == 3
    
    def test_load_nonexistent(self):
        """Test loading non-existent model file."""
        new_hmm = RegimeHMM(n_states=3)
        
        with pytest.raises(FileNotFoundError):
            new_hmm.load('nonexistent.pkl')
    
    def test_integration_fit_predict(self):
        """Test complete fit and predict workflow."""
        # Fit model
        self.hmm.fit(self.sample_df)
        
        # Predict probabilities
        tail_df = self.sample_df.tail(5)
        probs = self.hmm.predict_proba(tail_df)
        
        # Verify results
        assert isinstance(probs, np.ndarray)
        assert len(probs) == 3
        assert np.allclose(probs.sum(), 1.0, atol=1e-6)
        assert np.all(probs >= 0) and np.all(probs <= 1) 