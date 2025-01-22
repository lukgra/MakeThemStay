
import numpy as np
import pandas as pd

from typing                 import Tuple
from pathlib                import Path
from joblib                 import load
from sklearn.ensemble       import RandomForestClassifier
from sklearn.preprocessing  import StandardScaler, OneHotEncoder
from shap                   import TreeExplainer

from config                 import COLUMNS, SCALE_COLUMNS, OH_ENC_COLUMNS, ORD_ENC_COLUMNS


class Model:
    def __init__(self, dir: str='../model/release', version: int=0):
        dir_path: Path = Path(dir).joinpath(str(version))

        self._model: RandomForestClassifier = load(dir_path.joinpath('model.joblib'))
        self._scaler: StandardScaler = load(dir_path.joinpath('scaler.joblib'))
        self._encoder: OneHotEncoder = load(dir_path.joinpath('encoder.joblib'))
        self._explainer: TreeExplainer = TreeExplainer(self._model)

        self._data: pd.DataFrame = None
        self._prediction: int = None
        self._exp_features: list = None


    def predict(self, X: dict) -> Tuple[int, list[str]]:
        # --- Processing --- #
        self._process_data(X)

        # --- Prediction --- #
        self._run_model_prediction()

        # --- Explanation --- #
        self._explain_prediction()

        return self._prediction, self._exp_features


    def _process_data(self, X: dict) -> None:
        # --- Input --- #
        self._data: pd.DataFrame = pd.DataFrame([X]).reindex(columns=COLUMNS.keys())

        # --- Scale --- #
        self._data[SCALE_COLUMNS] = self._scaler.transform(self._data[SCALE_COLUMNS])

        # --- One-Hot Encoding --- #
        encoded_df = pd.DataFrame(
            self._encoder.transform(self._data[OH_ENC_COLUMNS]).toarray(),
            columns=self._encoder.get_feature_names_out(OH_ENC_COLUMNS)
        )
        self._data = pd.concat([self._data.drop(columns=OH_ENC_COLUMNS), encoded_df], axis=1)

        # --- Oridnal encoding --- # 
        self._data['Gender'] = self._data['Gender'].map({'Male': 0, 'Female': 1})
        self._data[ORD_ENC_COLUMNS] = self._data[ORD_ENC_COLUMNS].apply(lambda col: col.map({'No': 0, 'Yes': 1}))


    def _run_model_prediction(self) -> int:
        self._prediction = round(self._model.predict_proba(self._data)[0][1] * 100)
        

    def _explain_prediction(self) -> list:
        shap_values: np.ndarray = self._explainer.shap_values(self._data)[..., 1] # Second column
        shap_df: pd.DataFrame = pd.DataFrame({
                "Feature": self._data.columns,
                "Feature Value": self._data.values.flatten(),
                "SHAP Value": shap_values.flatten()
            }).sort_values(
                by=['SHAP Value'],
                ascending=False
            ).reset_index(drop=True)
        
        # This crazy line removes records, that have one hot encoded columns with a value of 0
        shap_df = shap_df[~((shap_df['Feature'].str.contains('_')) & (shap_df['Feature Value'] == 0))]

        # TODO: fix the one hot feature that contains 1 (remove the _ sign and make the value different second element of the field)
        
        self._exp_features = list(shap_df.head(5)['Feature'])