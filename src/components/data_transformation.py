import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

class DataTranformation:
    def __init__(self):
        self.data_tranformation_config=DataTransformationConfig()

    def get_data_transfomrer(self):
        '''
        this function is responsible for data transformation
        '''
        try:
            numerical_features=['reading_score', 'writing_score']
            categorical_features=['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
            num_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='most_frequent')),
                    ("One_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info("categoriy and numrical data encoded and scaled")
            preprocesoor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_features),
                    ("cat_pipeline",cat_pipeline,categorical_features)
                ]
            )
            return preprocesoor                    
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_tranformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("read train and test data")
            logging.info("obtaining pre processing object")
            preprocesssing_obj=self.get_data_transfomrer()
            target_column_name="math_score"
            numerical_features=['reading_score', 'writing_score']
            input_features_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_features_train_df=train_df[target_column_name]
            input_features_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_features_test_df=test_df[target_column_name]
            logging.info("apllying preporcessing...")
            input_feature_train_arr=preprocesssing_obj.fit_transform(input_features_train_df)
            input_feature_test_arr=preprocesssing_obj.transform(input_features_test_df)
            train_arr=np.c_[
                input_feature_train_arr,np.array(target_features_train_df)
            ]
            test_arr=np.c_[
                input_feature_test_arr,np.array(target_features_test_df)
            ]
            logging.info("saved preprocessing object")
            save_object(
                file_path=self.data_tranformation_config.preprocessor_obj_file_path,
                obj=preprocesssing_obj
            )
            return (
                train_arr,
                test_arr,
                self.data_tranformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)