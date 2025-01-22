
import pandas as pd

from pathlib                import Path
from joblib                 import load
from sklearn.ensemble       import RandomForestClassifier
from sklearn.preprocessing  import StandardScaler, OneHotEncoder

from config                 import COLUMNS, SCALE_COLUMNS, OH_ENC_COLUMNS, ORD_ENC_COLUMNS


class Model:
    def __init__(self, dir: str='../model/release', version: int=0):
        dir_path: Path = Path(dir).joinpath(str(version))

        self._model: RandomForestClassifier = load(dir_path.joinpath('model.joblib'))
        self._scaler: StandardScaler = load(dir_path.joinpath('scaler.joblib'))
        self._encoder: OneHotEncoder = load(dir_path.joinpath('encoder.joblib'))

        self._data: pd.DataFrame = None


    def predict(self, X: dict) -> int:
        self._process_data(X)
        return int(
            round(self._model.predict_proba(self._data)[0][1] * 100)
        )


    def explain(self) -> dict:
        pass


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


if __name__ == '__main__':
    m = Model()
    print(m.predict(
        {
            'Age': 12,
            'Company Reputation': 'Good',
            'Company Size': 'Large',
            'Company Tenure': 1,
            'Distance from Home': 10,
            'Education Level': 'Bachelor’s Degree',
            'Employee Recognition': 'Medium',
            'Gender': 'Male',
            'Innovation Opportunities': 'Yes',
            'Job Level': 'Mid-level',
            'Job Role': 'Technology',
            'Job Satisfaction': 'Low',
            'Leadership Opportunities': 'No',
            'Marital Status': 'Divorced',
            'Monthly Income': 4000,
            'Number of Dependents': 1,
            'Number of Promotions': 1,
            'Overtime': 'Yes',
            'Performance Rating': 'Average',
            'Remote Work': 'No',
            'Work-Life Balance': 'Below Average',
            'Years at Company': 3
        }
    ))