import yaml
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, MaxAbsScaler
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, OrdinalEncoder
from category_encoders import *

class Preprocessor:
    def __init__(self, config_file):
        self.config_file = config_file
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
            
            
    def _save_updated_config(self):
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f)
            
    
    def _ask_user_for_feature_config(self, missing_feature_name):
        print(f"The feature '{missing_feature_name}' is not available in the dataset.")
        
        feature_type = input("Enter the feature type (numeric or categorical): ")
        dtype = input("Enter the data type (e.g., int64, float64, object): ")
        description = input("Enter a description of the feature: ")

        feature_config = {
            'name': missing_feature_name,
            'type': feature_type,
            'dtype': dtype,
            'description': description
        }

        if feature_type == 'numeric':
            invalid = input("Enter a list of invalid values separated by commas (e.g., -9999,.,.A): ").split(',')
            feature_config['invalid'] = invalid

            missing_values_handling = input("Enter the method to handle missing values (drop_rows, drop_columns, impute_mean, impute_median, impute_mode, impute_knn, none): ")
            feature_config['missing_values_handling'] = missing_values_handling

            preprocessing = input("Enter the feature scaling method (min_max_scaling, standard_scaling, robust_scaling, max_abs_scaling, manual, none): ")
            feature_config['preprocessing'] = {'feature_scaling': preprocessing}

        elif feature_type == 'categorical':
            invalid = input("Enter a list of invalid values separated by commas (e.g., -9999,.,.A): ").split(',')
            feature_config['invalid'] = invalid

            missing_values_handling = input("Enter the method to handle missing values (drop_rows, drop_columns, impute_mode, impute_custom_category, none): ")
            feature_config['missing_values_handling'] = missing_values_handling

            encoding_method = input("Enter the encoding method for categorical features (one_hot_encoding, label_encoding, ordinal_encoding, binary_encoding, target_encoding, none): ")
            feature_config['preprocessing'] = {'encoding_method': encoding_method}

            if encoding_method == 'target_encoding':
                target_column = input("Enter the target column for target encoding: ")
                feature_config['preprocessing']['target_column'] = target_column

        else:
            raise ValueError(f"Invalid feature type '{feature_type}'")

        return feature_config
        
    def _handle_missing_values(self, df, feature_config):
        handling_methods = feature_config.get('missing_values_handling', 'impute_mode')
        feature_name = feature_config['name']
        
        if handling_methods == 'drop_rows':
            df = df.dropna(subset=[feature_name])
        elif handling_methods == 'drop_columns':
            df = df.drop(columns=[feature_name])
        elif handling_methods in ['impute_mode', 'impute_custom_category']:
            if handling_methods == 'impute_mode':
                fill_value = df[feature_name].mode().iloc[0]
            else:
                fill_value = feature_config.get('custom_category', 'Unknown')
            df[feature_name] = df[feature_name].fillna(fill_value)
        elif handling_methods != 'none':
            raise ValueError(f"Invalid missing values handling method '{handling_methods}'")

        return df

    def _encode_categorical_feature(self, df, feature_config):
        encoding_method = feature_config.get('preprocessing', {}).get('encoding_method', 'one_hot_encoding')
        feature_name = feature_config['name']

        if encoding_method == 'none':
            return df

        if encoding_method == 'one_hot_encoding':
            encoder = OneHotEncoder(sparse=False)
            encoded_features = encoder.fit_transform(df[[feature_name]])
            encoded_feature_names = encoder.get_feature_names_out([feature_name])
            encoded_df = pd.DataFrame(encoded_features, columns=encoded_feature_names, index=df.index)
            df = pd.concat([df.drop(columns=[feature_name]), encoded_df], axis=1)
        elif encoding_method == 'label_encoding':
            label_encoder = LabelEncoder()
            df[feature_name] = label_encoder.fit_transform(df[feature_name])
        elif encoding_method == 'ordinal_encoding':
            ordinal_encoder = OrdinalEncoder()
            df[feature_name] = ordinal_encoder.fit_transform(df[[feature_name]])
        elif encoding_method == 'binary_encoding':
            binary_encoder = BinaryEncoder(cols=[feature_name])
            df = binary_encoder.fit_transform(df)
        elif encoding_method == 'target_encoding':
            target_column = feature_config.get('preprocessing', {}).get('target_column', None)
            if target_column is None:
                raise ValueError("Target column must be specified for target encoding")
            target_encoder = TargetEncoder(cols=[feature_name])
            df = target_encoder.fit_transform(df, df[target_column])
        else:
            raise ValueError(f"Invalid encoding method '{encoding_method}'")

        return df

    def preprocess(self, df):
                
        for feature_config in self.config['features']:
            feature_name = feature_config['name']
            dtype = feature_config['dtype']
            
            if feature_name not in df.columns:
                feature_config = self._ask_user_for_feature_config(feature_name)
                # Add the new feature configuration to the YAML file
                self.config['features'].append(feature_config)
                self._save_updated_config()
            
            # Check and change dtype if needed
            if df[feature_name].dtype != dtype:
                df[feature_name] = df[feature_name].astype(dtype)

            if feature_config['type'] == 'numeric':
                df = self._handle_missing_values(df, feature_config)
                df = self._scale_feature(df, feature_config)
            elif feature_config['type'] == 'categorical':
                df = self._handle_missing_values(df, feature_config)
                df = self._encode_categorical_feature(df, feature_config)
            else:
                raise ValueError(f"Invalid feature type '{feature_config['type']}'")

        return df



# Usage example:
# preprocessor = Preprocessor('config.yaml')
# preprocessed_df = preprocessor.preprocess(df)

